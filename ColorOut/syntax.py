import os
import shutil
import json
import pymel.core as pm
import pymel.api as pma
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from ColorOut.loggingFn import Logger


class HighlighRule:
    def __init__(self, fg_color, pattern="", bg_color=None, bold=False, italic=False, font_name="Courier New"):
        self.pattern = QtCore.QRegExp(pattern)
        self.form = QtGui.QTextCharFormat()
        self.form.setForeground(QtGui.QColor(*fg_color))
        if bg_color:
            self.form.setBackground(QtGui.QColor(*bg_color))
        # !Setting font results in highlighted text no resizing
        # self.font = QtGui.QFont(font_name)
        # self.form.setFont(self.font)
        # self.font.setBold(bold)
        # self.font.setItalic(italic)

    @classmethod
    def from_dict(cls, rule_dict):
        new_rule = HighlighRule(rule_dict.get("fg_color", [0, 0, 0]),
                                rule_dict.get("pattern", ""),
                                rule_dict.get("bg_color", None),
                                rule_dict.get("bold", 0),
                                rule_dict.get("italic", 0),
                                rule_dict.get("font_name", "Courier New"))
        return new_rule


class StdOutSyntax(QtGui.QSyntaxHighlighter):
    def __init__(self, parent, rules):
        super(StdOutSyntax, self).__init__(parent)
        self.parent = parent
        self.rules = rules

    def highlightBlock(self, text):
        try:
            for rule in self.rules:
                pattern = rule.pattern
                index = pattern.indexIn(text)
                while index >= 0:
                    matchLen = pattern.matchedLength()
                    self.setFormat(index, matchLen, rule.form)
                    index = pattern.indexIn(text, index + matchLen)

                self.setCurrentBlockState(0)
        except Exception:
            Logger.exception("Highlighter error")


class HighlightManager:

    DEFAULT_RULES = os.path.join(pm.moduleInfo(mn="ColorOut", p=1), "ColorOut", "rules", "default.json")  # type:str
    USER_RULES = os.path.join(pm.moduleInfo(mn="ColorOut", p=1), "ColorOut", "rules", "user.json")  # type:str

    @classmethod
    def get_script_editor_reporter(cls):
        """Gets current reporter widget

        :return: Reporter as widget
        :rtype: QtWidgets.QTextEdit
        """
        reporter = None
        widgetIndex = 1
        while widgetIndex:
            try:
                reporter = wrapInstance(long(pma.MQtUtil.findControl("cmdScrollFieldReporter{0}".format(widgetIndex))), QtWidgets.QTextEdit)
                break
            except TypeError:
                widgetIndex += 1

        return reporter

    @classmethod
    def load_rules(cls):
        if not os.path.isfile(cls.USER_RULES):
            shutil.copy2(cls.DEFAULT_RULES, cls.USER_RULES)

        # Import rules
        rules = None
        with open(cls.USER_RULES, "r") as json_file:
            rules = json.load(json_file)
        if not rules:
            Logger.error("User rules are empty, using defaults")
            with open(cls.DEFAULT_RULES, "r") as json_file:
                rules = json.load(json_file)

        rule_objects = []
        for r in rules.keys():
            rule_objects.append(HighlighRule.from_dict(rules[r]))

        return rule_objects

    @classmethod
    def applyHighlight(cls):
        i = 1
        while i:
            try:
                seReporter = cls.get_script_editor_reporter()  # type:QtWidgets.QTextEdit
                # Remove the old syntax and raise exception to get out of the loop
                assert seReporter.findChild(QtGui.QSyntaxHighlighter).deleteLater()
            except TypeError:
                # If no widget found - increment
                i += 1
            except (AttributeError, AssertionError):
                break

        stdOut = StdOutSyntax(seReporter, cls.load_rules())
        Logger.debug("Highlighter applied")
        return stdOut

    @classmethod
    def on_focus_changed(cls, old_widget, new_widget):
        if not new_widget:
            return
        if "cmdScrollFieldExecuter" in new_widget.objectName():
            cls.applyHighlight()

    @classmethod
    def create_connection(cls):
        app = QtWidgets.QApplication.instance()  # type: QtWidgets.QApplication
        app.focusChanged.connect(cls.on_focus_changed)

    @classmethod
    def remove_connection(cls):
        app = QtWidgets.QApplication.instance()  # type: QtWidgets.QApplication
        try:
            app.focusChanged.disconnect(cls.on_focus_changed)
        except RuntimeError:
            pass

        Logger.debug("Removed connection")


if __name__ == "__main__":
    HighlightManager.remove_connection()
    HighlightManager.create_connection()
