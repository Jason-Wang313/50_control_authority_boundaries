$ErrorActionPreference = "Stop"

$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
$Paper = Join-Path $Root "paper"
$Data = Join-Path $Root "data"
$OutPdf = "C:\Users\wangz\Downloads\50.pdf"

New-Item -ItemType Directory -Force -Path $Data | Out-Null

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Program,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $Program @Arguments | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "$Program failed with exit code $LASTEXITCODE. Check paper/main.log for details."
    }
}

Push-Location $Paper
try {
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
    Invoke-Checked pdflatex -interaction=nonstopmode -halt-on-error main.tex
}
finally {
    Pop-Location
}

$BuiltPdf = Join-Path $Paper "main.pdf"
if (-not (Test-Path $BuiltPdf)) {
    throw "Expected PDF was not produced: $BuiltPdf"
}

Copy-Item -Force -Path $BuiltPdf -Destination $OutPdf
Remove-Item -Force -LiteralPath $BuiltPdf

$hash = Get-FileHash -Path $OutPdf -Algorithm SHA256
$status = [ordered]@{
    paper = 50
    status = "final_v3_full_scale"
    canonical_pdf = $OutPdf
    canonical_sha256 = $hash.Hash
    local_pdf_removed = -not (Test-Path $BuiltPdf)
    built_at = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
}

$status | ConvertTo-Json | Set-Content -Encoding UTF8 -Path (Join-Path $Data "build_status.json")
