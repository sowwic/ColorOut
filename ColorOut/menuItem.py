import pymel.core as pm
from ColorOut import settingsDialog
from ColorOut.loggingFn import Logger


class ColorOutItem:
    WINDOW_MENU = pm.melGlobals["$gMainWindowMenu"]
    ITEM_OBJECT = "ColorOutMenuItem"
    ITEM_LABEL = "ColorOut"

    @classmethod
    def delete_old(cls):
        if pm.menuItem(cls.ITEM_OBJECT, q=1, ex=1):
            pm.deleteUI(cls.ITEM_OBJECT, mi=1)

    @classmethod
    def create(cls):
        cls.delete_old()
        try:
            pm.menuItem(cls.ITEM_OBJECT,
                        l=cls.ITEM_LABEL,
                        parent=cls.WINDOW_MENU,
                        i="colorProfile.svg",
                        ia="wmNodeEditor",
                        c=settingsDialog.Dialog.display)
            Logger.info("Created menuItem: Windows>ColorOut")
        except Exception:
            Logger.exception("Error when creating menu item")

    @classmethod
    def save_add_scriptJob(cls):
        create_script = "from ColorOut import menuItem\nmenuItem.ColorOutItem.create()"
        # ? TODO:Find better event to connect to
        pm.scriptJob(e=["SceneOpened", create_script], ro=1)
        Logger.debug("Safe add scriptJob added")


if __name__ == "__main__":
    ColorOutItem.save_add_scriptJob()
