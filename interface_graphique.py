import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQtGraph Example")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create three plot windows
        self.plot1 = pg.PlotWidget(title="Plot 1")
        self.plot2 = pg.PlotWidget(title="Plot 2")
        self.plot3 = pg.PlotWidget(title="Plot 3")

        layout.addWidget(self.plot1)
        layout.addWidget(self.plot2)
        layout.addWidget(self.plot3)

        # Example data
        x = [1, 2, 3, 4, 5]
        y1 = [10, 20, 30, 40, 50]
        y2 = [50, 40, 30, 20, 10]
        y3 = [10, 30, 20, 40, 50]

        # Plot data
        self.plot1.plot(x, y1, pen='r')
        self.plot2.plot(x, y2, pen='g')
        self.plot3.plot(x, y3, pen='b')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())