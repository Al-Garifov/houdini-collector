import glob
import os

from PySide2.QtWidgets import QTreeWidget, QHeaderView, QTreeWidgetItem
from PySide2.QtCore import Signal, QUrl, Qt

from .button import ToolButton
from .utility import get_human_readable


class CustomListView(QTreeWidget):
    def __init__(self, parent=None):
        super(CustomListView, self).__init__(parent)
        self.files = set()
        self.error_files = set()
        self.fileDropped = Signal(list)
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

    def addLeaf(self, link, prev):
        try:
            size = os.path.getsize(link)
        except:
            self.error_files.add(link)
            return
        self.total_size += size
        size = get_human_readable(size)
        new_child = QTreeWidgetItem([os.path.basename(link), size])
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
                        if "<udim>" in link or "<UDIM>" in link:
                            for udim in glob.glob(link.replace("<udim>", "*").replace("<UDIM>", "*")):
                                self.addLeaf(udim, prev)
                        else:
                            self.addLeaf(link, prev)
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
