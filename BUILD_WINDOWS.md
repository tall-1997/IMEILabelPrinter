# Windows 打包说明

## 重要提示

**此程序只能在 Windows 系统上打包和运行**，因为依赖 BarTender 2021（仅支持 Windows）。

## 打包步骤

### 方法一：使用一键打包脚本（推荐）

1. 将整个 `IMEILabelPrinter` 文件夹复制到 **Windows 电脑**
2. 双击运行 `build.bat`
3. 等待打包完成（约 2-5 分钟）
4. 打包完成后，`dist` 目录即为可分发的程序

### 方法二：手动执行命令

在 Windows 命令行（CMD）中依次执行：

```cmd
cd D:\Desktop\IMEILabelPrinter

REM 1. 安装依赖
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

REM 2. 安装 PyInstaller
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple

REM 3. 执行打包
pyinstaller --clean IMEILabelPrinter.spec
```

## 打包结果

打包完成后，`dist` 目录结构如下：

```
dist/IMEI 标签打印系统/
├── IMEI 标签打印系统.exe    ← 主程序（双击运行）
├── config.json              ← 配置文件
├── templates/
│   └── README.txt          ← 模板配置说明
├── data/                    ← 数据目录（首次运行时自动创建）
└── 其他依赖文件             ← PyInstaller 自动生成
```

## 分发使用

### 方式一：整个目录分发（推荐）

1. 将整个 `dist/IMEI 标签打印系统` 文件夹复制到目标电脑
2. 在目标电脑上放置 BarTender 模板到 `templates/` 目录
3. 双击 `IMEI 标签打印系统.exe` 运行

### 方式二：创建安装包（可选）

使用 NSIS、Inno Setup 等工具创建安装程序：
1. 将 `dist/IMEI 标签打印系统` 所有内容打包
2. 创建安装向导
3. 生成 `.exe` 安装程序

## 目标电脑要求

### 必需环境
- ✅ Windows 10/11 操作系统
- ✅ BarTender 2021 Automation 版（已安装并激活）
- ✅ 标签打印机驱动已安装

### 无需安装
- ❌ 不需要 Python 环境
- ❌ 不需要安装任何依赖包
- ❌ 不需要 BarTender SDK（Automation 版已包含）

## 常见问题

### Q: 打包时提示 "No module named 'win32com'"
**A:** 确保已安装 pywin32：
```cmd
pip install pywin32
```

### Q: 打包后运行提示 "BarTender.Application 不存在"
**A:** 
- 目标电脑必须安装 BarTender 2021 Automation 版
- 检查 BarTender 是否正确激活
- 尝试以管理员身份运行

### Q: 杀毒软件报毒
**A:** PyInstaller 打包的程序有时会被误报，可以：
1. 添加到杀毒软件白名单
2. 使用代码签名证书签名（企业使用）
3. 向杀毒软件厂商提交误报申诉

### Q: 生成的 EXE 文件太大（超过 100MB）
**A:** 这是正常的，因为包含了：
- Python 运行时（~30MB）
- PyQt5 库（~40MB）
- matplotlib、pandas 等库（~30MB）

可以通过以下方式优化：
- 使用 `--onefile` 参数生成单文件
- 移除不需要的模块
- 使用 UPX 压缩（已默认启用）

## 测试清单

打包后请测试以下功能：

- [ ] 程序能否正常启动
- [ ] 三个标签页能否正常切换
- [ ] 加载 BarTender 模板是否成功
- [ ] 输入 IMEI 能否正常打印
- [ ] 重复打印校验是否生效
- [ ] 历史记录能否正常显示
- [ ] 统计图表能否正常生成
- [ ] 导出 Excel 功能是否正常

## 技术支持

如遇到打包问题，请提供：
1. 完整的错误信息
2. Windows 版本
3. Python 版本（`python --version`）
4. BarTender 版本信息
