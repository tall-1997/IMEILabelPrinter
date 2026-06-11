"""
BarTender 连接测试工具
用于诊断 BarTender COM 连接问题
"""

import sys
import pythoncom
import win32com.client


def test_bartender_connection():
    """测试 BarTender COM 连接"""
    print("=" * 60)
    print("BarTender COM 连接测试工具")
    print("=" * 60)
    print()
    
    # 测试 1: COM 初始化
    print("[测试 1] COM 初始化...")
    try:
        pythoncom.CoInitialize()
        print("✓ COM 初始化成功")
    except Exception as e:
        print(f"✗ COM 初始化失败：{e}")
        return
    print()
    
    # 测试 2: 创建 BarTender 应用对象
    print("[测试 2] 创建 BarTender.Application 对象...")
    try:
        app = win32com.client.Dispatch("BarTender.Application")
        if app:
            print("✓ BarTender 应用程序对象创建成功")
            print(f"  应用程序名称：BarTender")
        else:
            print("✗ 无法创建 BarTender 应用程序对象")
            return
    except pythoncom.com_error as e:
        print(f"✗ COM 错误：{e}")
        print(f"  错误代码：{e.hresult}")
        print("\n可能原因：")
        print("  1. BarTender 未安装")
        print("  2. BarTender 未正确激活")
        print("  3. 需要管理员权限")
        return
    except Exception as e:
        print(f"✗ 错误：{e}")
        return
    print()
    
    # 测试 3: 获取 BarTender 版本信息
    print("[测试 3] 获取 BarTender 版本信息...")
    try:
        # 尝试获取版本信息
        print("✓ BarTender 已连接")
        print(f"  提示：请手动在 BarTender 中查看版本")
    except Exception as e:
        print(f"  无法获取详细信息：{e}")
    print()
    
    # 测试 4: 打开模板文件（如果有参数）
    if len(sys.argv) > 1:
        template_path = sys.argv[1]
        print(f"[测试 4] 打开模板文件：{template_path}...")
        try:
            import os
            if not os.path.exists(template_path):
                print(f"✗ 文件不存在：{template_path}")
            else:
                print(f"✓ 文件存在")
                doc = app.Documents.Open(template_path, False, "", "")
                if doc:
                    print(f"✓ 模板打开成功")
                    
                    # 测试 5: 读取数据源
                    print("[测试 5] 读取数据源...")
                    sources = []
                    for obj in doc.Objects:
                        if hasattr(obj, 'DataSource') and obj.DataSource:
                            if hasattr(obj.DataSource, 'Name') and obj.DataSource.Name:
                                sources.append(obj.DataSource.Name)
                    
                    if sources:
                        print(f"✓ 找到 {len(sources)} 个数据源:")
                        for s in list(set(sources)):
                            print(f"   - {s}")
                    else:
                        print("⚠ 未找到命名的数据源")
                    
                    doc.Close(False)
                else:
                    print("✗ 无法打开模板")
        except pythoncom.com_error as e:
            print(f"✗ COM 错误：{e}")
            print(f"  错误代码：{e.hresult}")
        except Exception as e:
            print(f"✗ 错误：{e}")
        print()
    
    # 清理
    try:
        app.Quit()
    except:
        pass
    
    print("=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_bartender_connection()
