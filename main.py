"""
IMEI 标签打印系统 - 主程序入口
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from ui.main_window import MainWindow
from ui.print_tab import PrintTab
from ui.history_tab import HistoryTab
from ui.statistics_tab import StatisticsTab
from core.excel_manager import ExcelRecordManager


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    app.setFont(QFont("Microsoft YaHei", 10))
    app.setStyle("Fusion")
    
    app.setApplicationName("IMEI 标签打印系统")
    app.setOrganizationName("IMEILabelPrinter")
    
    # 获取程序所在目录
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 数据文件路径
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    excel_path = os.path.join(data_dir, "records.xlsx")
    
    # 模板文件路径
    templates_dir = os.path.join(base_dir, "templates")
    os.makedirs(templates_dir, exist_ok=True)
    template_path = os.path.join(templates_dir, "imei_label.btw")
    
    # 检查模板文件是否存在
    if not os.path.exists(template_path):
        QMessageBox.warning(
            None,
            "模板文件缺失",
            f"未找到 BarTender 模板文件:\n{template_path}\n\n"
            f"请将您的 BarTender 模板文件复制到此位置，\n"
            f"或创建一个名为 imei_label.btw 的模板。"
        )
    
    # 初始化记录管理器
    record_manager = ExcelRecordManager(excel_path)
    
    # 创建主窗口
    window = MainWindow()
    
    # 添加打印标签页
    print_tab = PrintTab(record_manager, template_path)
    window.add_page(print_tab, "打印录入", "print")
    
    # 添加历史查询标签页
    history_tab = HistoryTab(record_manager)
    window.add_page(history_tab, "历史查询", "history")
    
    # 添加统计报表标签页
    statistics_tab = StatisticsTab(record_manager)
    window.add_page(statistics_tab, "统计报表", "statistics")
    
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
