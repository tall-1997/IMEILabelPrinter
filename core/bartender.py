"""
BarTender 自动化打印模块
支持 BarTender 2021/2022 Automation API
"""

import os
import sys
import pythoncom
import win32com.client


class BarTenderPrinter:
    """BarTender 打印控制器"""
    
    def __init__(self, template_path: str):
        """
        初始化 BarTender 打印机
        
        Args:
            template_path: BarTender 模板文件路径 (.btw)
        """
        self.template_path = os.path.abspath(template_path)
        self.app = None
        self.document = None
        self._initialized = False
    
    def initialize(self):
        """初始化 BarTender COM 对象"""
        try:
            # 确保 COM 初始化
            pythoncom.CoInitialize()
            
            # 尝试创建 BarTender 应用程序对象
            # BarTender 2022 使用相同的 ProgID
            self.app = win32com.client.Dispatch("BarTender.Application")
            
            if not self.app:
                return False, "无法创建 BarTender 应用程序对象，请确认 BarTender 已正确安装"
            
            self._initialized = True
            return True, "BarTender 初始化成功"
            
        except pythoncom.com_error as e:
            error_code = e.hresult if hasattr(e, 'hresult') else 'unknown'
            return False, f"COM 错误 (代码：{error_code}): BarTender 可能未安装、未激活，或版本不兼容"
        except Exception as e:
            return False, f"BarTender 初始化失败：{str(e)}"
    
    def load_template(self, silent=False):
        """
        加载模板文件
        
        Args:
            silent: 是否静默模式（不显示错误弹窗）
            
        Returns:
            (success: bool, message: str)
        """
        if not self._initialized:
            success, msg = self.initialize()
            if not success:
                return False, msg
        
        # 检查文件是否存在
        if not os.path.exists(self.template_path):
            return False, f"模板文件不存在:\n\n{self.template_path}\n\n请检查文件路径是否正确。"
        
        try:
            # BarTender 2022 使用 Documents.Open 方法
            # 先尝试直接访问 Documents 属性
            try:
                documents = self.app.Documents
            except AttributeError:
                # 如果 Documents 不是直接属性，尝试通过其他方式访问
                return False, "BarTender 对象模型不兼容：\n\n无法访问 Documents 集合。\n\n可能原因：\n1. BarTender 版本不兼容\n2. BarTender 未完全启动\n3. COM 接口访问权限问题\n\n建议：\n- 确保 BarTender 2021 或 2022 已安装\n- 以管理员身份运行本程序\n- 先手动打开 BarTender 软件"
            
            # 打开模板文件
            # 参数：FileName, ReadOnly, PasswordDocument, PasswordTemplate
            self.document = documents.Open(self.template_path, False, "", "")
            
            if not self.document:
                return False, f"无法打开模板文件:\n\n{self.template_path}\n\n文件可能已损坏或格式不正确。"
            
            return True, "模板加载成功"
            
        except pythoncom.com_error as e:
            error_code = e.hresult if hasattr(e, 'hresult') else 'unknown'
            error_msg = self._parse_bartender_error(error_code)
            return False, f"BarTender 打开模板失败 ({error_code}):\n\n{error_msg}\n\n文件：{self.template_path}\n\n建议：\n1. 在 BarTender 中直接打开此模板确认是否正常\n2. 检查模板是否与当前 BarTender 版本兼容\n3. 确保模板文件未被其他程序占用"
        except Exception as e:
            return False, f"加载模板失败：{str(e)}\n\n文件：{self.template_path}"
    
    def _parse_bartender_error(self, error_code):
        """解析 BarTender COM 错误代码"""
        error_messages = {
            -2147417848: "对象不存在或已释放",
            -2147467259: "文件不存在或路径无效",
            -2147221022: " BarTender 服务未响应",
            -2147352567: "访问被拒绝（权限问题）",
            'unknown': "未知 COM 错误，可能是 BarTender 未响应或模板文件损坏"
        }
        return error_messages.get(error_code, f"COM 错误代码：{error_code}")
    
    def get_data_sources(self):
        """
        获取模板中所有数据源名称
        
        Returns:
            (success: bool, data: list or message: str)
        """
        if not self.document:
            return False, "模板未加载"
        
        try:
            data_sources = []
            
            # 遍历所有对象
            for obj in self.document.Objects:
                try:
                    # 检查对象类型和数据源
                    if hasattr(obj, 'DataSource') and obj.DataSource:
                        if hasattr(obj.DataSource, 'Name') and obj.DataSource.Name:
                            data_sources.append(str(obj.DataSource.Name))
                except:
                    # 忽略无法访问的对象
                    continue
            
            # 去重
            unique_sources = list(set(data_sources))
            
            if not unique_sources:
                return False, "未在模板中找到命名的数据源。请检查：\n1. 文本对象是否设置了数据源\n2. 数据源是否有名称\n3. 在 BarTender 中双击文本对象，在「数据源」选项卡中确认"
            
            return True, unique_sources
            
        except pythoncom.com_error as e:
            error_code = e.hresult if hasattr(e, 'hresult') else 'unknown'
            return False, f"获取数据源时发生 COM 错误 ({error_code})"
        except Exception as e:
            return False, f"获取数据源失败：{str(e)}"
    
    def set_data_value(self, data_source_name: str, value: str):
        """
        设置数据源的值
        
        Args:
            data_source_name: 数据源名称
            value: 要设置的值
            
        Returns:
            (success: bool, message: str)
        """
        if not self.document:
            return False, "模板未加载，请先加载模板"
        
        try:
            found = False
            
            # 遍历所有对象查找匹配的数据源
            for obj in self.document.Objects:
                try:
                    if hasattr(obj, 'DataSource') and obj.DataSource:
                        if hasattr(obj.DataSource, 'Name') and str(obj.DataSource.Name) == data_source_name:
                            # 设置数据源值
                            obj.DataSource.Value = value
                            found = True
                            break
                except:
                    continue
            
            if not found:
                available = []
                for obj in self.document.Objects:
                    try:
                        if hasattr(obj, 'DataSource') and obj.DataSource and hasattr(obj.DataSource, 'Name'):
                            available.append(str(obj.DataSource.Name))
                    except:
                        pass
                
                return False, f"未找到数据源 '{data_source_name}'\n\n可用的数据源:\n" + "\n".join(available) if available else "（无命名数据源）"
            
            return True, f"数据源 '{data_source_name}' 已更新为 '{value}'"
            
        except pythoncom.com_error as e:
            error_code = e.hresult if hasattr(e, 'hresult') else 'unknown'
            return False, f"设置数据源时发生 COM 错误 ({error_code})"
        except Exception as e:
            return False, f"设置数据源失败：{str(e)}"
    
    def print_label(self, copies: int = 1):
        """
        打印标签
        
        Args:
            copies: 打印份数
            
        Returns:
            (success: bool, message: str)
        """
        if not self.document:
            return False, "模板未加载，无法打印"
        
        try:
            # 使用 Print 方法
            # 参数：PrinterName, StartPosition, EndPosition, PrimaryIndexes, SecondaryIndexes, CopyNumber, DocumentRevision, Option
            self.document.Print("", 1, copies)
            return True, f"成功打印 {copies} 份标签"
            
        except pythoncom.com_error as e:
            error_code = e.hresult if hasattr(e, 'hresult') else 'unknown'
            return False, f"打印时发生 COM 错误 ({error_code}): 请检查打印机连接和 BarTender 状态"
        except Exception as e:
            return False, f"打印失败：{str(e)}"
    
    def close(self):
        """关闭文档和应用程序"""
        try:
            if self.document:
                self.document.Close(False)  # False = 不保存更改
                self.document = None
            if self.app:
                self.app.Quit()
                self.app = None
            self._initialized = False
        except Exception:
            pass
    
    def __del__(self):
        """析构函数，确保资源释放"""
        self.close()
    
    def __enter__(self):
        """上下文管理器入口"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
