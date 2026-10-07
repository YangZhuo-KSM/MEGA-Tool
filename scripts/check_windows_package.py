"""Extract outside the workspace and verify the actual executable, not Python source."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.desktop import healthy


def main():
    staging=Path(tempfile.mkdtemp(prefix='MEGA_Tool-便携验收-'))
    with ZipFile(ROOT/'dist/MEGA_Tool-Windows-alpha8.zip') as archive:
        archive.extractall(staging)
    project=staging/'MEGA_Tool_Windows'
    exe=project/'MEGA_Tool_Windows.exe'
    # The original launcher deliberately occupies 8501. This copy must avoid it.
    assert healthy(8501),'Start the original launcher before this conflict check'
    check=subprocess.run([str(exe),'--check'],cwd=project,timeout=95,creationflags=subprocess.CREATE_NO_WINDOW)
    assert check.returncode==0,'See the Windows temporary launcher error log'
    result=json.loads((project/'tmp/desktop/check.json').read_text(encoding='utf-8'))
    assert Path(result['root'])==project and ':8501/' not in result['url']
    assert not healthy(int(result['url'].split(':')[-1].strip('/')))
    assert not (project/'Asset_by_user').exists() and not (project/'data/reviews.json').exists()
    launcher=subprocess.Popen([str(exe),'--no-browser','--port','8513'],cwd=project,creationflags=subprocess.CREATE_NO_WINDOW)
    deadline=time.monotonic()+90
    while time.monotonic()<deadline:
        assert launcher.poll() is None,'Portable launcher exited early'
        state_path=project/'tmp/desktop/instance.json'
        if state_path.exists() and healthy(8513): break
        time.sleep(.25)
    else: raise TimeoutError('Portable GUI did not become ready')
    before=json.loads(state_path.read_text(encoding='utf-8'))
    duplicate=subprocess.run([str(exe),'--no-browser'],cwd=project,timeout=95,creationflags=subprocess.CREATE_NO_WINDOW)
    assert duplicate.returncode==0 and json.loads(state_path.read_text(encoding='utf-8'))==before
    assert healthy(8501),'Portable check interfered with the original server'
    report=dict(portable_root=str(project),staging=str(staging),launcher_pid=launcher.pid,
                server_pid=before['server_pid'],url='http://127.0.0.1:8513/',
                check_result=result,duplicate='passed',port_conflict='passed',
                next_action='Inspect portable UI without PDFs, then run this exe with --stop')
    (ROOT/'tmp/exe-package-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__=='__main__': main()
