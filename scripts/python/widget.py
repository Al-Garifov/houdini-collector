import glob
import json
import os
import shutil
from pprint import pprint

from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
import hou
import webbrowser

# TODO: split the widget to smaller parts, file is too big to read


def get_human_readable(size):
    suffixes = ["bytes", "KB", "MB", "GB", "TB", "PB"]
    idx = 0
    while size >= 1024:
        size /= 1024
        idx += 1
    if idx == 0:
        return "{:.0f} {}".format(size, suffixes[idx])
    return "{:.2f} {}".format(size, suffixes[idx])


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


class CustomListView(QTreeWidget):
    fileDropped = Signal(list)
    files = set()

    def parse_input(self, urls, processed_urls):
        for url in urls:
            if isinstance(url, QUrl):
                url = url.toLocalFile()
            if not os.path.isdir(url):
                if url not in self.files:
                    processed_urls.add(url.lower())
                    self.files.add(url.lower())
            else:
                files = os.listdir(url)
                processed_files = set()
                for file in files:
                    processed_files.add(os.path.join(url, file))
                self.parse_input(processed_files, processed_urls)

    def __init__(self, parent=None):
        super(CustomListView, self).__init__(parent)
        self.total_size = 0
        self.root_dialog = None
        self.setAcceptDrops(True)
        self.resize(1100, 500)
        self.setHeaderLabels(["Local Files", "Size", " ", " "])
        self.setColumnWidth(0, 1000)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 15)
        self.setColumnWidth(3, 15)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def addPaths(self, paths):
        for link in paths:
            disk = link.split("/")[0]
            prev = None
            for i in range(self.topLevelItemCount()):
                if disk == self.topLevelItem(i).text(0):
                    prev = self.topLevelItem(i)
            if not prev:
                prev = QTreeWidgetItem([disk])
                self.addTopLevelItem(prev)
            path = link.split("/")[1:]
            counter = 0
            for item in path:
                prev.setExpanded(True)
                flag = 0
                for i in range(prev.childCount()):
                    if item == prev.child(i).text(0):
                        prev = prev.child(i)
                        flag = 1
                        break
                if not flag:
                    if counter != len(path) - 1:
                        new_child = QTreeWidgetItem([item])
                        folder_path = os.path.join(link.split(item)[0], item)
                        new_child.setData(0, Qt.ItemDataRole.ToolTipRole, folder_path)
                        prev.addChild(new_child)
                        prev = new_child
                    else:
                        if "<udim>" in link:
                            for udim in glob.glob(link.replace("<udim>", "*")):
                                # FIXME: code dublication
                                size = os.path.getsize(udim)
                                self.total_size += size
                                size = get_human_readable(size)
                                new_child = QTreeWidgetItem([os.path.basename(udim), size])
                                self.files.add(udim)
                                new_child.setData(0, Qt.ItemDataRole.ToolTipRole, udim)
                                prev.addChild(new_child)
                                new_child.setSelected(True)
                                rem_button = ToolButton(new_child, self.style(), self.files, udim, self.root_dialog)
                                rem_button.clicked.connect(rem_button.remove_item)
                                self.setItemWidget(new_child, 3, rem_button)
                                show_button = ToolButton(new_child, self.style(), self.files, udim, self.root_dialog, icon="show")
                                show_button.clicked.connect(show_button.show_item)
                                self.setItemWidget(new_child, 2, show_button)
                        else:
                            size = os.path.getsize(link)
                            self.total_size += size
                            size = get_human_readable(size)
                            new_child = QTreeWidgetItem([item, size])
                            self.files.add(link)
                            new_child.setData(0, Qt.ItemDataRole.ToolTipRole, link)
                            prev.addChild(new_child)
                            new_child.setSelected(True)
                            rem_button = ToolButton(new_child, self.style(), self.files, link, self.root_dialog)
                            rem_button.clicked.connect(rem_button.remove_item)
                            self.setItemWidget(new_child, 3, rem_button)
                            show_button = ToolButton(new_child, self.style(), self.files, link, self.root_dialog, icon="show")
                            show_button.clicked.connect(show_button.show_item)
                            self.setItemWidget(new_child, 2, show_button)
                counter += 1
        self.root_dialog.update_total_size()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            processed_urls = set()
            self.parse_input(event.mimeData().urls(), processed_urls)
            for url in processed_urls:
                links.append(url.replace("\\", "/"))
            self.addPaths(links)
        else:
            event.ignore()


class SubmitDialog(QDialog):
    def __init__(self, parent=None):
        super(SubmitDialog, self).__init__(parent)
        self.tree_list = CustomListView()
        self.tree_list.root_dialog = self
        self.setWindowTitle("Houdini Collector")
        layout = QVBoxLayout()
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        self.submit_button = QPushButton("Save to directory")
        self.submit_button.clicked.connect(self.save_files)
        h_layout.addWidget(self.submit_button, stretch=10)
        h_layout.addWidget(QLabel("Total size:"), stretch=1)
        self.size = QLabel(get_human_readable(self.tree_list.total_size))
        h_layout.addWidget(self.size, stretch=1)
        v_layout.addWidget(self.tree_list)
        v_layout.addLayout(h_layout)
        layout.addLayout(v_layout, stretch=10)
        self.setLayout(layout)
        self.resize(1100, 500)

    def update_total_size(self):
        self.size.setText(get_human_readable(self.tree_list.total_size))
        self.size.update()

    def save_files(self):
        target_dir = hou.ui.selectFile(file_type=hou.fileType.Directory)
        target_dir = hou.text.expandString(target_dir)
        for file in self.tree_list.files:
            file_dir = os.path.dirname(file)
            file_target_dir = os.path.join(target_dir, file_dir.replace(":", ""))
            os.makedirs(file_target_dir, exist_ok=True)
            shutil.copy(file, file_target_dir)


