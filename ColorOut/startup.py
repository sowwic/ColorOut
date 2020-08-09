import os
import pymel.core as pm
from ColorOut import syntax
from ColorOut import menuItem
from ColorOut.loggingFn import Logger

Logger.set_level(20)


def run():
    # Logging
    log_file = os.path.join(pm.moduleInfo(mn="ColorOut", p=1), "ColorOut.log")  # type:str
    Logger.write_to_rotating_file(log_file)
    Logger.info("Logging to file: {0}".format(log_file))

    syntax.HighlightManager.create_connection()
    Logger.info("Applied stdout highlighting")
    menuItem.ColorOutItem.save_add_scriptJob()
