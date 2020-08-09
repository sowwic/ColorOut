import os
import json
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import pymel.core as pm
import pymel.api as pma
from shiboken2 import wrapInstance
from ColorOut.loggingFn import Logger


def mayaMainWindow():
    mainWindowPtr = pma.MQtUtil.mainWindow()
    if mainWindowPtr:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)
    else:
        mayaMainWindow()


class Dialog(QtWidgets.QDialog):

    USER_RULES = os.path.join(pm.moduleInfo(mn="ColorOut", p=1), "ColorOut", "rules", "user.json")  # type:str
    WINDOW_TITLE = "ColorOut settings"
    UI_NAME = "ColorOutSettings"
    UI_INSTANCE = None

    @classmethod
    def display(cls, *args):
        if not cls.UI_INSTANCE:
            cls.UI_INSTANCE = Dialog()

        if cls.UI_INSTANCE.isHidden():
            cls.UI_INSTANCE.show()
        else:
            cls.UI_INSTANCE.raise_()
            cls.UI_INSTANCE.activateWindow()

    def __init__(self, parent=mayaMainWindow()):
        super(Dialog, self).__init__(parent)
        if pm.about(macOS=1):
            self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setMinimumSize(400, 300)

        # UI setup
        self.geometry = None
        self.create_actions()
        self.create_menu_bar()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_menu_bar(self):
        self.menubar = QtWidgets.QMenuBar()

    def create_widgets(self):
        self.all_rules = AllRulesWidget()
        self.rule_grp = QtWidgets.QGroupBox("Rule")
        self.rule_name = QtWidgets.QLineEdit()
        self.rule_pattern = QtWidgets.QLineEdit()
        self.rule_fg_color = ColorButton()
        self.rule_bg_color = ColorButton()
        self.rule_bg_color_checkbox = QtWidgets.QCheckBox("Background color")
        self.save_button = QtWidgets.QPushButton("Save")

        self.sections_splitter = QtWidgets.QSplitter()
        self.sections_splitter.addWidget(self.all_rules)
        self.sections_splitter.addWidget(self.rule_grp)

    def create_layouts(self):
        self.rule_color_layout = QtWidgets.QHBoxLayout()
        self.rule_color_layout.addWidget(QtWidgets.QLabel("Foregound color:"))
        self.rule_color_layout.addWidget(self.rule_fg_color)
        self.rule_color_layout.addStretch()
        self.rule_color_layout.addWidget(self.rule_bg_color_checkbox)
        self.rule_color_layout.addWidget(self.rule_bg_color)
        self.rule_color_layout.addStretch()

        self.main_rule_layout = QtWidgets.QFormLayout()
        self.main_rule_layout.addRow("Name:", self.rule_name)
        self.main_rule_layout.addRow("Pattern: ", self.rule_pattern)
        self.main_rule_layout.addRow(self.rule_color_layout)
        self.main_rule_layout.addRow(self.save_button)

        self.rule_grp.setLayout(self.main_rule_layout)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.sections_splitter)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.all_rules.list.currentItemChanged.connect(self.update_rule_info)
        self.all_rules.add_button.clicked.connect(self.add_rule)
        self.rule_bg_color_checkbox.toggled.connect(self.rule_bg_color.setEnabled)
        self.save_button.clicked.connect(self.save_changes)

    def showEvent(self, event):
        super(Dialog, self).showEvent(event)
        self.update_rule_list()
        if self.geometry:
            self.setGeometry(self.geometry)

    def hideEvent(self, event):
        if isinstance(self, Dialog):
            super(Dialog, self).hideEvent(event)
            self.geometry = self.saveGeometry()

    @QtCore.Slot(QtWidgets.QWidgetItem)
    def update_rule_info(self, item):
        rule_name = item.data(0)
        rule_data = item.data(QtCore.Qt.UserRole)
        Logger.debug(rule_data.get("fg_color"))
        self.rule_name.setText(rule_name)
        self.rule_pattern.setText(rule_data.get("pattern"))
        self.rule_fg_color.set_color(rule_data.get("fg_color"))
        self.rule_bg_color.set_color(rule_data.get("bg_color"))
        self.rule_bg_color_checkbox.setChecked(bool(rule_data.get("bg_color", False)))
        self.rule_bg_color.setEnabled(self.rule_bg_color_checkbox.isChecked())

    @QtCore.Slot()
    def update_rule_list(self):
        self.all_rules.list.clear()
        rules_dict = {}
        with open(self.USER_RULES, "r") as json_file:
            rules_dict = json.load(json_file)

        for rule in rules_dict.keys():
            item = QtWidgets.QListWidgetItem(rule)
            item.setData(QtCore.Qt.UserRole, rules_dict[rule])
            self.all_rules.list.addItem(item)

    def serialize_info(self):
        fg_color = self.rule_fg_color.get_color()
        fg_color = [fg_color.red(), fg_color.green(), fg_color.blue()]
        if self.rule_bg_color_checkbox.isChecked():
            bg_color = self.rule_bg_color.get_color()
            bg_color = [bg_color.red(), bg_color.green(), bg_color.blue()]
        else:
            bg_color = []

        rule_dict = {self.rule_name.text(): {
            "pattern": self.rule_pattern.text(),
            "fg_color": fg_color,
            "bg_color": bg_color}
        }
        return rule_dict

    @QtCore.Slot()
    def save_changes(self):
        current_item = self.all_rules.list.findItems(self.rule_name.text(), QtCore.Qt.MatchExactly)
        if current_item:
            print current_item
            # Logger.debug("Updating {}".format(current_item.data(0)))
        else:
            new_rule_item = QtWidgets.QListWidgetItem(self.rule_name.text())
            new_rule_item.setData(QtCore.Qt.UserRole, self.serialize_info())
            Logger.debug(new_rule_item.data(QtCore.Qt.UserRole))
            self.all_rules.list.addItem(new_rule_item)
            self.all_rules.list.setCurrentItem(new_rule_item)

    @QtCore.Slot()
    def add_rule(self):
        self.rule_name.setText("")
        self.rule_pattern.setText("")
        self.rule_fg_color.set_color(QtCore.Qt.white)
        self.rule_bg_color.set_color(QtCore.Qt.black)
        self.rule_bg_color_checkbox.setChecked(0)


class AllRulesWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AllRulesWidget, self).__init__(parent)

        # Widgets
        self.list = QtWidgets.QListWidget()
        self.add_button = QtWidgets.QPushButton("+")
        self.delete_button = QtWidgets.QPushButton("-")
        for btn in [self.add_button, self.delete_button]:
            btn.setMaximumWidth(30)

        # Layouts
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.list)
        self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)


class ColorButton(QtWidgets.QLabel):
    def __init__(self, parent=None, color=[1, 1, 1]):
        super(ColorButton, self).__init__(parent)

        self._color = QtGui.QColor()  # Invalid color

        self.set_size(25, 25)
        self.set_color(color)

    def set_size(self, width, height):
        self.setFixedSize(width, height)

    def set_color(self, color):
        Logger.debug("Color: {0}".format(color))
        if isinstance(color, list):
            if not color:
                color = [1, 1, 1]
            color = QtGui.QColor.fromRgb(*color)

        color = QtGui.QColor(color)
        if self._color == color:
            return

        self._color = color
        pixmap = QtGui.QPixmap(self.size())
        pixmap.fill(self._color)
        self.setPixmap(pixmap)

    def get_color(self):
        return self._color

    def select_color(self):
        color = QtWidgets.QColorDialog.getColor(self.get_color(), self, options=QtWidgets.QColorDialog.DontUseNativeDialog)
        if color.isValid():
            self.set_color(color)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.select_color()


if __name__ == "__main__":
    try:
        testTool.close()
        testTool.deleteLater()
    except BaseException:
        pass

    testTool = Dialog()
    testTool.show()
