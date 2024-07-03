import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class KneeSpaApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(KneeSpaApp, self).__init__()
        uic.loadUi("kneespa.ui", self)

        # Initialize table widget
        self.table_widget = self.findChild(
            QtWidgets.QTableWidget, "patient_table_widget"
        )
        if self.table_widget:
            self.table_widget.verticalHeader().setVisible(True)

        # Stacked widget pages
        self.home_page = 0
        self.main_page = 1
        self.help_page = 2
        self.profile_page = 3

        # Buttons
        self.protocols_button = self.findChild(
            QtWidgets.QPushButton, "protocols_button"
        )
        self.help_button = self.findChild(QtWidgets.QPushButton, "help_button")
        self.login_button = self.findChild(QtWidgets.QPushButton, "login_button")
        self.start_button = self.findChild(QtWidgets.QPushButton, "push_button_start")
        self.enter_patient_button = self.findChild(
            QtWidgets.QPushButton, "enter_patient_pin_button"
        )

        # Labels acting as buttons
        self.profile_button = self.findChild(QtWidgets.QLabel, "profile_button")
        self.video_player_button = self.findChild(
            QtWidgets.QLabel, "video_player_button"
        )
        self.brand_label = self.findChild(QtWidgets.QLabel, "top_nav_brand_label")
        self.brand_logo = self.findChild(QtWidgets.QLabel, "top_nav_logo")

        # User information labels
        self.username_nav = self.findChild(QtWidgets.QLabel, "username_nav")
        self.username_profile = self.findChild(QtWidgets.QLabel, "username_field")
        self.email_profile = self.findChild(QtWidgets.QLabel, "email_field")
        self.status_profile = self.findChild(QtWidgets.QLabel, "status_field")

        # Protocol image controls
        self.label_protocol_image = self.findChild(
            QtWidgets.QLabel, "label_protocol_image"
        )
        self.protocol_image_number = self.findChild(
            QtWidgets.QLineEdit, "protocol_number_field"
        )
        self.forward_button_protocol_image = self.findChild(
            QtWidgets.QLabel, "forward_button_protocol_image"
        )
        self.backward_button_protocol_image = self.findChild(
            QtWidgets.QLabel, "backward_button_protocol_image"
        )

        # Initialize protocol image
        self.current_image_number = 1
        self.update_protocol_image()

        # Connect protocol image navigation buttons
        self.forward_button_protocol_image.mousePressEvent = (
            self.show_next_protocol_image
        )
        self.backward_button_protocol_image.mousePressEvent = (
            self.show_previous_protocol_image
        )

        # Pressure field controls
        self.pressure_field = self.findChild(QtWidgets.QLineEdit, "pressure_field")
        self.plus_label_pressure = self.findChild(
            QtWidgets.QLabel, "plus_label_pressure"
        )
        self.minus_label_pressure = self.findChild(
            QtWidgets.QLabel, "minus_label_pressure"
        )

        # Initialize pressure field
        self.current_pressure = 40
        self.update_pressure_field()

        # Connect pressure field navigation buttons
        self.plus_label_pressure.mousePressEvent = self.increase_pressure
        self.minus_label_pressure.mousePressEvent = self.decrease_pressure

        # Leg length field controls
        self.leg_length_field = self.findChild(QtWidgets.QLineEdit, "leg_length_field")
        self.plus_label_leg_length = self.findChild(
            QtWidgets.QLabel, "plus_label_leg_length"
        )
        self.minus_label_leg_length = self.findChild(
            QtWidgets.QLabel, "minus_label_leg_length"
        )

        # Initialize leg length field
        self.current_leg_length = 6.0
        self.update_leg_length_field()

        # Connect leg length field navigation buttons
        self.plus_label_leg_length.mousePressEvent = self.increase_leg_length
        self.minus_label_leg_length.mousePressEvent = self.decrease_leg_length

        # Connect buttons to functions if they are found
        if self.protocols_button:
            self.protocols_button.clicked.connect(self.show_main_page)
        else:
            print("Error: 'protocols_button' not found")

        if self.help_button:
            self.help_button.clicked.connect(self.show_help_page)
        else:
            print("Error: 'help_button' not found")

        if self.login_button:
            self.login_button.clicked.connect(self.show_login_dialog)
        else:
            print("Error: 'login_button' not found")

        if self.start_button:
            self.start_button.clicked.connect(self.start_or_stop_protocol)
        else:
            print("Error: 'start_button' not found")

        if self.enter_patient_button:
            self.enter_patient_button.clicked.connect(self.show_enter_patient_dialog)
        else:
            print("Error: 'enter_patient_pin_button' not found")

        if self.profile_button:
            self.profile_button.mousePressEvent = self.show_profile_page
        else:
            print("Error: 'profile_button' not found")

        if self.video_player_button:
            self.video_player_button.mousePressEvent = self.show_video_player_dialog
        else:
            print("Error: 'video_player_button' not found")

        if self.brand_label:
            self.brand_label.mousePressEvent = self.return_to_home_page
        else:
            print("Error: 'brand_label' not found")

        if self.brand_logo:
            self.brand_logo.mousePressEvent = self.return_to_home_page
        else:
            print("Error: 'brand_logo' not found")

        # Check and print any QLabel stylesheets issues
        for label_name in [
            "label_15",
            "label_16",
            "label_17",
            "label_18",
            "label_19",
            "label_20",
        ]:
            label = self.findChild(QtWidgets.QLabel, label_name)
            if label is not None:
                if not label.styleSheet():
                    print(
                        f"Could not parse stylesheet of object QLabel(name = '{label_name}')"
                    )
            else:
                print(f"QLabel '{label_name}' not found")

        # Set the initial page to home_page
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.home_page
        )

        # Initialize the login dialog
        self.login_dialog = None
        self.init_login_dialog()

    def update_protocol_image(self):
        image_path = (
            f"images/graphics/protocol-graphics/{self.current_image_number}.png"
        )
        self.label_protocol_image.setPixmap(QPixmap(image_path))
        self.protocol_image_number.setText(str(self.current_image_number))

    def show_next_protocol_image(self, event):
        if self.current_image_number < 18:
            self.current_image_number += 1
            self.update_protocol_image()

    def show_previous_protocol_image(self, event):
        if self.current_image_number > 1:
            self.current_image_number -= 1
            self.update_protocol_image()

    def update_pressure_field(self):
        self.pressure_field.setText(f"{self.current_pressure} lbs")

    def increase_pressure(self, event):
        if self.current_pressure < 100:
            self.current_pressure += 5
            self.update_pressure_field()

    def decrease_pressure(self, event):
        if self.current_pressure > 0:
            self.current_pressure -= 5
            self.update_pressure_field()

    def update_leg_length_field(self):
        self.leg_length_field.setText(f"{self.current_leg_length:.1f} in")

    def increase_leg_length(self, event):
        if self.current_leg_length < 18:
            self.current_leg_length += 0.5
            self.update_leg_length_field()

    def decrease_leg_length(self, event):
        if self.current_leg_length > 0:
            self.current_leg_length -= 0.5
            self.update_leg_length_field()

    def start_or_stop_protocol(self):
        if self.start_button.text() == "Start":
            self.start_button.setText("Stop")
            self.start_button.setStyleSheet(
                "background-color: rgb(200, 0, 0);"
                "color: white;"
                "border: none;"
                "text-decoration: none;"
                "margin: 0px 15px;"
                "font-size: 20px;"
                "font-weight: bold;"
                "border-radius: 8px;"
            )
        else:
            self.start_button.setText("Start")
            self.start_button.setStyleSheet(
                "background-color: rgb(0, 200, 0);"
                "color: white;"
                "border: none;"
                "text-decoration: none;"
                "margin: 0px 15px;"
                "font-size: 20px;"
                "font-weight: bold;"
                "border-radius: 8px;"
            )

    def show_login_dialog(self):
        self.login_dialog.exec_()

    def init_login_dialog(self):
        self.login_dialog = QtWidgets.QDialog(self)
        uic.loadUi("login.ui", self.login_dialog)
        self.login_dialog.adjustSize

        self.login_line_edit = self.login_dialog.findChild(
            QtWidgets.QLineEdit, "password_line_edit"
        )
        self.login_help_button = self.login_dialog.findChild(
            QtWidgets.QPushButton, "login_help_button"
        )
        self.login_enter_button = self.login_dialog.findChild(
            QtWidgets.QPushButton, "enter_password_button"
        )
        self.login_clear_button = self.login_dialog.findChild(
            QtWidgets.QPushButton, "clear_password_button"
        )

        self.login_help_button.clicked.connect(self.show_help_dialog)
        self.login_enter_button.clicked.connect(self.handle_login)
        self.login_clear_button.clicked.connect(self.clear_line_edit)

        for i in range(10):
            button = self.login_dialog.findChild(
                QtWidgets.QPushButton, f"pushButton_{i}"
            )
            if button:
                button.clicked.connect(lambda _, x=str(i): self.append_star(x))

    def append_star(self, value):
        self.login_line_edit.setText(self.login_line_edit.text() + "*")

    def clear_line_edit(self):
        self.login_line_edit.clear()

    def show_help_dialog(self):
        help_dialog = QtWidgets.QDialog(self)
        uic.loadUi("login-help.ui", help_dialog)
        help_dialog.exec_()

    def handle_login(self):
        if self.login_line_edit.text() == "***":  # Assuming '123' was entered as '***'
            self.login_line_edit.clear()
            self.username_nav.setText("user.lastname")
            self.username_profile.setText("user.lastname")
            self.email_profile.setText("user.lastname@outlook.com")
            self.status_profile.setText("Admin")
            self.login_button.setText("Logout")
            self.login_button.clicked.disconnect()
            self.login_button.clicked.connect(self.handle_logout)
            self.login_dialog.accept()

    def handle_logout(self):
        self.username_nav.setText("")
        self.username_profile.setText("")
        self.email_profile.setText("")
        self.status_profile.setText("")
        self.login_button.setText("Login")
        self.login_button.clicked.disconnect()
        self.login_button.clicked.connect(self.show_login_dialog)

        # Reset the page to home_page
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.home_page
        )

    def show_home_page(self):
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.home_page
        )

    def return_to_home_page(self, event):
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.home_page
        )

    def show_main_page(self):
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.main_page
        )
        if self.findChild(QtWidgets.QTabWidget, "DRx_tabs"):
            self.findChild(QtWidgets.QTabWidget, "DRx_tabs").setCurrentIndex(0)

    def show_help_page(self):
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.help_page
        )

    def show_profile_page(self, event):
        self.findChild(QtWidgets.QStackedWidget, "stackedWidget").setCurrentIndex(
            self.profile_page
        )

    def show_enter_patient_dialog(self):
        enter_patient_dialog = QtWidgets.QDialog(self)
        uic.loadUi("enter-patient.ui", enter_patient_dialog)
        enter_patient_dialog.adjustSize()
        enter_patient_dialog.exec_()

    def show_video_player_dialog(self, event):
        video_player_dialog = QtWidgets.QDialog(self)
        uic.loadUi("video-player.ui", video_player_dialog)
        video_player_dialog.adjustSize()
        video_player_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = KneeSpaApp()
    window.show()
    sys.exit(app.exec_())
