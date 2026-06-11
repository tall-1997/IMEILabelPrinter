# IMEI 标签打印系统 - 离线安装指南

## 📦 离线包内容

```
offline_release/
├── python-3.11.9-amd64.exe          # Python 安装包（需单独下载）
├── IMEILabelPrinter_source.zip      # 程序源代码
├── offline_packages/                 # Python 依赖包
├── requirements.txt                  # 依赖列表
├── install_offline.bat               # 一键安装脚本
└── README_OFFLINE.md                 # 本文件
```

## 🚀 快速安装步骤

### 步骤 1：下载 Python

在有网络的机器上下载：
```
https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
```

### 步骤 2：准备离线包

在有网络的机器上：

```bash
# 1. 下载依赖包
download_offline_deps.bat

# 2. 打包源代码
# 右键 IMEILabelPrinter 文件夹 -> 发送到 -> 压缩文件夹
# 重命名为 IMEILabelPrinter_source.zip
```

### 步骤 3：复制到 U 盘

将以下文件复制到 U 盘：
- `python-3.11.9-amd64.exe`
- `IMEILabelPrinter_source.zip`
- `offline_packages/` 文件夹
- `requirements.txt`
- `install_offline.bat`
- 本文件

### 步骤 4：在目标机器上安装

#### 4.1 安装 Python
1. 双击运行 `python-3.11.9-amd64.exe`
2. **务必勾选** ✅ "Add Python to PATH"
3. 点击 "Install Now"

#### 4.2 安装依赖
1. 解压 `IMEILabelPrinter_source.zip`
2. 进入解压后的文件夹
3. 双击运行 `install_offline.bat`

#### 4.3 运行程序

```bash
# 运行主程序
python main.py

# 运行诊断工具（推荐先运行这个）
python diagnose_bartender.py "你的模板路径.btw"
```

## 🔧 故障排查

### 问题 1：pip 命令不存在
**解决**: Python 安装时没有勾选 "Add Python to PATH"，重新安装 Python 并勾选。

### 问题 2：依赖安装失败
**解决**: 检查 `offline_packages` 文件夹是否包含 `.whl` 文件，如没有请重新运行 `download_offline_deps.bat`。

### 问题 3：BarTender 模板加载失败
**解决**: 运行 `diagnose_bartender.py` 查看具体错误信息。

## 📞 获取帮助

如果安装过程中遇到问题，请提供：
1. `diagnose_bartender.py` 的完整输出
2. 安装时的错误截图
3. BarTender 版本号

---

**版本**: v1.2.2  
**更新日期**: 2025-02-xx  
**兼容系统**: Windows 10/11 x64  
**BarTender 版本**: 2021/2022 Enterprise
