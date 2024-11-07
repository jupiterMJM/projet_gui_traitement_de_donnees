import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog
import pyqtgraph as pg
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
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
        file_button = QPushButton("Choose Scan of bottle 1 and 2")
        info_layout.addWidget(file_button)
        file_button.clicked.connect(self.open_file_dialog)

        self.calib_alpha = QLineEdit(text="alpha")
        info_layout.addWidget(self.calib_alpha)

        self.calib_V0 = QLineEdit(text="V0")
        info_layout.addWidget(self.calib_V0)

        self.calib_t0 = QLineEdit(text="t0")
        info_layout.addWidget(self.calib_t0)

        submit_button = QPushButton("Submit")
        info_layout.addWidget(submit_button)
        submit_button.clicked.connect(self.button_callback)

        

        

        # Create three plot windows
        plot_layout = QVBoxLayout()
        content_layout.addLayout(plot_layout)
        self.plot1 = pg.PlotWidget(title="Bottle 1")
        self.plot2 = pg.PlotWidget(title="Bottle 1 x Theory")
        self.plot3 = pg.PlotWidget(title="Bottle 2")

        plot_layout.addWidget(self.plot1)
        plot_layout.addWidget(self.plot2)
        plot_layout.addWidget(self.plot3)

    def button_callback(self):
        # Get the information entered by the user
        alpha = self.calib_alpha.text()
        V0 = self.calib_V0.text()
        t0 = self.calib_t0.text()

    def open_file_dialog(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_path, _ = QFileDialog.getOpenFileName(self, "Choose File", "", "All Files (*);;Text Files (*.txt)", options=options)
            if file_path:
                print(f"Selected file: {file_path}")
        


    def plot(self, data_tof_1, data_tof_1_theory, data_tof_2):
        """
        data_tof_1: tuple (energy_axis, signal_E) for bottle 1
        data_tof_1_theory: tuple (energy_axis, signal_E) for bottle 1 x Theory
        data_tof_2: tuple (energy_axis, signal_E) for bottle 2
        """
        # Plot data
        self.plot1.plot(data_tof_1[0], data_tof_1[1], pen='r')
        self.plot2.plot(data_tof_1_theory[0], data_tof_1_theory[1], pen='g')
        self.plot3.plot(data_tof_2[0], data_tof_2[1], pen='b')

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())