import os.path

from ui.utility import capture_to_sentry
from ui import dialog
import houdini_parser
from PySide2 import QtCore
import importlib
import hou
import sys

path = os.path.join(os.path.dirname(__file__), "site-packages")
sys.path.insert(0, path)

import sentry_sdk
from sentry_sdk import capture_message


@capture_to_sentry
def run():
    sentry_sdk.init(
        dsn="https://907fc1d47a6b6e29691284fceac1d73c@o4507125362458624.ingest.us.sentry.io/4507125364162560",
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        traces_sample_rate=1.0,
        # Set profiles_sample_rate to 1.0 to profile 100%
        # of sampled transactions.
        # We recommend adjusting this value in production.
        profiles_sample_rate=1.0
    )

    capture_message("Service started!")

    importlib.reload(houdini_parser)
    importlib.reload(dialog)

    refs = houdini_parser.run()

    t = dialog.SubmitDialog()
    t.setParent(hou.qt.mainWindow(), QtCore.Qt.Window)
    t.tree_list.addPaths(refs)
    t.update_total_size()
    t.show()
