from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter, QAbstractItemView
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

        # Create the "Add 3D object" button
        self.button = QPushButton("Add 3D object")
        self.button.clicked.connect(self.open_file_dialog)

        # Create the "Delete object" button
        self.delete_button = QPushButton("Delete object")
        self.delete_button.clicked.connect(self.delete_selected_object)

        # Create the VisPy canvas
        self.vispy_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        self.update_visualization()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Type", "Name", "Points", "Faces"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table()

        # Right pannel
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.button)
        splitter1.addWidget(QWidget())
        splitter1.setSizes([1, 10000])

        # Left pannel
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.table_widget)
        splitter2.addWidget(self.delete_button)
        splitter2.setSizes([10000, 1])

        # All
        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(splitter2)
        splitter3.addWidget(self.vispy_canvas.native)
        splitter3.addWidget(splitter1)
        splitter3.setSizes([1, 10000, 1])

        # Set the splitter as the central widget
        self.setCentralWidget(splitter3)

    def open_file_dialog(self):
        """
        Opens a file dialog to select an OBJ file.

        Returns:
            str: The selected file name.
        """
        file_names, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "resources/obj", "OBJ Files (*.obj)")
        for file_name in file_names:
            if file_name:
                # Create a new Polyhedron from the OBJ file
                polyhedron = Polyhedron(file_name)
                
                # Add the Polyhedron to the Scene
                self.scene.add_object(polyhedron)

        # Update the visualization and the table
        self.update()

    def update_visualization(self):
        """
        Updates the visualization of the scene in the VisPy canvas.
        """
        self.scene.vispy_display(self.vispy_canvas)

    def update_table(self):
        """
        Updates the table widget with information about the objects in the scene.
        """
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.scene.objects))
        for row, polyhedron in enumerate(self.scene.objects):
            self.table_widget.setItem(row, 0, QTableWidgetItem(type(polyhedron).__name__))
            self.table_widget.setItem(row, 1, QTableWidgetItem(polyhedron.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(len(polyhedron.vertices))))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(len(polyhedron.faces))))
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        width = sum(self.table_widget.columnWidth(i) + 1 for i in range(self.table_widget.columnCount()))
        width += self.table_widget.verticalHeader().width()
        if self.table_widget.rowCount() > 0:
            width += 12
        self.table_widget.setMinimumWidth(width)

    def update(self):
        """
        Updates the visualization and the table.
        """
        self.update_visualization()
        self.update_table()

    def delete_selected_object(self):
        """
        Deletes the currently selected objects from the scene and the table.
        """
        selected_rows = sorted(set(index.row() for index in self.table_widget.selectedIndexes()), reverse=True)
        for row in selected_rows:
            # Remove the object from the scene
            self.scene.remove_object(row)

        # Update the visualization and the table
        self.update()

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