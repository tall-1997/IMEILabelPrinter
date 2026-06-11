"""
历史查询页面 UI 组件
"""

from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QDateEdit, QLineEdit, QFileDialog, QGroupBox, QHeaderView
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont


class HistoryTab(QWidget):
    """历史查询标签页"""
    
    def __init__(self, record_manager):
        super().__init__()
        
        self.record_manager = record_manager
        self.current_records = []
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """初始化 UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 筛选条件区域
        filter_group = QGroupBox("筛选条件")
        filter_layout = QFormLayout()
        filter_layout.setSpacing(10)
        
        # 日期范围筛选
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setDateRange(QDate(2020, 1, 1), QDate.currentDate())
        
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setDateRange(QDate(2020, 1, 1), QDate.currentDate())
        
        # IMEI 关键字搜索
        self.imei_search = QLineEdit()
        self.imei_search.setPlaceholderText("输入 IMEI 关键字搜索")
        
        # 筛选按钮
        self.search_btn = QPushButton("查询")
        self.search_btn.clicked.connect(self.load_data)
        
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_filters)
        
        filter_row = QHBoxLayout()
        filter_row.addWidget(QLabel("开始日期:"))
        filter_row.addWidget(self.start_date)
        filter_row.addWidget(QLabel("结束日期:"))
        filter_row.addWidget(self.end_date)
        filter_row.addWidget(QLabel("IMEI:"))
        filter_row.addWidget(self.imei_search, 1)
        filter_row.addWidget(self.search_btn)
        filter_row.addWidget(self.reset_btn)
        
        filter_layout.addRow(filter_row)
        filter_group.setLayout(filter_layout)
        
        # 数据表格区域
        table_group = QGroupBox("打印记录")
        table_layout = QVBoxLayout()
        
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(5)
        self.record_table.setHorizontalHeaderLabels([
            "IMEI", "打印时间", "份数", "操作员", "备注"
        ])
        
        header = self.record_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        self.record_table.setAlternatingRowColors(True)
        self.record_table.setStyleSheet(
            "QTableWidget::item { padding: 8px; }"
        )
        
        table_layout.addWidget(self.record_table)
        table_group.setLayout(table_layout)
        
        # 导出按钮
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        self.export_btn = QPushButton("导出 Excel")
        self.export_btn.clicked.connect(self.export_data)
        
        export_layout.addWidget(self.export_btn)
        
        # 统计信息
        self.info_label = QLabel("")
        self.info_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        export_layout.addWidget(self.info_label)
        
        main_layout.addWidget(filter_group)
        main_layout.addWidget(table_group)
        main_layout.addLayout(export_layout)
        
        self.setLayout(main_layout)
    
    def reset_filters(self):
        """重置筛选条件"""
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.end_date.setDate(QDate.currentDate())
        self.imei_search.clear()
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        start_date = self.start_date.date().toString("yyyy-MM-dd")
        end_date = self.end_date.date().toString("yyyy-MM-dd")
        imei_keyword = self.imei_search.text().strip()
        
        self.current_records = self.record_manager.get_records(
            start_date=start_date,
            end_date=end_date,
            imei_keyword=imei_keyword
        )
        
        self.record_table.setRowCount(0)
        
        for record in self.current_records:
            row = self.record_table.rowCount()
            self.record_table.insertRow(row)
            
            self.record_table.setItem(row, 0, QTableWidgetItem(record["imei"]))
            self.record_table.setItem(row, 1, QTableWidgetItem(record["print_time"]))
            self.record_table.setItem(row, 2, QTableWidgetItem(str(record["copies"])))
            self.record_table.setItem(row, 3, QTableWidgetItem(record["operator"]))
            self.record_table.setItem(row, 4, QTableWidgetItem(record["note"]))
        
        total_records = len(self.current_records)
        total_copies = sum(r["copies"] for r in self.current_records)
        self.info_label.setText(
            f"共 {total_records} 条记录，总计 {total_copies} 份标签"
        )
    
    def export_data(self):
        """导出数据到 Excel"""
        if not self.current_records:
            QMessageBox.warning(self, "无数据", "没有可导出的记录")
            return
        
        from PyQt5.QtWidgets import QMessageBox
        
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出 Excel",
            f"打印记录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "Excel 文件 (*.xlsx)"
        )
        
        if file_path:
            success, msg = self.record_manager.export_to_excel(file_path, self.current_records)
            if success:
                QMessageBox.information(self, "导出成功", f"数据已导出到:\n{file_path}")
            else:
                QMessageBox.critical(self, "导出失败", f"导出失败:\n{msg}")


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    from core.excel_manager import ExcelRecordManager
    
    record_manager = ExcelRecordManager("data/records.xlsx")
    history = HistoryTab(record_manager)
    history.show()
    sys.exit(app.exec_())
