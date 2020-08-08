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


if __name__ == "__main__":
    pass
