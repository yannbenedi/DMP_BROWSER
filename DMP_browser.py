from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListWidget, QPushButton, QLineEdit, QMessageBox, \
    QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from psd_tools import PSDImage
import glob
import re
import sys
import os
from pathlib import Path
from icecream import ic
import resources  # Import the compiled resource file for icon

"""
clean, remove try catch and ic
indicate where to change for new project
export requirments.txt
"""


class UI(QMainWindow):
    ROOT_PATH = Path(r"C:\TMP_local\Project")

    def __init__(self):
        super(UI, self).__init__()

        # Load the UI to keep the resource icon
        fileh = QtCore.QFile("DMPbrowserUI.ui")
        fileh.open(QtCore.QFile.ReadOnly)
        uic.loadUi(fileh, self)
        fileh.close()

        self.list_pic_suffix = [".jpg", ".psd", ".psb"]

        # CUSTOM DIRECTORY
        self.dir_special = {
            "References": Path(r"C:\_YannB\_WORK\11_UNTOLD\_REF"),
            "Textures": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
            "Plate": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
            "Transfer": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
            "Tools": Path(r"C:\_YannB\_WORK\11_UNTOLD\_TRANSFER"),
        }
        self.special_keys = [key for key in self.dir_special]

        # Define Widgets
        self.frame_folder_shortcut = self.findChild(QFrame, "frame_folder_shortcut")

        self.user_shot_type = self.findChild(QLineEdit, "user_shot_type")
        self.user_shot_type.setFocusPolicy(Qt.StrongFocus)  # focus to start typing

        self.label_seq_info = self.findChild(QLabel, "label_seq_info")
        self.label_scene_info = self.findChild(QLabel, "label_scene_info")
        self.label_shot_info = self.findChild(QLabel, "label_shot_info")
        self.label_valid_check = self.findChild(QLabel, "label_valid_check")
        self.label_custom_dir = self.findChild(QLabel, "label_custom_dir")

        self.list_seq_sel = self.findChild(QListWidget, "list_seq_sel")
        self.list_scene_sel = self.findChild(QListWidget, "list_scene_sel")
        self.list_shot_sel = self.findChild(QListWidget, "list_shot_sel")
        self.list_file_shot_sel = self.findChild(QListWidget, "list_file_shot_sel")
        self.list_3Dfile_shot_sel = self.findChild(QListWidget, "list_3Dfile_shot_sel")

        self.label_sel_pic = self.findChild(QLabel, "label_sel_pic")

        self.update_psd_but = self.findChild(QPushButton, "update_psd_but")
        self.open_shot_but = self.findChild(QPushButton, "open_shot_but")
        self.open_3D_but = self.findChild(QPushButton, "open_3D_but")

        # Widgets edit and signals
        self.user_shot_type.setPlaceholderText("Type Seq Scene Shot separated by space")

        self.open_shot_but.clicked.connect(lambda: self.open_folder(self.shot_PSD_dir))
        self.open_3D_but.clicked.connect(lambda: self.open_folder(self.shot_3D_dir))
        self.update_psd_but.clicked.connect(lambda: self.extract_psd_thumbnail())

        # List Select items
        self.list_seq_sel.itemClicked.connect(self.list_seq_clicked_event)
        self.list_scene_sel.itemClicked.connect(self.list_scene_clicked_event)
        self.list_shot_sel.itemClicked.connect(self.list_shot_clicked_event)
        self.list_file_shot_sel.itemClicked.connect(self.list_file_clicked_event)
        self.list_3Dfile_shot_sel.itemClicked.connect(self.list_3Dfile_clicked_event)

        self.list_file_shot_sel.doubleClicked.connect(lambda: self.open_folder(self.file_dir))
        self.list_3Dfile_shot_sel.doubleClicked.connect(lambda: self.open_folder(self.file3D_dir))

        self.set_lists()

        # Create list custom directories
        self.dir_custom_layout = QVBoxLayout()
        self.dir_custom_layout.setSpacing(10)
        self.dir_custom_layout.setAlignment(Qt.AlignTop)
        self.dir_custom_dct = {}
        self.add_custom_dir_but()
        self.frame_folder_shortcut.setLayout(self.dir_custom_layout)

        # Show app
        self.show()

    def add_custom_dir_but(self):
        """
        Create Custom Directories
        """
        for key in self.dir_special:
            button_layout = QHBoxLayout()
            self.dir_custom_layout.addLayout(button_layout)

            custom_dir_name_label = QLabel(key)

            custom_dir_icon_but = QPushButton("", self)
            custom_dir_icon_but.setIcon(QtGui.QIcon("./icons/folder.png"))
            custom_dir_icon_but.setIconSize(QtCore.QSize(35, 35))

            button_layout.setAlignment(Qt.AlignTop)
            button_layout.setSpacing(10)
            custom_dir_icon_but.setStyleSheet("QPushButton{ border: none; border-radius: 10px; }")

            button_layout.addWidget(custom_dir_icon_but)
            button_layout.addWidget(custom_dir_name_label)

            self.dir_custom_dct[custom_dir_icon_but] = self.dir_special[key]
            custom_dir_icon_but.clicked.connect(self.set_label)

    @pyqtSlot()
    def set_label(self):
        """
        Assign Custom directory path for each button
        """
        button = self.sender()
        custom_dir_path = self.dir_custom_dct[button]
        self.open_folder(custom_dir_path)

    def show_question_messagebox(self):
        self.buttonReply = QMessageBox.question(self, 'NEW SHOT?',
                                                f"Do you want to create: {self.seq} / {self.scene} / {self.shot}",
                                                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                                                QMessageBox.Cancel)

    def set_paths(self):
        """
        Project structure folder
        """
        self.seq_dir = self.ROOT_PATH / self.seq
        self.scene_dir = self.ROOT_PATH / self.seq / self.scene

        self.shot_dir = self.ROOT_PATH / self.seq / self.scene / self.shot
        self.shot_PSD_dir = self.shot_dir / "PSD"
        self.shot_3D_dir = self.shot_dir / "3D" / "scenes"
        self.label_shot_info.setText(self.shot)

    def create_template_folder(self):
        """
        Template for new shot
        """
        self.shot_dir.joinpath("3D/scenes").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/data").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/textures").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/assets").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("3D/imagePlane").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("PSD").mkdir(parents=True, exist_ok=True)
        self.shot_dir.joinpath("REF").mkdir(parents=True, exist_ok=True)

        self.update_all_lists()

        self.open_folder(self.shot_dir)
        self.user_shot_type.setText("")

    def update_all_lists(self):

        self.list_seq_sel.clear()
        self.list_scene_sel.clear()
        self.list_shot_sel.clear()
        self.list_file_shot_sel.clear()
        self.list_3Dfile_shot_sel.clear()

        # Update lists
        for folder in self.ROOT_PATH.iterdir():
            self.list_seq_sel.addItem(folder.name)
        for folder in self.seq_dir.iterdir():
            self.list_scene_sel.addItem(folder.name)
        for folder in self.scene_dir.iterdir():
            self.list_shot_sel.addItem(folder.name)
        for folder in self.shot_PSD_dir.iterdir():
            if folder.suffix in self.list_pic_suffix:
                self.list_file_shot_sel.addItem(folder.name)
        for folder in self.shot_3D_dir.iterdir():
            self.list_3Dfile_shot_sel.addItem(folder.name)

        item_seq = self.list_seq_sel.findItems(self.seq, Qt.MatchContains)
        self.list_seq_sel.setCurrentItem(item_seq[0])
        item_scene = self.list_scene_sel.findItems(self.scene, Qt.MatchContains)
        self.list_scene_sel.setCurrentItem(item_scene[0])
        item_shot = self.list_shot_sel.findItems(self.shot, Qt.MatchContains)
        self.list_shot_sel.setCurrentItem(item_shot[0])

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            try:
                self.check_project_entry_format()
                self.set_paths()
                if self.shot_dir.exists():
                    self.update_all_lists()
                else:
                    self.show_question_messagebox()
                    if self.buttonReply == QMessageBox.Yes:
                        self.create_template_folder()
                    if self.buttonReply == QMessageBox.No:
                        print('No clicked.')
                    if self.buttonReply == QMessageBox.Cancel:
                        print('Cancel')
            except Exception as e:
                print(e)


    def list_seq_clicked_event(self, item):
        self.seq = item.text()
        self.seq_dir = self.ROOT_PATH / self.seq
        self.label_seq_info.setText(self.seq)

        self.list_scene_sel.clear()
        self.list_shot_sel.clear()
        self.list_file_shot_sel.clear()
        self.list_3Dfile_shot_sel.clear()

        if self.seq_dir.is_dir():
            for folder in self.seq_dir.iterdir():
                self.list_scene_sel.addItem(folder.name)

    def list_scene_clicked_event(self, item):
        self.scene = item.text()
        self.scene_dir = self.ROOT_PATH / self.seq / self.scene
        self.label_scene_info.setText(self.scene)

        self.list_shot_sel.clear()
        self.list_file_shot_sel.clear()
        self.list_3Dfile_shot_sel.clear()

        if self.scene_dir.is_dir():
            for folder in self.scene_dir.iterdir():
                self.list_shot_sel.addItem(folder.name)

    def list_shot_clicked_event(self, item):
        self.shot = item.text()
        self.set_paths()
        self.list_file_update()

    def list_3Dfile_clicked_event(self, item):

        self.file3D = item.text()
        self.file3D_dir = self.shot_3D_dir / self.file3D

    def list_file_clicked_event(self, item):
        self.file = item.text()
        self.file_dir = self.shot_PSD_dir / self.file

        self.file_pic = QPixmap(str(self.file_dir))
        self.smaller_pixmap = self.file_pic.scaled(700, 400, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.label_sel_pic.setPixmap(self.smaller_pixmap)

    def list_file_update(self):
        self.list_file_shot_sel.clear()
        self.list_3Dfile_shot_sel.clear()

        if self.shot_PSD_dir.is_dir():
            for folder in self.shot_PSD_dir.iterdir():
                if folder.suffix in self.list_pic_suffix:
                    self.list_file_shot_sel.addItem(folder.name)
        if self.shot_3D_dir.is_dir():
            for folder in self.shot_3D_dir.iterdir():
                self.list_3Dfile_shot_sel.addItem(folder.name)

    def extract_psd_thumbnail(self):
        # Create jpg from each psd or psb for gallery
        search_patch = f'{self.shot_PSD_dir}\\*.psd'
        search_patch_psb = f'{self.shot_PSD_dir}\\*.psb'
        shot_pics = glob.glob(search_patch) + glob.glob(search_patch_psb)

        for pic in shot_pics:
            PSDImage.open(pic).composite().save(f"{pic}_preview.jpg")
        self.list_file_update()


    def check_project_entry_format(self):
        """
        UPDATE PER PROJECT
        check if the user entry is matching the project format. check pattern "000 000 0000"
        Add zero if needed "10 20 5", turn into "010 020 0005"
        seq should be 3 / scene should be 3 / shot should be 4
        """

        ic("START SPLIT USER NAME")
        self.seq, self.scene, self.shot = str(self.user_shot_type.text()).split()
        ic(self.seq, self.scene, self.shot)

        # add zeros needed to fill the pattern match "000 000 0000"
        self.seq = f"{int(self.seq):03d}"
        self.scene = f"{int(self.scene):03d}"
        self.shot = f"{int(self.shot):04d}"

        shot_user_corrected = " ".join((self.seq, self.scene, self.shot))
        ic(self.seq, self.scene, self.shot)
        ic(shot_user_corrected)

        # check "000 000 0000" pattern
        pattern_project = re.compile("^[0-9]{3}\s[0-9]{3}\s[0-9]{4}$")
        pattern_check_result = pattern_project.match(shot_user_corrected)

        if pattern_check_result:
            self.user_shot_type.setText(shot_user_corrected)

    def set_lists(self):
        self.list_seq_sel.clear()
        self.list_scene_sel.clear()
        self.list_shot_sel.clear()
        self.list_file_shot_sel.clear()
        for folder in self.ROOT_PATH.iterdir():
            self.list_seq_sel.addItem(folder.name)

    def open_folder(self, user_dir):
        os.startfile(user_dir)


if __name__ == "__main__":
    # Initialise app
    app = QApplication(sys.argv)

    # load stylesheet
    qss = "style.qss"
    with open(qss, "r") as fh:
        app.setStyleSheet(fh.read())

    UIWindow = UI()
    #UIWindow.user_shot_type.setFocus() # add focus on QlineEdit to start typing
    app.exec()
