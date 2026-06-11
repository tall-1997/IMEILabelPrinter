"""
打印录入页面 UI 组件
"""

import os
import re
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QSpinBox, QPushButton, QComboBox,
    QMessageBox, QGroupBox, QTextEdit, QFileDialog,
    QDialog, QDialogButtonBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDateEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QDate
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
        self.validation_excel_path = ""
        self.validation_data = set()
        
        self.init_ui()
        self.load_data_sources()
    
    def init_ui(self):
        """初始化 UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        if self.layout():
            while self.layout().count():
                item = self.layout().takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            self.setLayout(main_layout)
            main_layout = self.layout()
        
        main_layout.setAlignment(Qt.AlignTop)
        
        # Excel 文件选择区域
        excel_group = QGroupBox("校验数据源配置")
        excel_layout = QHBoxLayout()
        
        self.excel_path_label = QLabel("未选择文件")
        self.excel_path_label.setStyleSheet("color: #999;")
        
        self.select_excel_btn = QPushButton("选择 Excel 文件")
        self.select_excel_btn.clicked.connect(self.on_select_excel_clicked)
        
        self.load_excel_btn = QPushButton("加载数据")
        self.load_excel_btn.clicked.connect(self.on_load_excel_clicked)
        self.load_excel_btn.setEnabled(False)
        
        self.validation_status = QLabel("未校验")
        self.validation_status.setStyleSheet("color: #f44336; font-weight: bold;")
        
        excel_layout.addWidget(QLabel("文件:"))
        excel_layout.addWidget(self.excel_path_label, 1)
        excel_layout.addWidget(self.select_excel_btn)
        excel_layout.addWidget(self.load_excel_btn)
        excel_layout.addWidget(QLabel("状态:"))
        excel_layout.addWidget(self.validation_status)
        
        excel_group.setLayout(excel_layout)
        
        # 打印按钮区域（放在中间方便快速操作）
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        
        self.print_btn = QPushButton("打印标签")
        self.print_btn.setMinimumHeight(60)
        self.print_btn.setFont(QFont("Microsoft YaHei", 16, QFont.Bold))
        self.print_btn.clicked.connect(self.on_print_clicked)
        self.print_btn.setEnabled(False)
        
        self.preview_btn = QPushButton("查看数据")
        self.preview_btn.setMinimumHeight(60)
        self.preview_btn.clicked.connect(self.on_preview_excel_clicked)
        self.preview_btn.setEnabled(False)
        
        button_layout.addWidget(self.print_btn)
        button_layout.addWidget(self.preview_btn)
        
        # 状态显示区域
        status_group = QGroupBox("打印状态")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("就绪 - 请先选择并加载校验 Excel 文件")
        self.status_label.setFont(QFont("Microsoft YaHei", 12))
        self.status_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        self.log_text.setPlaceholderText("打印日志...")
        
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.log_text)
        status_group.setLayout(status_layout)
        
        main_layout.addWidget(excel_group)
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
    
    def on_select_excel_clicked(self):
        """选择 Excel 文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择校验 Excel 文件",
            "",
            "Excel 文件 (*.xlsx *.xls)"
        )
        
        if file_path:
            self.validation_excel_path = file_path
            self.excel_path_label.setText(os.path.basename(file_path))
            self.excel_path_label.setStyleSheet("color: #2196F3; font-weight: bold;")
            self.load_excel_btn.setEnabled(True)
            self.validation_data.clear()
            self.validation_status.setText("待加载")
            self.validation_status.setStyleSheet("color: #FF9800; font-weight: bold;")
            self.update_status("已选择文件，请点击加载数据", True)
            self.log_message(f"已选择校验文件：{file_path}")
    
    def on_load_excel_clicked(self):
        """加载 Excel 数据"""
        if not self.validation_excel_path:
            QMessageBox.warning(self, "错误", "请先选择 Excel 文件")
            return
        
        try:
            self.validation_status.setText("加载中...")
            self.validation_status.setStyleSheet("color: #2196F3; font-weight: bold;")
            
            from openpyxl import load_workbook
            wb = load_workbook(self.validation_excel_path, read_only=True)
            ws = wb.active
            
            self.validation_data.clear()
            count = 0
            
            for row in ws.iter_rows():
                for cell in row:
                    if cell.value:
                        value = str(cell.value).strip()
                        if self.validate_imei(value):
                            self.validation_data.add(value)
                            count += 1
            
            wb.close()
            
            if count > 0:
                self.validation_status.setText(f"已加载 {count} 条")
                self.validation_status.setStyleSheet("color: #4CAF50; font-weight: bold;")
                self.print_btn.setEnabled(True)
                self.preview_btn.setEnabled(True)
                self.update_status("就绪 - 可以点击打印", True)
                self.log_message(f"成功加载 {count} 条 IMEI 数据")
                QMessageBox.information(
                    self,
                    "加载成功",
                    f"成功加载 {count} 条 IMEI 数据\n\n"
                    f"只有完全匹配的 IMEI 才能打印"
                )
            else:
                self.validation_status.setText("无有效数据")
                self.validation_status.setStyleSheet("color: #f44336; font-weight: bold;")
                self.update_status("未找到有效的 15 位 IMEI 数据", False)
                self.log_message("未找到有效的 IMEI 数据")
                QMessageBox.warning(
                    self,
                    "警告",
                    "Excel 文件中未找到有效的 15 位 IMEI 数据\n\n"
                    "请确保文件中包含 15 位数字的 IMEI 号码"
                )
                
        except Exception as e:
            self.validation_status.setText("加载失败")
            self.validation_status.setStyleSheet("color: #f44336; font-weight: bold;")
            self.update_status(f"加载失败：{str(e)}", False)
            self.log_message(f"加载 Excel 失败：{str(e)}")
            QMessageBox.critical(self, "加载失败", f"无法加载 Excel 文件:\n{str(e)}")
    
    def on_preview_excel_clicked(self):
        """预览 Excel 数据"""
        if not self.validation_data:
            QMessageBox.information(self, "无数据", "没有可预览的数据")
            return
        
        dialog = ExcelPreviewDialog(self.validation_data, self)
        dialog.exec_()
    
    def on_print_clicked(self):
        """打印按钮点击事件"""
        # 弹出输入对话框
        dialog = IMEIInputDialog(self)
        if dialog.exec_() != QDialog.Accepted:
            return
        
        imei = dialog.get_imei().strip()
        
        if not self.validate_imei(imei):
            QMessageBox.warning(self, "验证失败", "请输入有效的 15 位 IMEI 号码")
            return
        
        # 校验是否在 Excel 中
        if self.validation_data and imei not in self.validation_data:
            QMessageBox.critical(
                self,
                "校验失败",
                f"IMEI {imei} 不在校验数据中！\n\n"
                f"请确保输入的 IMEI 与 Excel 文件中的数据完全匹配"
            )
            self.log_message(f"校验失败：IMEI {imei} 不在允许列表中")
            self.update_status("校验失败 - IMEI 不在允许列表中", False)
            return
        
        copies = dialog.get_copies()
        data_source = self.datasource_combo.currentText().strip()
        
        if not data_source:
            QMessageBox.warning(self, "验证失败", "请输入数据源名称")
            return
        
        import getpass
        operator = getpass.getuser()
        
        # 检查是否已打印
        exists, record = self.record_manager.check_imei_exists(imei)
        
        if exists:
            dialog_dup = DuplicatePrintDialog(imei, record, self)
            result = dialog_dup.exec_()
            
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
            
        except Exception as e:
            error_msg = str(e)
            self.log_message(f"打印失败：{error_msg}")
            self.update_status(f"打印失败：{error_msg}", False)
            QMessageBox.critical(self, "打印失败", f"打印过程中发生错误:\n{error_msg}")
        finally:
            self.print_btn.setEnabled(True)


