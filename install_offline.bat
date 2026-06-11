@echo off
chcp 65001
echo ========================================
echo IMEI 标签打印系统 - 离线安装
echo ========================================
echo.

echo 正在安装 Python 依赖包...
echo.

pip install --no-index --find-links=.\offline_packages -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo 安装完成！
    echo ========================================
    echo.
    echo 现在可以运行程序：
    echo   python main.py
    echo.
    echo 或运行诊断工具：
    echo   python diagnose_bartender.py "你的模板路径.btw"
    echo.
) else (
    echo.
    echo ========================================
    echo 安装失败！
    echo ========================================
    echo.
    echo 请确认：
    echo 1. offline_packages 文件夹存在且包含.whl 文件
    echo 2. requirements.txt 文件存在
    echo 3. Python 已正确安装并添加到 PATH
    echo.
)

pause
