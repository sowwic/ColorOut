import pymel.core as pm
from ColorOut import settingsDialog


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
        menu_item = pm.menuItem(cls.ITEM_OBJECT,
                                l=cls.ITEM_LABEL,
                                parent=cls.WINDOW_MENU,
                                i="colorProfile.svg",
                                ia="wmNodeEditor",
                                c=settingsDialog.Dialog.display)


if __name__ == "__main__":
    ColorOutItem.create()
