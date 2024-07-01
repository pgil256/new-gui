import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QCheckBox,
    QStackedWidget,
    QFrame,
    QDialog,
    QComboBox,
)
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import csv


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("kneespa.ui", self)

    def initUI(self):

        # Keypad for logging in
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        keypad_layout = QHBoxLayout()
        self.keypad = []
        for i in range(1, 10):
            btn = QPushButton(str(i), self)
            btn.clicked.connect(self.keypad_input)
            keypad_layout.addWidget(btn)
            self.keypad.append(btn)

        clear_button = QPushButton("X", self)
        clear_button.clicked.connect(self.clear_password)
        keypad_layout.addWidget(clear_button)

        layout.addLayout(keypad_layout)

        # Login button
        login_button = QPushButton("Login", self)
        login_button.clicked.connect(self.login)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def keypad_input(self):
        sender = self.sender()
        self.password_input.setText(self.password_input.text() + "*")

    def clear_password(self):
        self.password_input.clear()

    def login(self):
        user_password = 123
        admin_password = 456
        if self.password_input.text() == user_password:
            main_window.stackedWidget.setCurrentIndex(1)
        elif self.password_input.text() == admin_password:
            main_window.stackedWidget.setCurrentIndex(1)
        else:
            self.password_input.setText("")


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Preconfigured Protocols", self)
        layout.addWidget(title)

        # Protocol display area
        self.protocol_image = QLabel(self)
        self.image_index = 1
        self.update_image()
        layout.addWidget(self.protocol_image)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        self.left_button = QPushButton("<", self)
        self.left_button.clicked.connect(self.prev_image)
        nav_layout.addWidget(self.left_button)

        self.right_button = QPushButton(">", self)
        self.right_button.clicked.connect(self.next_image)
        nav_layout.addWidget(self.right_button)

        layout.addLayout(nav_layout)

        # Enter Treatment Plan button
        enter_treatment_button = QPushButton("Enter Treatment Plan", self)
        enter_treatment_button.clicked.connect(self.enter_treatment_plan)
        layout.addWidget(enter_treatment_button)

        # Use Custom Preset button
        use_custom_preset_button = QPushButton("Use Custom Preset", self)
        use_custom_preset_button.clicked.connect(self.use_custom_preset)
        layout.addWidget(use_custom_preset_button)

        # Start button
        start_button = QPushButton("Start", self)
        layout.addWidget(start_button)

        # Show Pressure checkbox
        self.show_pressure_checkbox = QCheckBox("Show Pressure", self)
        layout.addWidget(self.show_pressure_checkbox)

        # Timer
        self.timer_label = QLabel("Time Remaining: ", self)
        layout.addWidget(self.timer_label)

        # Back button
        back_button = QPushButton("Back", self)
        back_button.clicked.connect(self.back)
        layout.addWidget(back_button)

        # Mov button
        mov_button = QPushButton("Mov", self)
        mov_button.clicked.connect(self.show_mov)
        layout.addWidget(mov_button)

        # Help button
        help_button = QPushButton("Help", self)
        help_button.clicked.connect(self.show_help)
        layout.addWidget(help_button)

        self.setLayout(layout)

    def update_image(self):
        self.protocol_image.setPixmap(
            QPixmap(f"images/protocol-graphics/{self.image_index}.png")
        )

    def prev_image(self):
        if self.image_index > 1:
            self.image_index -= 1
            self.update_image()

    def next_image(self):
        if self.image_index < 18:
            self.image_index += 1
            self.update_image()

    def enter_treatment_plan(self):
        dialog = TreatmentPlanDialog(self)
        dialog.exec_()

    def use_custom_preset(self):
        dialog = CustomPresetDialog(self)
        dialog.exec_()

    def back(self):
        self.parent().setCurrentIndex(0)

    def show_mov(self):
        dialog = MovDialog(self)
        dialog.exec_()

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec_()


class TreatmentPlanDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.patient_id_input = QLineEdit(self)
        layout.addWidget(self.patient_id_input)

        self.patient_data_fields = {}
        for field in [
            "Patient Name",
            "Treatment Start Date",
            "Treatment Frequency",
            "Protocol Number",
            "Number of Cycles",
            "Pressure",
            "Use Pulse",
        ]:
            h_layout = QHBoxLayout()
            label = QLabel(field, self)
            h_layout.addWidget(label)
            if field == "Use Pulse":
                input_widget = QComboBox(self)
                input_widget.addItems(["true", "false"])
            else:
                input_widget = QLineEdit(self)
            self.patient_data_fields[field] = input_widget
            h_layout.addWidget(input_widget)
            layout.addLayout(h_layout)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        edit_button = QPushButton("Edit", self)
        edit_button.clicked.connect(self.edit_fields)
        button_layout.addWidget(edit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def clear_fields(self):
        for field in self.patient_data_fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)

    def edit_fields(self):
        if self.parent().parent().parent().password_input.text() == "456":
            for field in self.patient_data_fields.values():
                field.setEnabled(True)
        else:
            for field in self.patient_data_fields.values():
                field.setEnabled(False)


class CustomPresetDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        fields = ["Protocol Number", "Number of Cycles", "Pressure", "Use Pulse"]
        self.custom_fields = {}
        for field in fields:
            h_layout = QHBoxLayout()
            label = QLabel(field, self)
            h_layout.addWidget(label)
            if field == "Use Pulse":
                input_widget = QComboBox(self)
                input_widget.addItems(["true", "false"])
            else:
                input_widget = QLineEdit(self)
            self.custom_fields[field] = input_widget
            h_layout.addWidget(input_widget)
            layout.addLayout(h_layout)

        button_layout = QHBoxLayout()
        clear_button = QPushButton("Clear", self)
        clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(clear_button)

        enter_button = QPushButton("Enter", self)
        button_layout.addWidget(enter_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def clear_fields(self):
        for field in self.custom_fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)


class MovDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle("YouTube Player")

        iframe = QLabel(self)
        iframe.setText(
            '<iframe width="560" height="315" src="https://www.youtube.com/embed/UIyvAmPFn8g?si=RbX3jltrUwZ1aFJi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
        )
        layout.addWidget(iframe)

        self.setLayout(layout)


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        help_text = QLabel("Instructions on how to use the current page...", self)
        layout.addWidget(help_text)

        close_button = QPushButton("X", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)


class MainWindow(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.login_page = LoginPage()
        self.main_page = MainPage()

        self.addWidget(self.login_page)
        self.addWidget(self.main_page)

        self.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
