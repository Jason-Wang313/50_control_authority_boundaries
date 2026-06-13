$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Paper = Join-Path $Root "paper"
$Data = Join-Path $Root "data"
$OutPdf = "C:\Users\wangz\Downloads\50.pdf"

New-Item -ItemType Directory -Force -Path $Data | Out-Null

Push-Location $Paper
try {
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    Copy-Item -Force -Path "main.pdf" -Destination $OutPdf
    Remove-Item -Force -Path "main.pdf"
}
finally {
    Pop-Location
}

$status = [ordered]@{
    paper = 50
    decision = "workshop-only"
    canonical_pdf = $OutPdf
    local_pdf_removed = -not (Test-Path (Join-Path $Paper "main.pdf"))
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}

$status | ConvertTo-Json | Set-Content -Encoding UTF8 -Path (Join-Path $Data "build_status.json")
