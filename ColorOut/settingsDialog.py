import os
import json
from PySide2 import QtCore
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
        self.rule_fg_color_button = QtWidgets.QPushButton()
        self.rule_bg_color_button = QtWidgets.QPushButton()
        self.rule_bg_color_checkbox = QtWidgets.QCheckBox("Background color")

        self.sections_splitter = QtWidgets.QSplitter()
        self.sections_splitter.addWidget(self.all_rules)
        self.sections_splitter.addWidget(self.rule_grp)

    def create_layouts(self):
        self.rule_color_layout = QtWidgets.QHBoxLayout()
        self.rule_color_layout.addWidget(QtWidgets.QLabel("Foregound color:"))
        self.rule_color_layout.addWidget(self.rule_fg_color_button)
        self.rule_color_layout.addWidget(self.rule_bg_color_checkbox)
        self.rule_color_layout.addWidget(self.rule_bg_color_button)

        self.main_rule_layout = QtWidgets.QFormLayout()
        self.main_rule_layout.addRow("Name:", self.rule_name)
        self.main_rule_layout.addRow("Pattern: ", self.rule_pattern)
        self.main_rule_layout.addRow(self.rule_color_layout)

        self.rule_grp.setLayout(self.main_rule_layout)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.sections_splitter)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.all_rules.list.currentItemChanged.connect(self.update_rule_info)
        self.rule_bg_color_checkbox.toggled.connect(self.rule_bg_color_button.setEnabled)
        self.rule_fg_color_button.clicked.connect(self.select_fg_color)
        self.rule_bg_color_button.clicked.connect(self.select_bg_color)

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
        self.rule_name.setText(rule_name)
        self.rule_pattern.setText(rule_data.get("pattern"))
        self.rule_fg_color_button.setProperty("color", rule_data.get("fg_color"))
        self.rule_bg_color_button.setProperty("color", rule_data.get("bg_color"))
        self.rule_bg_color_checkbox.setChecked(bool(rule_data.get("bg_color", False)))

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

    @QtCore.Slot()
    def select_fg_color(self):
        starting_color = self.rule_fg_color_button.property("color")
        Logger.debug("Staring fg color: {0}".format(starting_color))

    @QtCore.Slot()
    def select_bg_color(self):
        starting_color = self.rule_bg_color_button.property("color")
        Logger.debug("Staring bg color: {0}".format(starting_color))


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


class ColorButton(QtWidgets.QPushButton):
    pass


if __name__ == "__main__":
    try:
        testTool.close()
        testTool.deleteLater()
    except BaseException:
        pass

    testTool = Dialog()
    testTool.show()
