@echo off
REM Docker构建脚本 - Windows版本
REM 带友好提示和进度显示

setlocal enabledelayedexpansion

REM 设置代码页为UTF-8
chcp 65001 >nul

:menu
echo.
echo ============================================================
echo 🐳 股票咨询Agent - Docker构建工具
echo ============================================================
echo.
echo 请选择构建模式：
echo.
echo   1. Mock模式 (推荐测试)
echo      - 无需GPU
echo      - 构建快速 (~2-3分钟)
echo      - 镜像小 (~500MB)
echo.
echo   2. ChatGLM3-6B模式
echo      - 需要GPU (RTX 3070 8GB+)
echo      - 构建较慢 (~5-10分钟)
echo      - 镜像大 (~2GB)
echo.
echo   3. Qwen2-1.5B模式
echo      - 需要GPU (RTX 3060 6GB+)
echo      - 构建中等 (~4-8分钟)
echo      - 镜像中等 (~1.5GB)
echo.
echo   4. 构建所有模式
echo.
echo   0. 退出
echo.
set /p choice="请输入选项 [0-4]: "

if "%choice%"=="1" goto build_mock
if "%choice%"=="2" goto build_chatglm3
if "%choice%"=="3" goto build_qwen2
if "%choice%"=="4" goto build_all
if "%choice%"=="0" goto exit
echo [ERROR] 无效选项
goto menu

:check_docker
echo [INFO] 检查Docker环境...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker未运行，请启动Docker Desktop
    pause
    exit /b 1
)
echo [SUCCESS] Docker环境正常
goto :eof

:check_gpu
echo [INFO] 检查GPU支持...
nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo [WARNING] 未检测到NVIDIA GPU
    goto :eof
)
echo [SUCCESS] 检测到NVIDIA GPU
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
goto :eof

:build_mock
call :check_docker
echo.
echo ============================================================
echo 🔨 构建Mock模式镜像
echo ============================================================
echo.
echo [INFO] 开始构建...
echo [INFO] 预计时间: 2-3分钟
echo.

docker build --build-arg MODE=mock -t stock-agent:mock --progress=plain .

if errorlevel 1 (
    echo.
    echo [ERROR] 构建失败
    pause
    goto menu
)

echo.
echo [SUCCESS] Mock模式镜像构建完成！
echo [INFO] 镜像名称: stock-agent:mock
docker images stock-agent:mock
goto show_results

:build_chatglm3
call :check_docker
call :check_gpu
echo.
echo ============================================================
echo 🔨 构建ChatGLM3-6B模式镜像
echo ============================================================
echo.
echo [INFO] 开始构建...
echo [INFO] 预计时间: 5-10分钟
echo.

docker build --build-arg MODE=gpu -t stock-agent:chatglm3 --progress=plain .

if errorlevel 1 (
    echo.
    echo [ERROR] 构建失败
    pause
    goto menu
)

echo.
echo [SUCCESS] ChatGLM3模式镜像构建完成！
echo [INFO] 镜像名称: stock-agent:chatglm3
docker images stock-agent:chatglm3
goto show_results

:build_qwen2
call :check_docker
call :check_gpu
echo.
echo ============================================================
echo 🔨 构建Qwen2-1.5B模式镜像
echo ============================================================
echo.
echo [INFO] 开始构建...
echo [INFO] 预计时间: 4-8分钟
echo.

docker build --build-arg MODE=gpu -t stock-agent:qwen2 --progress=plain .

if errorlevel 1 (
    echo.
    echo [ERROR] 构建失败
    pause
    goto menu
)

echo.
echo [SUCCESS] Qwen2模式镜像构建完成！
echo [INFO] 镜像名称: stock-agent:qwen2
docker images stock-agent:qwen2
goto show_results

:build_all
call :check_docker
echo.
echo ============================================================
echo 🔨 构建所有模式
echo ============================================================
echo.

call :build_mock_silent
echo.
call :build_chatglm3_silent
echo.
call :build_qwen2_silent

goto show_results

:build_mock_silent
echo [INFO] 构建Mock模式...
docker build --build-arg MODE=mock -t stock-agent:mock -q .
echo [SUCCESS] Mock模式完成
goto :eof

:build_chatglm3_silent
echo [INFO] 构建ChatGLM3模式...
docker build --build-arg MODE=gpu -t stock-agent:chatglm3 -q .
echo [SUCCESS] ChatGLM3模式完成
goto :eof

:build_qwen2_silent
echo [INFO] 构建Qwen2模式...
docker build --build-arg MODE=gpu -t stock-agent:qwen2 -q .
echo [SUCCESS] Qwen2模式完成
goto :eof

:show_results
echo.
echo ============================================================
echo 📊 构建结果汇总
echo ============================================================
echo.
echo 已构建的镜像：
docker images stock-agent
echo.
echo [INFO] 下一步：
echo   1. 启动服务: docker-compose --profile mock up -d
echo   2. 查看日志: docker-compose logs -f agent-mock
echo   3. 测试接口: curl http://localhost:8765/health
echo.
pause
goto menu

:exit
echo [INFO] 退出
exit /b 0
