from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter
from Scene import Scene
from Polyhedron import Polyhedron
from vispy import scene

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initializes the main window of the Ray Tracing application.
        """
        super().__init__()

        # Set the window title
        self.setWindowTitle("Ray Tracing")

        # Create a Scene instance
        self.scene = Scene()

        # Create the "Open 3D file" button
        self.button = QPushButton("Add 3D object")
        self.button.clicked.connect(self.open_file_dialog)

        # Create the VisPy canvas
        self.vispy_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        self.update_visualization()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Type", "Name", "Points", "Faces"])
        self.set_table_size()

        # Table + VisPy canvas
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.table_widget)
        splitter1.addWidget(self.vispy_canvas.native)
        splitter1.setSizes([1, 10000])

        # Add 3d object button  + (Table + VisPy canvas)
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.button)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([1, 10000])

        # Set the splitter as the central widget
        self.setCentralWidget(splitter2)

    def open_file_dialog(self):
        """
        Opens a file dialog to select an OBJ file.

        Returns:
            str: The selected file name.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "resources/obj", "OBJ Files (*.obj)")
        if file_name:
            # Create a new Polyhedron from the OBJ file
            polyhedron = Polyhedron(file_name)
            
            # Add the Polyhedron to the Scene
            self.scene.add_object(polyhedron)

            # Update the visualization
            self.update_visualization()

            # Add the Polyhedron to the table
            row = self.table_widget.rowCount()
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(type(polyhedron).__name__))
            self.table_widget.setItem(row, 1, QTableWidgetItem(polyhedron.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(len(polyhedron.vertices))))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(len(polyhedron.faces))))
            self.set_table_size()

    def update_visualization(self):
        """
        Updates the visualization of the scene in the VisPy canvas.
        """
        self.scene.vispy_display(self.vispy_canvas)

    def set_table_size(self):
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        width = sum(self.table_widget.columnWidth(i)+1 for i in range(self.table_widget.columnCount()))
        width += self.table_widget.verticalHeader().width()
        if self.table_widget.rowCount() > 0:
            width += 12
        self.table_widget.setMinimumWidth(width)

def main():
    """
    The main function of the RayTracing program.
    Initializes the application, creates the main window, and starts the event loop.
    """
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec_()

if __name__ == "__main__":
    main()