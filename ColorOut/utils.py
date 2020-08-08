import pymel.core as pm
import pymel.api as pma
from PySide2 import QtWidgets
from shiboken2 import wrapInstance, getCppPointer


def getScriptEditorPanel():
    scriptEditorPanel = None
    for panel in pm.getPanel(all=1):
        if "script" in panel:
            scriptEditorPanel = panel
            break

    return scriptEditorPanel


def getScriptEditorReporter():
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


def test_callback(*args):
    print "called"


def script_editor_window():
    se_object = pma.MQtUtil.findWindow("scriptEditorPanel1Window")
    if not se_object:
        return
    # script_editor = wrapInstance(long(pma.MQtUtil.findWindow("scriptEditorPanel1Window")), QtWidgets.QWidget)  # type:QtWidgets.QWidget
    # main_window = wrapInstance(long(pma.MQtUtil.mainWindow()), QtWidgets.QMainWindow)  # type:QtWidgets.QMainWindow
    # print "Script editor: {0}".format(script_editor)
    # for child in main_window.children():
    #     print child


if __name__ == "__main__":
    print getScriptEditorPanel()