class IMEIInputDialog(QDialog):
    """IMEI 输入对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("输入 IMEI 号码")
        self.setModal(True)
        self.resize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # IMEI 输入
        imei_group = QGroupBox("IMEI 信息")
        imei_form = QFormLayout()
        
        self.imei_input = QLineEdit()
        self.imei_input.setPlaceholderText("请输入或扫描 15 位 IMEI")
        self.imei_input.setFont(QFont("Consolas", 16))
        self.imei_input.setMaxLength(15)
        
        self.copies_spin = QSpinBox()
        self.copies_spin.setMinimum(1)
        self.copies_spin.setMaximum(999)
        self.copies_spin.setValue(1)
        self.copies_spin.setFont(QFont("Microsoft YaHei", 12))
        
        imei_form.addRow("IMEI 号码:", self.imei_input)
        imei_form.addRow("打印份数:", self.copies_spin)
        
        imei_group.setLayout(imei_form)
        
        # 提示信息
        info_label = QLabel("ℹ 只有 Excel 文件中完全匹配的 IMEI 才能打印")
        info_label.setStyleSheet("color: #2196F3; font-size: 12px;")
        info_label.setWordWrap(True)
        
        # 按钮
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Ok).setText("打印")
        button_box.button(QDialogButtonBox.Cancel).setText("取消")
        
        layout.addWidget(imei_group)
        layout.addWidget(info_label)
        layout.addWidget(button_box)
        
        self.setLayout(layout)
        self.imei_input.setFocus()
    
    def get_imei(self) -> str:
        """获取 IMEI"""
        return self.imei_input.text()
    
    def get_copies(self) -> int:
        """获取打印份数"""
        return self.copies_spin.value()


class ExcelPreviewDialog(QDialog):
    """Excel 数据预览对话框"""
    
    def __init__(self, data: set, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Excel 数据预览")
        self.setModal(True)
        self.resize(600, 500)
        self.data = data
        
        self.init_ui()
    
    def init_ui(self):
        """初始化 UI"""
        layout = QVBoxLayout()
        
        # 统计信息
        info_label = QLabel(f"共 {len(self.data)} 条 IMEI 数据")
        info_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        info_label.setStyleSheet("color: #2196F3;")
        
        # 数据表格
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["IMEI 号码"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        self.table.setAlternatingRowColors(True)
        
        # 加载数据（限制显示前 100 条）
        display_data = sorted(list(self.data))[:100]
        self.table.setRowCount(len(display_data))
        
        for i, imei in enumerate(display_data):
            self.table.setItem(i, 0, QTableWidgetItem(imei))
        
        # 提示
        if len(self.data) > 100:
            tip_label = QLabel(f"（仅显示前 100 条，共 {len(self.data)} 条）")
            tip_label.setStyleSheet("color: #999; font-size: 11px;")
            layout.addWidget(tip_label)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        
        layout.addWidget(info_label)
        layout.addWidget(self.table)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


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
