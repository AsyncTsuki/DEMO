@echo off
chcp 65001 >nul
echo ========================================
echo 数据库重置和初始化工具
echo ========================================
echo.
echo 警告: 此操作会删除所有现有数据！
echo.
set /p confirm=确认继续吗? (yes/no): 

if /i not "%confirm%"=="yes" (
    echo 操作已取消
    pause
    exit /b
)

echo.
echo [1/2] 重置数据库...
python reset_db.py
if errorlevel 1 (
    echo 重置数据库失败！
    pause
    exit /b 1
)

echo.
echo [2/2] 初始化测试数据...
python init_db.py
if errorlevel 1 (
    echo 初始化数据失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✓ 数据库重置完成！
echo ========================================
echo.
echo 测试账户:
echo   用户名: admin  密码: admin123
echo   用户名: test   密码: test123
echo.
pause
