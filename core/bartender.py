"""
BarTender 自动化打印模块
支持 BarTender 2021 Automation API
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
            pythoncom.CoInitialize()
            self.app = win32com.client.Dispatch("BarTender.Application")
            self._initialized = True
            return True, "BarTender 初始化成功"
        except Exception as e:
            return False, f"BarTender 初始化失败：{str(e)}"
    
    def load_template(self) -> tuple:
        """
        加载模板文件
        
        Returns:
            (success: bool, message: str)
        """
        if not self._initialized:
            success, msg = self.initialize()
            if not success:
                return False, msg
        
        try:
            if not os.path.exists(self.template_path):
                return False, f"模板文件不存在：{self.template_path}"
            
            self.document = self.app.Documents.Open(self.template_path)
            return True, "模板加载成功"
        except Exception as e:
            return False, f"加载模板失败：{str(e)}"
    
    def get_data_sources(self) -> tuple:
        """
        获取模板中所有数据源名称
        
        Returns:
            (success: bool, data: list or message: str)
        """
        if not self.document:
            success, msg = self.load_template()
            if not success:
                return False, msg
        
        try:
            data_sources = []
            for obj in self.document.Objects:
                if obj.ObjectType == 1:  # btTextObject
                    data_source = obj.DataSource
                    if data_source and data_source.Name:
                        data_sources.append(data_source.Name)
            return True, list(set(data_sources))
        except Exception as e:
            return False, f"获取数据源失败：{str(e)}"
    
    def set_data_value(self, data_source_name: str, value: str) -> tuple:
        """
        设置数据源的值
        
        Args:
            data_source_name: 数据源名称
            value: 要设置的值
            
        Returns:
            (success: bool, message: str)
        """
        if not self.document:
            success, msg = self.load_template()
            if not success:
                return False, msg
        
        try:
            found = False
            for obj in self.document.Objects:
                if obj.ObjectType == 1:  # btTextObject
                    data_source = obj.DataSource
                    if data_source and data_source.Name == data_source_name:
                        data_source.Value = value
                        found = True
                        break
            
            if not found:
                return False, f"未找到数据源：{data_source_name}"
            
            return True, f"数据源 '{data_source_name}' 已更新"
        except Exception as e:
            return False, f"设置数据源失败：{str(e)}"
    
    def print_label(self, copies: int = 1) -> tuple:
        """
        打印标签
        
        Args:
            copies: 打印份数
            
        Returns:
            (success: bool, message: str)
        """
        if not self.document:
            return False, "模板未加载"
        
        try:
            self.document.Print(1, copies)
            return True, f"成功打印 {copies} 份标签"
        except Exception as e:
            return False, f"打印失败：{str(e)}"
    
    def close(self):
        """关闭文档和应用程序"""
        try:
            if self.document:
                self.document.Close(False)
                self.document = None
            if self.app:
                self.app.Quit()
                self.app = None
            self._initialized = False
        except Exception:
            pass
    
    def __enter__(self):
        """上下文管理器入口"""
        self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口"""
        self.close()
