"""Reproducible folder distribution; original PDFs and personal reviews excluded."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
TARGET=ROOT/'dist/MEGA_Tool_Windows'

def main():
    if (TARGET/'data/reviews.json').exists():
        raise RuntimeError('发行目录存在人工审核数据；请先保留整个目录，再使用新的输出位置。')
    subprocess.run([sys.executable,'-m','PyInstaller','--noconfirm','--onedir','--windowed',
        '--name','MEGA_Tool_Windows','--distpath',str(ROOT/'dist'),'--workpath',str(ROOT/'build/windows'),
        '--specpath',str(ROOT/'build'),'--paths',str(ROOT),'--collect-all','streamlit',
        '--collect-all','altair','--collect-all','pypdfium2','--collect-submodules','paris',
        '--copy-metadata','streamlit','--copy-metadata','pypdfium2',
        '--hidden-import','tkinter','--hidden-import','tkinter.messagebox',
        '--hidden-import','streamlit.web.bootstrap','--hidden-import','pypdf',
        str(ROOT/'desktop_launcher.py')],cwd=ROOT,check=True)
    for name in ('app.py','local_sources.example.json'):
        shutil.copy2(ROOT/name,TARGET/name)
    for name in ('corpus.json','coverage_plan.json','sampling_plan.json','extraction.json'):
        dest=TARGET/'data'/name; dest.parent.mkdir(exist_ok=True)
        shutil.copy2(ROOT/'data'/name,dest)
    (TARGET/'.streamlit').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'.streamlit/config.toml',TARGET/'.streamlit/config.toml')
    shutil.copy2(ROOT/'docs/WINDOWS_EXE.md',TARGET/'使用说明.md')
    print('Built',TARGET/'MEGA_Tool_Windows.exe')

if __name__=='__main__': main()
