import os
import shutil

from PySide2.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
import hou

from .listview import CustomListView
from .utility import get_human_readable


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


