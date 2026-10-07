"""Local desktop lifecycle. It never edits corpus, scans or review records."""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.request import build_opener, ProxyHandler


def project_root(explicit=None, executable=None, frozen=None):
    if explicit:
        root=Path(explicit).resolve()
    else:
        frozen=getattr(sys,'frozen',False) if frozen is None else frozen
        base=Path(executable or sys.executable).resolve().parent if frozen else Path(__file__).resolve().parents[1]
        # A build inside the research workspace uses its existing confirmed data.
        root=next((p for p in [base,*base.parents] if (p/'app.py').is_file()
                   and (p/'data/corpus.json').is_file() and (p/'Asset_by_user').is_dir()),base)
    if not (root/'app.py').is_file() or not (root/'data/corpus.json').is_file():
        raise ValueError('找不到程序和研究数据，请保留exe所在的完整文件夹。')
    return root


def free_port(preferred=8501):
    for candidate in (preferred,0):
        with socket.socket() as sock:
            try:
                sock.bind(('127.0.0.1',candidate))
                return sock.getsockname()[1]
            except OSError:
                if candidate==0: raise


def healthy(port):
    try:
        # Local loopback must not go through workstation HTTP proxy settings.
        with build_opener(ProxyHandler({})).open(f'http://127.0.0.1:{port}/_stcore/health',timeout=1) as response:
            return response.status==200 and response.read().strip()==b'ok'
    except (OSError,ValueError):
        return False


class InstanceLock:
    def __init__(self,path):
        self.path=Path(path); self.handle=None

    def acquire(self):
        import msvcrt
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.handle=self.path.open('a+b')
        self.handle.seek(0,2)
        if self.handle.tell()==0:
            self.handle.write(b'0'); self.handle.flush()
        self.handle.seek(0)
        try:
            msvcrt.locking(self.handle.fileno(),msvcrt.LK_NBLCK,1)
            return True
        except OSError:
            self.handle.close(); self.handle=None
            return False

    def close(self):
        if self.handle:
            import msvcrt
            self.handle.seek(0)
            msvcrt.locking(self.handle.fileno(),msvcrt.LK_UNLCK,1)
            self.handle.close(); self.handle=None


class WindowsJob:
    """Kill only our service process tree if the launcher exits unexpectedly."""
    def __init__(self,process):
        import ctypes
        from ctypes import wintypes as w
        class Basic(ctypes.Structure):
            _fields_=[('ProcessTime',ctypes.c_longlong),('JobTime',ctypes.c_longlong),
                ('Flags',w.DWORD),('MinWS',ctypes.c_size_t),('MaxWS',ctypes.c_size_t),
                ('Active',w.DWORD),('Affinity',ctypes.c_size_t),('Priority',w.DWORD),('Scheduling',w.DWORD)]
        class IO(ctypes.Structure):
            _fields_=[(name,ctypes.c_ulonglong) for name in ('ReadOps','WriteOps','OtherOps','ReadBytes','WriteBytes','OtherBytes')]
        class Extended(ctypes.Structure):
            _fields_=[('Basic',Basic),('IO',IO),('ProcessMemory',ctypes.c_size_t),
                ('JobMemory',ctypes.c_size_t),('PeakProcess',ctypes.c_size_t),('PeakJob',ctypes.c_size_t)]
        self.api=ctypes.WinDLL('kernel32',use_last_error=True)
        self.api.CreateJobObjectW.argtypes=[ctypes.c_void_p,w.LPCWSTR]; self.api.CreateJobObjectW.restype=w.HANDLE
        self.api.SetInformationJobObject.argtypes=[w.HANDLE,ctypes.c_int,ctypes.c_void_p,w.DWORD]
        self.api.AssignProcessToJobObject.argtypes=[w.HANDLE,w.HANDLE]
        self.api.CloseHandle.argtypes=[w.HANDLE]
        self.handle=self.api.CreateJobObjectW(None,None)
        info=Extended(); info.Basic.Flags=0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        if not self.handle or not self.api.SetInformationJobObject(self.handle,9,ctypes.byref(info),ctypes.sizeof(info)):
            self.close(); raise ctypes.WinError(ctypes.get_last_error())
        if not self.api.AssignProcessToJobObject(self.handle,w.HANDLE(int(process._handle))):
            self.close(); raise ctypes.WinError(ctypes.get_last_error())

    def close(self):
        if self.handle:
            self.api.CloseHandle(self.handle); self.handle=None


class Server:
    def __init__(self,root,port=None):
        self.root=Path(root); self.port=port or free_port(); self.process=None; self.job=None; self.log=None
        self.runtime=self.root/'tmp/desktop'; self.runtime.mkdir(parents=True,exist_ok=True)
        self.url=f'http://127.0.0.1:{self.port}/'

    def start(self):
        command=[sys.executable]
        if not getattr(sys,'frozen',False): command.append(str(Path(__file__).resolve().parents[1]/'desktop_launcher.py'))
        command+=['--serve','--root',str(self.root),'--port',str(self.port)]
        env=dict(os.environ,MEGA_TOOL_ROOT=str(self.root),PYTHONUTF8='1')
        self.log=(self.runtime/'server.log').open('ab',buffering=0)
        self.process=subprocess.Popen(command,cwd=self.root,env=env,stdin=subprocess.DEVNULL,
            stdout=self.log,stderr=self.log,creationflags=subprocess.CREATE_NO_WINDOW)
        try: self.job=WindowsJob(self.process)
        except Exception:
            self.stop(); raise

    def wait(self,timeout=90):
        until=time.monotonic()+timeout
        while time.monotonic()<until:
            if self.process.poll() is not None:
                raise RuntimeError('服务启动失败，详细原因见 '+str(self.runtime/'server.log'))
            if healthy(self.port): return
            time.sleep(.25)
        raise TimeoutError('服务未能在90秒内启动，详细原因见 '+str(self.runtime/'server.log'))

    def stop(self):
        if self.job: self.job.close(); self.job=None
        if self.process and self.process.poll() is None:
            self.process.terminate()
        if self.process:
            try: self.process.wait(timeout=10)
            except subprocess.TimeoutExpired: self.process.kill(); self.process.wait(timeout=5)
        if self.log: self.log.close(); self.log=None


def save_state(server):
    path=server.runtime/'instance.json'
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(dict(root=str(server.root),port=server.port,
        launcher_pid=os.getpid(),server_pid=server.process.pid),ensure_ascii=False),encoding='utf-8')
    temp.replace(path)


def existing_url(root,timeout=90):
    until=time.monotonic()+timeout
    while time.monotonic()<until:
        try:
            state=json.loads((root/'tmp/desktop/instance.json').read_text(encoding='utf-8'))
            port=state['port']
            if Path(state['root'])==root and type(port) is int and 1<=port<=65535 and healthy(port):
                return f'http://127.0.0.1:{port}/'
        except (OSError,ValueError,KeyError,TypeError): pass
        time.sleep(.25)
    raise RuntimeError('已有启动器正在运行，但服务没有就绪；请查看启动器窗口。')
