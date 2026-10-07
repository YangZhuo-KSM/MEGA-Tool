import json
from pathlib import Path
import socket
import subprocess
import sys

import pytest
from paris.desktop import project_root,free_port,InstanceLock,healthy


def make_project(root,scans=False):
    (root/'data').mkdir(parents=True)
    (root/'app.py').write_text('',encoding='utf-8')
    (root/'data/corpus.json').write_text('{}',encoding='utf-8')
    if scans: (root/'Asset_by_user').mkdir()
    return root


def test_packaged_build_uses_original_workspace_but_portable_copy_uses_its_data(tmp_path):
    original=make_project(tmp_path/'研究目录',True)
    package=make_project(original/'dist/MEGA_Tool_Windows')
    assert project_root(executable=package/'MEGA_Tool_Windows.exe',frozen=True)==original
    portable=make_project(tmp_path/'独立副本')
    assert project_root(executable=portable/'MEGA_Tool_Windows.exe',frozen=True)==portable
    assert project_root(explicit=portable)==portable
    with pytest.raises(ValueError): project_root(explicit=tmp_path/'missing')


def test_busy_port_is_not_reused_or_stopped():
    with socket.socket() as occupied:
        occupied.bind(('127.0.0.1',0)); occupied.listen()
        original=occupied.getsockname()[1]
        selected=free_port(original)
        assert selected!=original
        assert occupied.getsockname()[1]==original


@pytest.mark.skipif(sys.platform!='win32',reason='Windows launcher')
def test_single_instance_lock_releases_and_reacquires(tmp_path):
    first=InstanceLock(tmp_path/'instance.lock'); second=InstanceLock(tmp_path/'instance.lock')
    try:
        assert first.acquire() and not second.acquire()
        first.close(); assert second.acquire()
    finally: first.close(); second.close()


@pytest.mark.skipif(sys.platform!='win32',reason='Windows process lifecycle')
def test_real_launcher_health_and_owned_service_exit():
    root=Path(__file__).resolve().parents[1]
    port=free_port(0)
    result=subprocess.run([sys.executable,str(root/'desktop_launcher.py'),'--check','--root',str(root),
        '--port',str(port)],cwd=root,timeout=95,capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0,result.stderr
    state=json.loads((root/'tmp/desktop/check.json').read_text(encoding='utf-8'))
    assert state['ok'] and state['root']==str(root) and state['url']==f'http://127.0.0.1:{port}/'
    assert not healthy(port)
    assert not (root/'tmp/desktop/instance.json').exists()
