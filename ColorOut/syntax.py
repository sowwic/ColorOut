from ColorOut import utils
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2 import QtWidgets


class HighlighRule:
    def __init__(self, fgColor, pattern="", bgColor=None, bold=False, italic=False, fontName="Courier New"):
        self.pattern = QtCore.QRegExp(pattern)
        self.form = QtGui.QTextCharFormat()
        self.form.setForeground(QtGui.QColor(*fgColor))
        if bgColor:
            self.form.setBackground(QtGui.QColor(*bgColor))
        # !Setting font cause constant not scalable fontsize
        # self.font = QtGui.QFont(fontName)
        # self.font.setBold(bold)
        # self.font.setItalic(italic)
        # self.form.setFont(self.font)


class StdOutSyntax(QtGui.QSyntaxHighlighter):
    def __init__(self, parent, rules):
        super(StdOutSyntax, self).__init__(parent)
        self.parent = parent
        self.rules = rules

    def highlightBlock(self, text):
        for rule in self.rules:
            pattern = rule.pattern
            index = pattern.indexIn(text)
            while index >= 0:
                matchLen = pattern.matchedLength()
                self.setFormat(index, matchLen, rule.form)
                index = pattern.indexIn(text, index + matchLen)

            self.setCurrentBlockState(0)


def applyHighlight():
    i = 1
    while i:
        try:
            seReporter = utils.getScriptEditorReporter()  # type:QtWidgets.QTextEdit
            # Remove the old syntax and raise exception to get out of the loop
            assert seReporter.findChild(QtGui.QSyntaxHighlighter).deleteLater()
        except TypeError:
            # If no widget found - increment
            i += 1
        except (AttributeError, AssertionError):
            break

    # Define rules
    infoRule = HighlighRule(fgColor=(135, 206, 250), pattern=r"^(#|//).*(info|INFO|NOTE).+$")
    debugRule = HighlighRule(fgColor=(135, 206, 250), pattern=r"^(#|//).*(debug|DEBUG).+$")
    warningRule = HighlighRule(fgColor=(255, 175, 44), pattern=r"^(#|//).*(warning|WARNING|Warning).+$")
    errorRule = HighlighRule(fgColor=(240, 128, 128), pattern=r"^(#|//).*(error|ERROR|Error|CRITICAL).+$")

    stdOut = StdOutSyntax(seReporter, [infoRule, debugRule, warningRule, errorRule])

    return stdOut


def on_focus_changed(old_widget, new_widget):
    if not new_widget:
        return
    if "cmdScrollFieldExecuter" in new_widget.objectName():
        applyHighlight()


def create_connection():
    app = QtWidgets.QApplication.instance()
    app.focusChanged.connect(on_focus_changed)


if __name__ == "__main__":
    create_connection()
