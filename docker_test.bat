@echo off
REM Docker测试脚本 - Windows版本
setlocal enabledelayedexpansion
chcp 65001 >nul

:menu
echo.
echo ============================================================
echo 🧪 Docker测试菜单
echo ============================================================
echo.
echo   1. 启动服务
echo   2. 运行所有测试
echo   3. 健康检查
echo   4. 聊天接口测试
echo   5. 工具和股票列表
echo   6. 查看日志
echo   7. 交互式测试
echo   8. 停止服务
echo   0. 退出
echo.
set /p choice="请选择 [0-8]: "

if "%choice%"=="1" goto start_service
if "%choice%"=="2" goto run_all_tests
if "%choice%"=="3" goto test_health
if "%choice%"=="4" goto test_chat
if "%choice%"=="5" goto test_lists
if "%choice%"=="6" goto show_logs
if "%choice%"=="7" goto interactive
if "%choice%"=="8" goto stop_service
if "%choice%"=="0" goto exit
echo [WARNING] 无效选项
pause
goto menu

:start_service
echo.
echo ============================================================
echo 🚀 启动Mock模式服务
echo ============================================================
echo.
echo [INFO] 停止已有容器...
docker-compose --profile mock down 2>nul

echo [INFO] 启动新容器...
docker-compose --profile mock up -d

echo [INFO] 等待服务启动...
timeout /t 5 /nobreak >nul

echo [SUCCESS] 服务已启动
pause
goto menu

:test_health
echo.
echo ============================================================
echo 🏥 健康检查测试
echo ============================================================
echo.
echo [INFO] 测试 /health 端点...
curl -s http://localhost:8765/health
echo.
pause
goto menu

:test_chat
echo.
echo ============================================================
echo 💬 聊天接口测试
echo ============================================================
echo.
echo [INFO] 发送测试查询: 比亚迪现在多少钱？
curl -s -X POST http://localhost:8765/chat -H "Content-Type: application/json" -d "{\"query\": \"比亚迪现在多少钱？\"}"
echo.
pause
goto menu

:test_lists
echo.
echo ============================================================
echo 🔧 工具列表
echo ============================================================
echo.
curl -s http://localhost:8765/tools
echo.
echo.
echo ============================================================
echo 📊 股票列表
echo ============================================================
echo.
curl -s http://localhost:8765/stocks
echo.
pause
goto menu

:show_logs
echo.
echo ============================================================
echo 📋 容器日志
echo ============================================================
echo.
docker-compose logs --tail=30 agent-mock
echo.
pause
goto menu

:interactive
echo.
echo ============================================================
echo 🎮 交互式测试
echo ============================================================
echo.
echo 输入你的问题（输入 'exit' 返回菜单）:
echo.

:interactive_loop
set /p query="您: "
if "%query%"=="exit" goto menu
if "%query%"=="" goto interactive_loop

echo.
echo Agent: 思考中...
curl -s -X POST http://localhost:8765/chat -H "Content-Type: application/json" -d "{\"query\": \"%query%\"}"
echo.
echo.
echo ------------------------------------------------------------
echo.
goto interactive_loop

:run_all_tests
echo.
echo ============================================================
echo 🧪 运行所有测试
echo ============================================================
echo.

echo [TEST 1/4] 健康检查...
curl -s http://localhost:8765/health | findstr "healthy" >nul
if errorlevel 1 (
    echo [FAIL] 健康检查失败
) else (
    echo [PASS] 健康检查通过
)

echo.
echo [TEST 2/4] 聊天接口...
curl -s -X POST http://localhost:8765/chat -H "Content-Type: application/json" -d "{\"query\": \"测试\"}" | findstr "success" >nul
if errorlevel 1 (
    echo [FAIL] 聊天接口失败
) else (
    echo [PASS] 聊天接口正常
)

echo.
echo [TEST 3/4] 工具列表...
curl -s http://localhost:8765/tools | findstr "count" >nul
if errorlevel 1 (
    echo [FAIL] 工具列表失败
) else (
    echo [PASS] 工具列表正常
)

echo.
echo [TEST 4/4] 股票列表...
curl -s http://localhost:8765/stocks | findstr "count" >nul
if errorlevel 1 (
    echo [FAIL] 股票列表失败
) else (
    echo [PASS] 股票列表正常
)

echo.
echo ============================================================
echo [SUCCESS] 所有测试完成！
echo ============================================================
pause
goto menu

:stop_service
echo.
echo [INFO] 停止服务...
docker-compose --profile mock down
echo [SUCCESS] 服务已停止
pause
goto menu

:exit
echo [INFO] 退出
exit /b 0
