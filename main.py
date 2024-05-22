import faulthandler
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app.main_window import MainWindow
from app.module.config import cfg

# 将当前工作目录设置为程序所在的目录，确保无论从哪里执行，其工作目录都正确设置为程序本身的位置，避免路径错误。
os.chdir(
    os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__)))


def clear_last_cache():
    for root, dirs, files in os.walk(cfg.get(cfg.cacheFolder)):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                os.remove(file_path)


# 启用 DPI 缩放
if cfg.get(cfg.dpiScale) == "Auto":
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
else:
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

if __name__ == "__main__":
    faulthandler.enable()
    clear_last_cache()
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
    w = MainWindow()
    sys.exit(app.exec_())
