$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$parisPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $parisPython)) {
    Write-Error 'Please create .venv and install requirements.txt. See README.md.'
}
& $parisPython -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
