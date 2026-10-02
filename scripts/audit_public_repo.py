"""Inspect Git-visible files without staging, committing, or uploading them."""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'absolute_local_path': re.compile(r'(?i)(?:\b[a-z]:[\\/]|/(?:Users|home|mnt)/)'),
    'credential_candidate': re.compile(
        r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}'
        r'|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'
        r'|(?i:(?:api[_-]?key|password|access[_-]?token|cookie)\s*[:=]\s*[\x22\x27][^\x22\x27\s]{8,})'),
}


def audit():
    raw = subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT)
    files = sorted(set(filter(None,raw.decode('utf-8').split('\0'))))
    findings = []
    for name in files:
        path = ROOT/name
        if path.suffix.lower() in {'.png','.jpg','.jpeg'}:
            continue  # Screenshots require separate visual inspection.
        try:
            lines = path.read_text(encoding='utf-8').splitlines()
        except (UnicodeError,OSError):
            findings.append(dict(file=name,kind='unreadable_or_binary')); continue
        for line_no,line in enumerate(lines,1):
            for kind,pattern in PATTERNS.items():
                if pattern.search(line): findings.append(dict(file=name,line=line_no,kind=kind))
    return dict(candidate_files=files,findings=findings,
                limitation='Pattern checks are not a guarantee; visually inspect images and review each finding.')


if __name__=='__main__':
    result=audit()
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(bool(result['findings']))
