"""
主窗口 UI 组件
"""

import sys
import os
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("IMEI 标签打印系统")
        self.setMinimumSize(1024, 768)
        self.setStyleSheet(self._get_stylesheet())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Microsoft YaHei", 10))
        self.main_layout.addWidget(self.tab_widget)
        
        self.pages = {}
    
    def add_page(self, page: QWidget, title: str, key: str):
        """
        添加标签页
        
        Args:
            page: 页面组件
            title: 标签标题
            key: 页面标识符
        """
        self.tab_widget.addTab(page, title)
        self.pages[key] = page
    
    def get_page(self, key: str) -> Optional[QWidget]:
        """获取页面组件"""
        return self.pages.get(key)
    
    def _get_stylesheet(self) -> str:
        """获取样式表"""
        return """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #d0d0d0;
            background: white;
            border-radius: 5px;
        }
        QTabBar::tab {
            background: #e0e0e0;
            color: #333;
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 5px;
            border-top-right-radius: 5px;
        }
        QTabBar::tab:selected {
            background: white;
            border-bottom: 2px solid #2196F3;
        }
        QTabBar::tab:hover:!selected {
            background: #f0f0f0;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QPushButton:disabled {
            background-color: #BDBDBD;
        }
        QLineEdit, QComboBox, QSpinBox, QDateEdit {
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 8px;
            font-size: 14px;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {
            border: 2px solid #2196F3;
        }
        QTableWidget {
            border: 1px solid #d0d0d0;
            border-radius: 5px;
            gridline-color: #e0e0e0;
        }
        QTableWidget::item {
            padding: 8px;
        }
        QTableWidget::item:selected {
            background-color: #2196F3;
            color: white;
        }
        QHeaderView::section {
            background: #f5f5f5;
            padding: 8px;
            border: none;
            font-weight: bold;
        }
        QGroupBox {
            border: 1px solid #d0d0d0;
            border-radius: 5px;
            margin-top: 15px;
            padding-top: 15px;
            font-weight: bold;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 10px;
            color: #2196F3;
        }
        QLabel {
            color: #333;
            font-size: 14px;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
