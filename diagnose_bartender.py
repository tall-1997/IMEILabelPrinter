"""
BarTender 2022 COM 接口诊断工具
测试并显示 BarTender 对象模型结构
"""

import sys
import pythoncom
import win32com.client


def diagnose_bartender():
    """诊断 BarTender COM 接口"""
    print("=" * 70)
    print("BarTender 2022 COM 接口诊断工具")
    print("=" * 70)
    print()
    
    # 步骤 1: 初始化 COM
    print("[步骤 1] 初始化 COM...")
    try:
        pythoncom.CoInitialize()
        print("✓ COM 初始化成功")
    except Exception as e:
        print(f"✗ COM 初始化失败：{e}")
        return False
    print()
    
    # 步骤 2: 创建 BarTender 应用程序对象
    print("[步骤 2] 创建 BarTender.Application 对象...")
    try:
        app = win32com.client.Dispatch("BarTender.Application")
        print("✓ BarTender 应用程序对象创建成功")
        print(f"  ProgID: BarTender.Application")
        print(f"  对象类型：{type(app)}")
    except Exception as e:
        print(f"✗ 创建失败：{e}")
        print("\n可能原因：")
        print("  1. BarTender 未安装")
        print("  2. BarTender 未激活")
        print("  3. 需要管理员权限")
        return False
    print()
    
    # 步骤 3: 检查 Documents 属性
    print("[步骤 3] 检查 Documents 属性...")
    try:
        # 方法 1: 直接访问 Documents
        try:
            documents = app.Documents
            print(f"✓ 成功访问 Documents 属性")
            print(f"  类型：{type(documents)}")
            print(f"  文档数量：{documents.Count if hasattr(documents, 'Count') else 'N/A'}")
        except AttributeError as e:
            print(f"✗ Documents 属性不存在：{e}")
            # 尝试其他可能的属性名
            print("\n尝试其他可能的属性名：")
            for attr in ['Documents', 'documents', 'Document', 'document', 'Files', 'Templates']:
                if hasattr(app, attr):
                    print(f"  ✓ 找到属性：{attr}")
                else:
                    print(f"  ✗ 未找到：{attr}")
    except Exception as e:
        print(f"✗ 检查失败：{e}")
    print()
    
    # 步骤 4: 列出应用程序的所有属性和方法
    print("[步骤 4] BarTender.Application 对象的方法和属性：")
    methods = []
    properties = []
    try:
        for item in dir(app):
            if not item.startswith('_'):
                try:
                    attr = getattr(app, item)
                    if callable(attr):
                        methods.append(item)
                    else:
                        properties.append(item)
                except:
                    pass
        
        print(f"  属性 ({len(properties)}): {', '.join(properties[:20])}")
        if len(properties) > 20:
            print(f"           ... 还有 {len(properties)-20} 个")
        print(f"  方法 ({len(methods)}): {', '.join(methods[:20])}")
        if len(methods) > 20:
            print(f"           ... 还有 {len(methods)-20} 个")
    except Exception as e:
        print(f"  无法列出：{e}")
    print()
    
    # 步骤 5: 测试打开模板（如果有参数）
    if len(sys.argv) > 1:
        template_path = sys.argv[1]
        print(f"[步骤 5] 测试打开模板：{template_path}")
        import os
        if not os.path.exists(template_path):
            print(f"  ✗ 文件不存在")
        else:
            print(f"  ✓ 文件存在")
            try:
                # 尝试不同的打开方式
                print("\n  尝试方式 1: Documents.Open()")
                try:
                    doc = app.Documents.Open(template_path)
                    print(f"  ✓ 成功打开")
                    
                    # 检查对象属性
                    print(f"    对象类型：{type(doc)}")
                    print(f"    可用属性：{[a for a in dir(doc) if not a.startswith('_')][:10]}")
                    
                    doc.Close(False)
                except Exception as e:
                    print(f"  ✗ 失败：{e}")
                
                print("\n  尝试方式 2: Open()")
                try:
                    doc = app.Open(template_path)
                    print(f"  ✓ 成功打开")
                    doc.Close(False)
                except Exception as e:
                    print(f"  ✗ 失败：{e}")
                    
            except Exception as e:
                print(f"  ✗ 错误：{e}")
        print()
    
    # 步骤 6: BarTender 版本信息
    print("[步骤 6] BarTender 版本信息:")
    try:
        # 尝试获取版本
        print(f"  提示：请在 BarTender 中查看「帮助」→「关于」")
        print(f"  或使用命令：BarTender.exe /?")
    except:
        pass
    print()
    
    # 清理
    try:
        app.Quit()
    except:
        pass
    
    print("=" * 70)
    print("诊断完成！")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    diagnose_bartender()
