# PowerShell脚本：创建和配置虚拟环境

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  股票Agent系统 - 环境设置" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python版本
Write-Host "🔍 检查Python版本..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "   $pythonVersion" -ForegroundColor Green

if ($pythonVersion -match "Python 3\.([0-9]+)\.") {
    $minorVersion = [int]$matches[1]
    if ($minorVersion -lt 10) {
        Write-Host "   ❌ Python版本过低，需要 >= 3.10" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✅ Python版本符合要求" -ForegroundColor Green
}

Write-Host ""

# 创建虚拟环境
if (Test-Path "venv") {
    Write-Host "📦 虚拟环境已存在" -ForegroundColor Yellow
    $recreate = Read-Host "是否重新创建? [y/N]"
    if ($recreate -eq "y" -or $recreate -eq "Y") {
        Write-Host "   删除旧环境..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force venv
    } else {
        Write-Host "   跳过创建" -ForegroundColor Green
        Write-Host ""
        Write-Host "🚀 激活虚拟环境:" -ForegroundColor Cyan
        Write-Host "   venv\Scripts\activate" -ForegroundColor White
        exit 0
    }
}

Write-Host "📦 创建虚拟环境..." -ForegroundColor Yellow
python -m venv venv

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ 创建失败" -ForegroundColor Red
    exit 1
}

Write-Host "   ✅ 创建成功" -ForegroundColor Green
Write-Host ""

# 激活虚拟环境
Write-Host "🔧 激活虚拟环境..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# 升级pip
Write-Host "📦 升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip -q

Write-Host "   ✅ pip已升级" -ForegroundColor Green
Write-Host ""

# 询问是否安装依赖
Write-Host "📦 是否安装项目依赖?" -ForegroundColor Yellow
Write-Host "   1. 服务端依赖 (需要GPU)" -ForegroundColor White
Write-Host "   2. 客户端依赖 (无需GPU)" -ForegroundColor White
Write-Host "   3. 全部依赖" -ForegroundColor White
Write-Host "   4. 跳过" -ForegroundColor White

$choice = Read-Host "请选择 [1-4]"

switch ($choice) {
    "1" {
        Write-Host "   安装服务端依赖..." -ForegroundColor Yellow
        pip install -r server\requirements.txt
    }
    "2" {
        Write-Host "   安装客户端依赖..." -ForegroundColor Yellow
        pip install -r client\requirements.txt
    }
    "3" {
        Write-Host "   安装全部依赖..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
    "4" {
        Write-Host "   跳过安装依赖" -ForegroundColor Green
    }
    default {
        Write-Host "   跳过安装依赖" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  ✅ 环境设置完成！" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 下一步操作:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 激活虚拟环境 (如果未激活):" -ForegroundColor White
Write-Host "   venv\Scripts\activate" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 运行环境检查:" -ForegroundColor White
Write-Host "   python scripts\setup_env.py" -ForegroundColor Gray
Write-Host ""
Write-Host "3. 下载模型:" -ForegroundColor White
Write-Host "   python scripts\download_model.py" -ForegroundColor Gray
Write-Host ""
Write-Host "4. 下载数据:" -ForegroundColor White
Write-Host "   python scripts\download_stock_data.py" -ForegroundColor Gray
Write-Host ""
