# IMEI 标签打印系统打包脚本
@echo off
chcp 65001 >nul

echo ========================================
echo IMEI 标签打印系统 - 打包工具
echo ========================================
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python 环境，请先安装 Python 3.9+
    pause
    exit /b 1
)

echo [1/4] 检查 Python 环境... OK
echo.

REM 安装依赖
echo [2/4] 安装依赖包...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [警告] 依赖安装可能不完整，但将继续打包
)
echo.

REM 安装 PyInstaller
echo [3/4] 安装 PyInstaller...
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
echo.

REM 执行打包
echo [4/4] 执行打包...
pyinstaller --clean IMEILabelPrinter.spec
echo.

REM 检查打包结果
if exist "dist\IMEI 标签打印系统.exe" (
    echo ========================================
    echo 打包成功!
    echo 可执行文件位置：dist\IMEI 标签打印系统.exe
    echo ========================================
    
    REM 复制配置文件
    echo.
    echo 复制配置文件...
    copy "config.json" "dist\config.json" >nul
    mkdir "dist\data" >nul 2>&1
    mkdir "dist\templates" >nul 2>&1
    copy "templates\README.txt" "dist\templates\README.txt" >nul
    
    echo.
    echo 打包完成！目录结构：
    echo   dist/
    echo   ├── IMEI 标签打印系统.exe    (主程序)
    echo   ├── config.json              (配置文件)
    echo   ├── data/                    (数据目录，自动创建)
    echo   └── templates/               (模板目录)
    echo       └── README.txt           (模板配置说明)
    
    echo.
    echo 使用说明:
    echo 1. 将整个 dist 目录复制到目标机器
    echo 2. 确保目标机器已安装 BarTender 2021 Automation
    echo 3. 将您的 .btw 模板文件放入 templates 目录
    echo 4. 运行 IMEI 标签打印系统.exe
    
) else (
    echo ========================================
    echo [错误] 打包失败！请检查错误信息
    echo ========================================
)

echo.
pause
