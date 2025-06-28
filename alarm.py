import os
import sys
import platform
import subprocess
from datetime import datetime, timedelta


# ==================== PyQt5 安装检查 ====================
def check_and_install_pyqt5():
    """检查并安装 PyQt5"""
    try:
        from PyQt5.QtWidgets import QApplication
        print("PyQt5 已安装")
        return True
    except ImportError:
        print("PyQt5 未安装，尝试自动安装...")

        # 获取 pip 可执行文件路径
        pip_executable = sys.executable.replace("python.exe", "pip.exe")
        if not os.path.exists(pip_executable):
            pip_executable = sys.executable.replace("pythonw.exe", "pip.exe")

        # 尝试安装 PyQt5
        try:
            result = subprocess.run(
                [pip_executable, "install", "PyQt5"],
                capture_output=True,
                text=True,
                check=True
            )
            print("PyQt5 安装成功!")
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"安装失败: {e}")
            print("错误输出:")
            print(e.stderr)
            print("\n请手动安装 PyQt5:")
            print(f"1. 打开 PyCharm 终端")
            print(f"2. 运行: pip install PyQt5")
            return False


# 检查并安装 PyQt5
if not check_and_install_pyqt5():
    print("无法继续运行，请手动安装 PyQt5")
    sys.exit(1)


# ==================== 修复 DLL 问题 ====================
def fix_pyqt5_dll_issue():
    """修复可能的 DLL 加载问题"""
    try:
        # 获取当前 Python 解释器路径
        python_dir = os.path.dirname(sys.executable)

        # 尝试设置插件路径
        possible_paths = [
            os.path.join(python_dir, "Lib", "site-packages", "PyQt5", "Qt5", "plugins"),
            os.path.join(python_dir, "Lib", "site-packages", "PyQt5", "Qt", "plugins"),
            os.path.join(os.path.dirname(python_dir), "Lib", "site-packages", "PyQt5", "Qt5", "plugins"),
            os.path.join(os.path.dirname(python_dir), "Lib", "site-packages", "PyQt5", "Qt", "plugins")
        ]

        for path in possible_paths:
            if os.path.exists(path):
                os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = path
                print(f"设置 QT_QPA_PLATFORM_PLUGIN_PATH 为: {path}")
                return True

        print("警告: 未能自动找到 Qt 插件路径")
        return False
    except Exception as e:
        print(f"修复 DLL 问题时出错: {e}")
        return False


# 执行修复
fix_pyqt5_dll_issue()

# ==================== 主程序导入 ====================
try:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QSpinBox, QComboBox, QLineEdit, QListWidget, QColorDialog,
        QMessageBox, QGroupBox, QTimeEdit, QTabWidget, QFrame
    )
    from PyQt5.QtCore import QTimer, Qt, QTime
    from PyQt5.QtGui import QColor, QFont, QPalette

    print("PyQt5 模块导入成功!")
except ImportError as e:
    print(f"导入错误: {e}")
    print("可能原因:")
    print("1. PyQt5 安装不完整")
    print("2. 虚拟环境配置不正确")
    print("3. 多个 Python 版本冲突")
    print("解决方案:")
    print("1. 在 PyCharm 终端运行: pip install --force-reinstall PyQt5")
    print("2. 检查 PyCharm 设置中的 Python 解释器路径")
    print("3. 尝试重启 PyCharm")
    sys.exit(1)


# ==================== 倒计时程序主代码 ====================
class CountdownTimer:
    def __init__(self, name, hours, minutes, seconds):
        self.name = name
        self.duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.end_time = datetime.now() + self.duration
        self.paused = False
        self.paused_time = None
        self.elapsed_pause = timedelta()
        self.completed = False

    def remaining_time(self):
        if self.paused:
            return self.paused_time
        elif self.completed:
            return timedelta(0)
        else:
            now = datetime.now()
            if now >= self.end_time:
                self.completed = True
                return timedelta(0)
            return self.end_time - now

    def pause(self):
        if not self.paused and not self.completed:
            self.paused = True
            self.paused_time = self.remaining_time()

    def resume(self):
        if self.paused and not self.completed:
            self.paused = False
            self.end_time = datetime.now() + self.paused_time

    def reset(self):
        self.paused = False
        self.completed = False
        self.end_time = datetime.now() + self.duration
        self.paused_time = None
        self.elapsed_pause = timedelta()


class CountdownApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("可自定义倒计时程序")
        self.setGeometry(100, 100, 800, 600)

        # 存储所有倒计时
        self.timers = []
        self.current_timer = None

        # 创建主界面
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # 主布局
        main_layout = QHBoxLayout(self.main_widget)

        # 左侧控制面板
        control_panel = QGroupBox("控制面板")
        control_layout = QVBoxLayout(control_panel)

        # 创建新倒计时
        new_timer_group = QGroupBox("创建新倒计时")
        new_timer_layout = QVBoxLayout(new_timer_group)

        self.timer_name_edit = QLineEdit("我的倒计时")
        self.timer_name_edit.setPlaceholderText("输入倒计时名称")
        new_timer_layout.addWidget(QLabel("名称:"))
        new_timer_layout.addWidget(self.timer_name_edit)

        time_layout = QHBoxLayout()
        self.hour_spin = QSpinBox()
        self.hour_spin.setRange(0, 99)
        self.hour_spin.setValue(0)
        time_layout.addWidget(QLabel("时:"))
        time_layout.addWidget(self.hour_spin)

        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 59)
        self.min_spin.setValue(1)
        time_layout.addWidget(QLabel("分:"))
        time_layout.addWidget(self.min_spin)

        self.sec_spin = QSpinBox()
        self.sec_spin.setRange(0, 59)
        self.sec_spin.setValue(30)
        time_layout.addWidget(QLabel("秒:"))
        time_layout.addWidget(self.sec_spin)

        new_timer_layout.addLayout(time_layout)

        self.create_btn = QPushButton("创建倒计时")
        self.create_btn.clicked.connect(self.create_timer)
        new_timer_layout.addWidget(self.create_btn)

        control_layout.addWidget(new_timer_group)

        # 倒计时列表
        self.timer_list = QListWidget()
        self.timer_list.itemSelectionChanged.connect(self.select_timer)
        control_layout.addWidget(QLabel("倒计时列表:"))
        control_layout.addWidget(self.timer_list)

        # 控制按钮
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("开始")
        self.start_btn.clicked.connect(self.start_timer)
        btn_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("暂停")
        self.pause_btn.clicked.connect(self.pause_timer)
        btn_layout.addWidget(self.pause_btn)

        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset_timer)
        btn_layout.addWidget(self.reset_btn)

        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self.delete_timer)
        btn_layout.addWidget(self.delete_btn)

        control_layout.addLayout(btn_layout)

        # 右侧显示区域
        display_panel = QGroupBox("倒计时显示")
        display_layout = QVBoxLayout(display_panel)

        # 倒计时显示
        self.timer_display = QLabel("00:00:00")
        self.timer_display.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.timer_display)

        # 名称显示
        self.timer_name_label = QLabel("")
        self.timer_name_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.timer_name_label)

        # 自定义选项
        custom_group = QGroupBox("自定义选项")
        custom_layout = QVBoxLayout(custom_group)

        # 字体大小
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("字体大小:"))
        self.font_size = QComboBox()
        self.font_size.addItems(["24", "36", "48", "64", "72", "96", "128"])
        self.font_size.setCurrentIndex(2)  # 默认48
        self.font_size.currentTextChanged.connect(self.update_display_style)
        font_layout.addWidget(self.font_size)
        custom_layout.addLayout(font_layout)

        # 字体颜色
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("字体颜色:"))
        self.font_color_btn = QPushButton("选择颜色")
        self.font_color_btn.clicked.connect(self.choose_font_color)
        color_layout.addWidget(self.font_color_btn)
        custom_layout.addLayout(color_layout)

        # 背景颜色
        bg_layout = QHBoxLayout()
        bg_layout.addWidget(QLabel("背景颜色:"))
        self.bg_color_btn = QPushButton("选择颜色")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        bg_layout.addWidget(self.bg_color_btn)
        custom_layout.addLayout(bg_layout)

        # 显示格式
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("显示格式:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["HH:MM:SS", "MM:SS", "SS", "完整时间"])
        self.format_combo.currentTextChanged.connect(self.update_display)
        format_layout.addWidget(self.format_combo)
        custom_layout.addLayout(format_layout)

        display_layout.addWidget(custom_group)

        # 添加左右面板到主布局
        main_layout.addWidget(control_panel, 1)
        main_layout.addWidget(display_panel, 2)

        # 定时器更新显示
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(100)  # 100毫秒更新一次

        # 样式初始化
        self.font_color = QColor(0, 0, 0)  # 黑色
        self.bg_color = QColor(255, 255, 255)  # 白色
        self.update_display_style()

        # 创建默认倒计时
        self.create_default_timer()

    def create_default_timer(self):
        """创建一个默认倒计时"""
        default_timer = CountdownTimer("示例倒计时", 0, 1, 0)
        self.timers.append(default_timer)
        self.timer_list.addItem(default_timer.name)
        self.timer_list.setCurrentRow(0)
        self.select_timer()

    def create_timer(self):
        """创建新的倒计时"""
        name = self.timer_name_edit.text().strip()
        if not name:
            name = "未命名倒计时"

        hours = self.hour_spin.value()
        minutes = self.min_spin.value()
        seconds = self.sec_spin.value()

        if hours == 0 and minutes == 0 and seconds == 0:
            QMessageBox.warning(self, "错误", "倒计时时间不能为零！")
            return

        new_timer = CountdownTimer(name, hours, minutes, seconds)
        self.timers.append(new_timer)
        self.timer_list.addItem(new_timer.name)
        self.timer_list.setCurrentRow(len(self.timers) - 1)
        self.select_timer()

    def select_timer(self):
        """选择当前倒计时"""
        selected = self.timer_list.currentRow()
        if selected >= 0 and selected < len(self.timers):
            self.current_timer = self.timers[selected]
            self.timer_name_label.setText(self.current_timer.name)
            self.update_display()

    def start_timer(self):
        """开始或继续倒计时"""
        if self.current_timer:
            if self.current_timer.paused:
                self.current_timer.resume()
            elif self.current_timer.completed:
                self.current_timer.reset()

    def pause_timer(self):
        """暂停倒计时"""
        if self.current_timer and not self.current_timer.completed:
            self.current_timer.pause()

    def reset_timer(self):
        """重置倒计时"""
        if self.current_timer:
            self.current_timer.reset()

    def delete_timer(self):
        """删除当前倒计时"""
        if self.current_timer and len(self.timers) > 1:
            index = self.timers.index(self.current_timer)
            self.timers.remove(self.current_timer)
            self.timer_list.takeItem(index)
            self.timer_list.setCurrentRow(0)
            self.select_timer()
        else:
            QMessageBox.warning(self, "错误", "不能删除最后一个倒计时！")

    def update_display(self):
        """更新倒计时显示"""
        if not self.current_timer:
            return

        remaining = self.current_timer.remaining_time()
        if not remaining:
            self.timer_display.setText("00:00:00")
            return

        # 根据选择的格式显示时间
        format_str = self.format_combo.currentText()

        if format_str == "HH:MM:SS":
            # 时:分:秒
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        elif format_str == "MM:SS":
            # 分:秒
            total_seconds = remaining.seconds
            minutes, seconds = divmod(total_seconds, 60)
            time_str = f"{minutes:02d}:{seconds:02d}"
        elif format_str == "SS":
            # 秒
            total_seconds = remaining.seconds
            time_str = f"{total_seconds}"
        else:  # 完整时间
            # 天:时:分:秒
            days = remaining.days
            hours, remainder = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_str = f"{days}天 {hours:02d}:{minutes:02d}:{seconds:02d}"

        self.timer_display.setText(time_str)

        # 如果倒计时结束，显示特殊样式
        if self.current_timer.completed:
            self.timer_display.setStyleSheet(
                f"background-color: #ff9999; color: #ff0000; font-size: {self.font_size.currentText()}px;"
            )
        else:
            self.update_display_style()

    def update_display_style(self):
        """更新显示样式"""
        if not self.current_timer or self.current_timer.completed:
            return

        style_sheet = f"""
            QLabel {{
                background-color: {self.bg_color.name()};
                color: {self.font_color.name()};
                font-size: {self.font_size.currentText()}px;
                border: 2px solid #cccccc;
                border-radius: 10px;
                padding: 20px;
            }}
        """
        self.timer_display.setStyleSheet(style_sheet)

    def choose_font_color(self):
        """选择字体颜色"""
        color = QColorDialog.getColor(self.font_color, self)
        if color.isValid():
            self.font_color = color
            self.update_display_style()

    def choose_bg_color(self):
        """选择背景颜色"""
        color = QColorDialog.getColor(self.bg_color, self)
        if color.isValid():
            self.bg_color = color
            self.update_display_style()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CountdownApp()
    window.show()
    sys.exit(app.exec_())