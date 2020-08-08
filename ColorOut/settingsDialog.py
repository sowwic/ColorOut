from PySide2 import QtCore
from PySide2 import QtWidgets
import pymel.core as pm
import pymel.api as pma
from shiboken2 import wrapInstance


def mayaMainWindow():
    mainWindowPtr = pma.MQtUtil.mainWindow()
    if mainWindowPtr:
        return wrapInstance(long(mainWindowPtr), QtWidgets.QWidget)
    else:
        mayaMainWindow()


class Dialog(QtWidgets.QDialog):

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
        self.setMinimumSize(500, 400)

        # UI setup
        self.geometry = None
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_actions(self):
        pass

    def create_widgets(self):
        pass

    def create_layouts(self):
        pass

    def create_connections(self):
        pass

    def showEvent(self, event):
        super(Dialog, self).showEvent(event)
        if self.geometry:
            self.setGeometry(self.geometry)

    def hideEvent(self, event):
        if isinstance(self, Dialog):
            super(Dialog, self).hideEvent(event)
            self.geometry = self.saveGeometry()


if __name__ == "__main__":
    try:
        testTool.close()
        testTool.deleteLater()
    except BaseException:
        pass

    testTool = Dialog()
    testTool.show()
