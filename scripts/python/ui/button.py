from PySide2.QtWidgets import QToolButton, QStyle
import os
import webbrowser


class ToolButton(QToolButton):
    def __init__(self, item, style, files, link, root, parent=None, icon="remove"):
        super(ToolButton, self).__init__(parent)
        self.item = item
        self.files = files
        self.link = link
        self.root = root
        if icon == "remove":
            pixmapi = getattr(QStyle, "SP_TitleBarCloseButton")
        else:
            pixmapi = getattr(QStyle, "SP_DirOpenIcon")
        self.setIcon(style.standardIcon(pixmapi))

    def remove_item(self):
        child = self.item
        parent = self.item.parent()
        self.files.remove(self.link)
        size = os.path.getsize(self.link)
        self.item.treeWidget().total_size -= size
        self.root.update_total_size()
        while parent:
            parent.removeChild(child)
            if not parent.childCount():
                child = parent
                parent = child.parent()
            else:
                parent = None

    def show_item(self):
        webbrowser.open(os.path.dirname(self.link))
