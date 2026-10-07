"""Windows desktop entry point and frozen Streamlit worker."""
import argparse
import os
from pathlib import Path
import sys


def serve(root,port):
    os.environ['MEGA_TOOL_ROOT']=str(root)
    os.chdir(root)
    # Windowed executables have no standard streams. Streamlit still logs to them.
    log=(root/'tmp/desktop/server-worker.log').open('a',encoding='utf-8',buffering=1)
    sys.stdout=log; sys.stderr=log
    import streamlit.web.bootstrap
    options={'server_address':'127.0.0.1','server_port':port,'server_headless':True,
             'server_fileWatcherType':'none','browser_gatherUsageStats':False,'global_developmentMode':False}
    streamlit.web.bootstrap.load_config_options(options)
    streamlit.web.bootstrap.run(str(root/'app.py'),False,[],options)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root'); parser.add_argument('--port',type=int)
    parser.add_argument('--serve',action='store_true')
    parser.add_argument('--check',action='store_true',help='Check packaged server and stop it without opening a browser')
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('--stop',action='store_true',help='Ask the launcher for this workspace to exit')
    args=parser.parse_args()
    from paris.desktop import project_root,Server,InstanceLock,save_state,existing_url
    root=project_root(args.root)
    if args.serve:
        serve(root,args.port); return
    runtime=root/'tmp/desktop'; runtime.mkdir(parents=True,exist_ok=True)
    if args.stop:
        (runtime/'exit.request').touch(); return
    lock=InstanceLock(runtime/'instance.lock')
    import webbrowser
    if not lock.acquire():
        if args.check: raise RuntimeError('启动器已运行，诊断测试不会中止已有服务。')
        url=existing_url(root)
        if not args.no_browser: webbrowser.open(url)
        return
    server=None
    try:
        (runtime/'exit.request').unlink(missing_ok=True)
        (runtime/'instance.json').unlink(missing_ok=True)
        if args.check: (runtime/'check.json').unlink(missing_ok=True)
        server=Server(root,args.port)
        server.start()
        if args.check:
            server.wait(); save_state(server)
            (runtime/'check.json').write_text(__import__('json').dumps(
                dict(ok=True,url=server.url,root=str(root),server_pid=server.process.pid)),encoding='utf-8')
            return
        import tkinter as tk
        from tkinter import ttk
        window=tk.Tk(); window.title('巴黎手稿研究工具'); window.geometry('530x280'); window.resizable(False,False)
        window.configure(background='#f7f5ef')
        text=tk.StringVar(value='正在启动，请稍候…')
        tk.Label(window,text='巴黎手稿 · 德中对读',font=('Microsoft YaHei',17),bg='#f7f5ef',fg='#253b34').pack(pady=(24,12))
        tk.Label(window,textvariable=text,font=('Microsoft YaHei',11),bg='#f7f5ef',wraplength=490).pack(pady=8)
        tk.Label(window,text='关闭这个启动器窗口将停止本地服务。',bg='#f7f5ef',fg='#66786d').pack(pady=6)
        buttons=ttk.Frame(window); buttons.pack(pady=14)
        open_button=ttk.Button(buttons,text='打开阅读器',state='disabled',command=lambda:webbrowser.open(server.url))
        open_button.pack(side='left',padx=8)
        ttk.Button(buttons,text='打开运行日志',command=lambda:os.startfile(str(runtime))).pack(side='left',padx=8)
        ttk.Button(buttons,text='退出',command=window.destroy).pack(side='left',padx=8)
        import threading,queue
        events=queue.Queue()
        def boot():
            try: server.wait(); events.put(None)
            except Exception as error: events.put(str(error))
        threading.Thread(target=boot,daemon=True).start()
        ready=False
        def poll():
            nonlocal ready
            if (runtime/'exit.request').exists(): window.destroy(); return
            if not events.empty():
                error=events.get()
                if error: text.set(error)
                else:
                    ready=True; save_state(server); text.set('已启动：'+server.url+'\n研究数据：'+str(root))
                    open_button.configure(state='normal')
                    if not args.no_browser: webbrowser.open(server.url)
            if ready and server.process.poll() is not None:
                ready=False; open_button.configure(state='disabled'); text.set('服务已停止，请退出后重新打开exe。详细原因见运行日志。')
            window.after(300,poll)
        window.after(100,poll); window.mainloop()
    finally:
        if server: server.stop()
        (runtime/'instance.json').unlink(missing_ok=True)
        (runtime/'exit.request').unlink(missing_ok=True)
        lock.close()


if __name__=='__main__':
    worker='--serve' in sys.argv
    diagnostic='--check' in sys.argv
    try: main()
    except Exception as error:
        # Preserve actionable diagnostics even in --windowed builds.
        import traceback,tempfile
        path=Path(tempfile.gettempdir())/'MEGA_Tool-launcher-error.log'
        trace=traceback.format_exc()
        path.write_text(trace,encoding='utf-8')
        if sys.stderr is not None: sys.stderr.write(trace)
        if not diagnostic and not worker:
            import tkinter as tk
            from tkinter import messagebox
            window=tk.Tk(); window.withdraw()
            messagebox.showerror('巴黎手稿启动失败',str(error)+'\n日志：'+str(path)); window.destroy()
        raise SystemExit(1)
