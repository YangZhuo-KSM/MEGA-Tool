"""Update the verified frozen Windows runtime with current app/data and archive it.

Use only for data/UI updates that do not change frozen paris modules. Rebuild the
runtime with build_windows.py when runtime behavior or dependencies change.
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from paris.corpus import load_corpus


def main():
    data = load_corpus()
    release = data['release']
    target = ROOT/'dist/MEGA_Tool_Windows'
    exe = target/'MEGA_Tool_Windows.exe'
    if not exe.is_file() or not (target/'_internal').is_dir():
        raise RuntimeError('Build the Windows runtime first')
    if (target/'data/reviews.json').exists():
        raise RuntimeError('Distribution contains user reviews; preserve it before updating')
    archive = ROOT/f'dist/MEGA_Tool-Windows-{release.split("-")[-1]}.zip'
    if archive.exists():
        raise RuntimeError(f'Archive already exists; refusing to replace: {archive}')
    backup = ROOT/f'local_backups/windows-before-{release.split("-")[-1]}'
    backup.mkdir(parents=True,exist_ok=False)
    copies = [('app.py','app.py'),('docs/WINDOWS_EXE.md','使用说明.md'),
              ('local_sources.example.json','local_sources.example.json'),
              ('.streamlit/config.toml','.streamlit/config.toml')]
    copies += [(f'data/{n}.json',f'data/{n}.json') for n in
               ('corpus','extraction','coverage_plan','sampling_plan')]
    hashes = {}
    for source, destination in copies:
        old = target/destination
        if old.exists():
            saved = backup/destination
            saved.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(old,saved)
        old.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/source,old)
        digest = hashlib.sha256(old.read_bytes()).hexdigest()
        assert digest == hashlib.sha256((ROOT/source).read_bytes()).hexdigest()
        hashes[destination] = digest
    metadata = dict(release=release,groups=len(data['alignments']),
                    runtime='Existing verified PyInstaller runtime; behavior/dependencies unchanged',
                    runtime_sha256=hashlib.sha256(exe.read_bytes()).hexdigest(),files=hashes)
    (target/'DATA_RELEASE.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    with ZipFile(archive,'w',ZIP_DEFLATED) as z:
        for path in sorted(target.rglob('*')):
            relative = path.relative_to(target)
            if not path.is_file() or relative.parts[0] in ('tmp','Asset_by_user'):
                continue
            if relative.as_posix() in ('data/reviews.json','local_sources.json'):
                raise RuntimeError(f'Private file in distribution: {relative}')
            z.write(path,'MEGA_Tool_Windows/'+relative.as_posix())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix('.zip.sha256').write_text(f'{digest}  {archive.name}\n',encoding='ascii')
    print(json.dumps(dict(archive=str(archive),sha256=digest,metadata=metadata),ensure_ascii=False))


if __name__ == '__main__':
    main()
