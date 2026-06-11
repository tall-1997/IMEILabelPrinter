@echo off
chcp 65001
echo ========================================
echo 下载 IMEI 标签打印系统离线依赖包
echo ========================================
echo.

if not exist offline_packages (
    mkdir offline_packages
)

cd offline_packages

echo 正在下载依赖包，请稍候...
echo.

pip download pygame==2.5.2 --no-deps -q
echo [1/9] pygame 下载完成

pip download pillow==10.3.0 --no-deps -q
echo [2/9] pillow 下载完成

pip download pywin32==306 --no-deps -q
echo [3/9] pywin32 下载完成

pip download PyQt5==5.15.10 --no-deps -q
echo [4/9] PyQt5 下载完成

pip download PyQt5_sip==12.13.0 --no-deps -q
echo [5/9] PyQt5_sip 下载完成

pip download PyQt5_Stub==5.15.10 --no-deps -q
echo [6/9] PyQt5_Stub 下载完成

pip download typing_extensions==4.12.0 --no-deps -q
echo [7/9] typing_extensions 下载完成

pip download openpyxl==3.1.4 --no-deps -q
echo [8/9] openpyxl 下载完成

pip download et_xmlfile==1.1.0 --no-deps -q
echo [9/9] et_xmlfile 下载完成

echo.
echo ========================================
echo 所有依赖下载完成！
echo ========================================
echo.
echo 请将以下文件一起复制到 U 盘：
echo - offline_packages 文件夹
echo - requirements.txt
echo - install_offline.bat
echo - python-3.11.9-amd64.exe (需单独下载)
echo.
pause
