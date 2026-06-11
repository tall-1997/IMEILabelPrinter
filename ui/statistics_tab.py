"""
统计报表页面 UI 组件
"""

from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QPushButton, QComboBox, QGroupBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class StatisticsTab(QWidget):
    """统计报表标签页"""
    
    def __init__(self, record_manager):
        super().__init__()
        
        self.record_manager = record_manager
        self.current_stats = []
        
        self.init_ui()
        self.load_statistics("day")
    
    def init_ui(self):
        """初始化 UI"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        
        # 统计图区域（使用 matplotlib 嵌入）
        chart_group = QGroupBox("统计图表")
        chart_layout = QVBoxLayout()
        
        # 统计类型选择
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("统计维度:"))
        
        self.stat_type_combo = QComboBox()
        self.stat_type_combo.addItem("按日统计", "day")
        self.stat_type_combo.addItem("按月统计", "month")
        self.stat_type_combo.addItem("按操作员统计", "operator")
        self.stat_type_combo.currentTextChanged.connect(self.on_stat_type_changed)
        
        type_layout.addWidget(self.stat_type_combo)
        type_layout.addStretch()
        
        self.refresh_btn = QPushButton("刷新统计")
        self.refresh_btn.clicked.connect(self.refresh_statistics)
        type_layout.addWidget(self.refresh_btn)
        
        # 使用 QLabel 显示统计图表
        self.chart_label = QLabel()
        self.chart_label.setAlignment(Qt.AlignCenter)
        self.chart_label.setMinimumHeight(400)
        self.chart_label.setStyleSheet(
            "background: white; border: 1px solid #d0d0d0; border-radius: 5px;"
        )
        self.chart_label.setText("图表生成中...")
        
        chart_layout.addLayout(type_layout)
        chart_layout.addWidget(self.chart_label)
        chart_group.setLayout(chart_layout)
        
        # 统计表格区域
        table_group = QGroupBox("统计数据")
        table_layout = QVBoxLayout()
        
        self.stat_table = QTableWidget()
        self.stat_table.setColumnCount(3)
        self.stat_table.setHorizontalHeaderLabels([
            "日期/操作员", "打印次数", "总份数"
        ])
        
        header = self.stat_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.stat_table.setAlternatingRowColors(True)
        
        table_layout.addWidget(self.stat_table)
        table_group.setLayout(table_layout)
        
        # 汇总信息
        summary_group = QGroupBox("汇总信息")
        summary_layout = QHBoxLayout()
        
        self.total_labels_label = QLabel("总打印次数：0")
        self.total_labels_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.total_labels_label.setStyleSheet("color: #2196F3;")
        
        self.total_copies_label = QLabel("总打印份数：0")
        self.total_copies_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.total_copies_label.setStyleSheet("color: #4CAF50;")
        
        self.avg_daily_label = QLabel("日均打印：0")
        self.avg_daily_label.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        self.avg_daily_label.setStyleSheet("color: #FF9800;")
        
        summary_layout.addWidget(self.total_labels_label)
        summary_layout.addWidget(self.total_copies_label)
        summary_layout.addWidget(self.avg_daily_label)
        summary_layout.addStretch()
        
        summary_group.setLayout(summary_layout)
        
        main_layout.addWidget(chart_group)
        main_layout.addWidget(table_group)
        main_layout.addWidget(summary_group)
        
        self.setLayout(main_layout)
    
    def on_stat_type_changed(self):
        """统计类型改变时刷新"""
        index = self.stat_type_combo.currentIndex()
        group_by = self.stat_type_combo.itemData(index)
        self.load_statistics(group_by)
    
    def refresh_statistics(self):
        """刷新统计"""
        self.refresh_statistics()
    
    def load_statistics(self, group_by: str):
        """加载统计数据"""
        self.current_stats = self.record_manager.get_statistics(group_by)
        
        # 更新表格
        self.stat_table.setRowCount(0)
        total_count = 0
        total_copies = 0
        
        for stat in self.current_stats:
            row = self.stat_table.rowCount()
            self.stat_table.insertRow(row)
            
            date_or_operator = stat.get("date") or stat.get("operator", "")
            count = stat.get("count", 0)
            copies = stat.get("total_copies", 0)
            
            self.stat_table.setItem(row, 0, QTableWidgetItem(date_or_operator))
            self.stat_table.setItem(row, 1, QTableWidgetItem(str(count)))
            self.stat_table.setItem(row, 2, QTableWidgetItem(str(copies)))
            
            total_count += count
            total_copies += copies
        
        # 更新汇总信息
        self.total_labels_label.setText(f"总打印次数：{total_count}")
        self.total_copies_label.setText(f"总打印份数：{total_copies}")
        
        if group_by == "day" and self.current_stats:
            avg_daily = total_count / len(self.current_stats)
            self.avg_daily_label.setText(f"日均打印：{avg_daily:.1f}")
        else:
            self.avg_daily_label.setText("日均打印：N/A")
        
        # 生成图表
        self.generate_chart(group_by)
    
    def generate_chart(self, group_by: str):
        """生成统计图表"""
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
            import io
            from PyQt5.QtGui import QPixmap
            
            if not self.current_stats:
                self.chart_label.setText("暂无数据")
                return
            
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if group_by in ["day", "month"]:
                labels = [s.get("date", "") for s in self.current_stats]
            else:
                labels = [s.get("operator", "") for s in self.current_stats]
            
            counts = [s.get("count", 0) for s in self.current_stats]
            copies = [s.get("total_copies", 0) for s in self.current_stats]
            
            x = range(len(labels))
            width = 0.35
            
            ax.bar([i - width/2 for i in x], counts, width, label="打印次数", color="#2196F3")
            ax.bar([i + width/2 for i in x], copies, width, label="总份数", color="#4CAF50")
            
            ax.set_xlabel("日期" if group_by in ["day", "month"] else "操作员")
            ax.set_ylabel("数量")
            ax.set_title("打印统计报表")
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha="right")
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buf = io.BytesIO()
            plt.savefig(buf, format="png", dpi=100)
            buf.seek(0)
            plt.close(fig)
            
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            
            scaled_pixmap = pixmap.scaled(
                self.chart_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.chart_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.chart_label.setText(f"图表生成失败：{str(e)}")
    
    def resizeEvent(self, event):
        """窗口大小改变时重新生成图表"""
        super().resizeEvent(event)
        if self.current_stats:
            index = self.stat_type_combo.currentIndex()
            group_by = self.stat_type_combo.itemData(index)
            self.generate_chart(group_by)


from PyQt5.QtWidgets import QTableWidget, QHeaderView, QMessageBox


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    from core.excel_manager import ExcelRecordManager
    
    record_manager = ExcelRecordManager("data/records.xlsx")
    stats = StatisticsTab(record_manager)
    stats.show()
    sys.exit(app.exec_())
