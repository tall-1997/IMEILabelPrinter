"""
打印录入页面 UI 组件
"""

import os
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QSpinBox, QPushButton, QComboBox,
    QMessageBox, QGroupBox, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class PrintTab(QWidget):
    """打印录入标签页"""
    
    print_success = pyqtSignal(str)
    
    def __init__(self, record_manager, template_path: str):
        super().__init__()
        
        self.record_manager = record_manager
        self.template_path = template_path
        self.bartender = None
        self.data_sources = []
        
        self.init_ui()
        self.load_data_sources()
    
    def init_ui(self):
        """初始化 UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        self.layout().setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignTop)
        
        # IMEI 输入区域
        imei_group = QGroupBox("IMEI 信息录入")
        imei_layout = QFormLayout()
        imei_layout.setSpacing(10)
        
        # IMEI 输入框 (支持扫码枪)
        self.imei_input = QLineEdit()
        self.imei_input.setPlaceholderText("请输入或扫描 IMEI (15 位数字)")
        self.imei_input.setFont(QFont("Consolas", 14))
        self.imei_input.setMaxLength(15)
        self.imei_input.returnPressed.connect(self.on_print_clicked)
        
        # 数据源名称配置
        self.datasource_combo = QComboBox()
        self.datasource_combo.setEditable(True)
        self.datasource_combo.setMinimumWidth(200)
        self.datasource_combo.addItem("IMEI1")
        
        # 打印份数
        self.copies_spin = QSpinBox()
        self.copies_spin.setMinimum(1)
        self.copies_spin.setMaximum(999)
        self.copies_spin.setValue(1)
        
        imei_layout.addRow("IMEI 号码:", self.imei_input)
        imei_layout.addRow("数据源名称:", self.datasource_combo)
        imei_layout.addRow("打印份数:", self.copies_spin)
        
        imei_group.setLayout(imei_layout)
        
        # 打印按钮区域
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.print_btn = QPushButton("打印标签")
        self.print_btn.setMinimumHeight(50)
        self.print_btn.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.print_btn.clicked.connect(self.on_print_clicked)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setMinimumHeight(50)
        self.clear_btn.clicked.connect(self.clear_input)
        
        button_layout.addWidget(self.print_btn)
        button_layout.addWidget(self.clear_btn)
        
        # 状态显示区域
        status_group = QGroupBox("打印状态")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("就绪")
        self.status_label.setFont(QFont("Microsoft YaHei", 12))
        self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setPlaceholderText("打印日志...")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.log_text)
        status_group.setLayout(status_layout)
        
        main_layout.addWidget(imei_group)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(status_group)
    
    def load_data_sources(self):
        """加载模板数据源"""
        try:
            from core.bartender import BarTenderPrinter
            
            self.bartender = BarTenderPrinter(self.template_path)
            success, result = self.bartender.load_template()
            
            if success:
                success, data_sources = self.bartender.get_data_sources()
                if success and data_sources:
                    self.data_sources = data_sources
                    self.datasource_combo.clear()
                    for ds in data_sources:
                        self.datasource_combo.addItem(ds)
                    self.log_message(f"已加载 {len(data_sources)} 个数据源")
                else:
                    self.log_message("未找到数据源，使用默认配置")
            else:
                self.log_message(f"模板加载失败：{result}")
        except Exception as e:
            self.log_message(f"初始化失败：{str(e)}")
    
    def validate_imei(self, imei: str) -> bool:
        """验证 IMEI 格式"""
        if not imei:
            return False
        pattern = r'^\d{15}$'
        return bool(re.match(pattern, imei.strip()))
    
    def log_message(self, message: str):
        """记录日志"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
    
    def update_status(self, status: str, success: bool = True):
        """更新状态显示"""
        self.status_label.setText(status)
        if success:
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #f44336; font-weight: bold;")
    
    def clear_input(self):
        """清空输入"""
        self.imei_input.clear()
        self.imei_input.setFocus()
        self.update_status("就绪", True)
    
    def on_print_clicked(self):
        """打印按钮点击事件"""
        imei = self.imei_input.text().strip()
        
        if not self.validate_imei(imei):
            QMessageBox.warning(self, "验证失败", "请输入有效的 15 位 IMEI 号码")
            return
        
        copies = self.copies_spin.value()
        data_source = self.datasource_combo.currentText().strip()
        
        if not data_source:
            QMessageBox.warning(self, "验证失败", "请输入数据源名称")
            return
        
        import getpass
        operator = getpass.getuser()
        
        # 检查是否已打印
        exists, record = self.record_manager.check_imei_exists(imei)
        
        if exists:
            dialog = DuplicatePrintDialog(imei, record, self)
            result = dialog.exec_()
            
            if result == QDialog.Rejected:
                self.update_status("已取消打印", False)
                self.log_message(f"用户取消打印已存在的 IMEI: {imei}")
                return
        
        # 执行打印
        self.update_status("正在打印...", True)
        self.print_btn.setEnabled(False)
        
        try:
            if not self.bartender:
                self.load_data_sources()
            
            success, msg = self.bartender.set_data_value(data_source, imei)
            if not success:
                raise Exception(msg)
            
            success, msg = self.bartender.print_label(copies)
            if not success:
                raise Exception(msg)
            
            self.record_manager.add_record(imei, copies, operator)
            
            self.log_message(f"打印成功：IMEI={imei}, 份数={copies}")
            self.update_status(f"打印成功！已打印 {copies} 份", True)
            self.print_success.emit(imei)
            
            QMessageBox.information(self, "打印成功", f"标签已成功打印 {copies} 份！")
            
            self.clear_input()
            
        except Exception as e:
            error_msg = str(e)
            self.log_message(f"打印失败：{error_msg}")
            self.update_status(f"打印失败：{error_msg}", False)
            QMessageBox.critical(self, "打印失败", f"打印过程中发生错误:\n{error_msg}")
        finally:
            self.print_btn.setEnabled(True)


class DuplicatePrintDialog(QMessageBox):
    """重复打印确认对话框"""
    
    def __init__(self, imei: str, record: dict, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("重复打印警告")
        self.setIcon(QMessageBox.Warning)
        
        print_time = record.get("print_time", "未知")
        copies = record.get("copies", 0)
        operator = record.get("operator", "未知")
        
        message = (
            f"IMEI {imei} 已打印过！\n\n"
            f"上次打印时间：{print_time}\n"
            f"上次打印份数：{copies}\n"
            f"操作员：{operator}\n\n"
            f"是否继续打印？"
        )
        
        self.setText(message)
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.button(QMessageBox.Yes).setText("继续打印")
        self.button(QMessageBox.No).setText("放弃打印")
        self.setDefaultButton(QMessageBox.No)


from PyQt5.QtWidgets import QDialog


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    from core.excel_manager import ExcelRecordManager
    
    record_manager = ExcelRecordManager("data/records.xlsx")
    template = PrintTab(record_manager, "templates/sample.btw")
    template.show()
    sys.exit(app.exec_())
