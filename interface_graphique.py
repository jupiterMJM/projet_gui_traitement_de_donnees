import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog, QMessageBox
import pyqtgraph as pg
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from ouverture_et_traitement_de_fichier import *

class MainWindow(QMainWindow):
    def __init__(self):
        self.file_to_data = None
        self.file_to_calib = None
        super().__init__()

        self.setWindowTitle("Comparaison de bouteilles magnétiques")
        self.setGeometry(100, 100, 1000, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Add a column on the right for entering diverse information
        info_layout = QVBoxLayout()
        content_layout.addLayout(info_layout)

        # Add widgets for entering information (e.g., QLineEdit, QLabel)

        info_label = QLabel("Enter Information:")
        info_layout.addWidget(info_label)

        # Add a button to open a file dialog
        self.file_button = QPushButton("Choose Scan of bottle 1 and 2")
        self.file_button.setStyleSheet("background-color: lightcoral")
        info_layout.addWidget(self.file_button)
        self.file_button.clicked.connect(self.open_file_dialog)

        self.what_s_bottle2 = QLineEdit("What's in bottle 2?")
        info_layout.addWidget(self.what_s_bottle2)

        self.calib_button = QPushButton("Choose Calibration File")
        self.calib_button.setStyleSheet("background-color: lightcoral")
        info_layout.addWidget(self.calib_button)
        self.calib_button.clicked.connect(self.open_file_dialog_bis)

        submit_button = QPushButton("Submit")
        info_layout.addWidget(submit_button)
        submit_button.clicked.connect(self.button_callback)


        # Create three plot windows
        plot_layout = QVBoxLayout()
        content_layout.addLayout(plot_layout)
        self.plot1 = pg.PlotWidget(title="Bottle 1")
        self.plot2 = pg.PlotWidget(title="Bottle 1 x Theory")
        self.plot3 = pg.PlotWidget(title="Bottle 2")

        # link x-axes between plots
        self.plot2.setXLink(self.plot1)
        self.plot3.setXLink(self.plot1)

        self.plot1.enableAutoRange(axis='y')
        self.plot2.enableAutoRange(axis='y')
        self.plot3.enableAutoRange(axis='y')

        self.plot1.setMouseEnabled(y=False)
        self.plot2.setMouseEnabled(y=False)
        self.plot3.setMouseEnabled(y=False)

        plot_layout.addWidget(self.plot1)
        plot_layout.addWidget(self.plot2)
        plot_layout.addWidget(self.plot3)

    def button_callback(self):
        data_tof_1, data_tof_2, data_tof_theory = None, None, None

        if self.file_to_data == None and self.file_to_calib == None and self.what_s_bottle2.text() not in ("liquid", "gas", "solid"):
            self.show_error_message("Please select a file and enter the information")
            return
        # Get the information entered by the user
        calib1, calib2 = extract_config_file(self.file_to_calib, what_s_in_bottle2=self.what_s_bottle2.text())

        # Call the function that processes the data
        data_tof_1, data_tof_2 = ouverture_data_tof(self.file_to_data)
        data_tof_1 = calibration_tof(data_tof_1, calib1["alpha"], calib1["t0"], calib1["V0"])
        data_tof_2 = calibration_tof(data_tof_2, calib2["alpha"], calib2["t0"], calib2["V0"])

        # Plot the data
        self.plot(data_tof_1, data_tof_theory, data_tof_2)

    def show_error_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    def open_file_dialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Text Files (*.txt)", options=options)
            if file_path:
                print(f"Selected file: {file_path}")
                self.file_to_data = file_path
            self.file_button.setStyleSheet("background-color: lightgreen")
        
    def open_file_dialog_bis(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Text Files (*.txt)", options=options)
            if file_path:
                print(f"Selected file: {file_path}")
                self.file_to_calib = file_path
            self.calib_button.setStyleSheet("background-color: lightgreen")

    def plot(self, data_tof_1, data_tof_1_theory, data_tof_2):
        """
        data_tof_1: tuple (energy_axis, signal_E) for bottle 1
        data_tof_1_theory: tuple (energy_axis, signal_E) for bottle 1 x Theory
        data_tof_2: tuple (energy_axis, signal_E) for bottle 2
        """
        # Plot data
        if data_tof_1: self.plot1.plot(data_tof_1[0], data_tof_1[1], pen='r')
        if data_tof_1_theory: self.plot2.plot(data_tof_1_theory[0], data_tof_1_theory[1], pen='g')
        if data_tof_2: self.plot3.plot(data_tof_2[0], data_tof_2[1], pen='b')

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())