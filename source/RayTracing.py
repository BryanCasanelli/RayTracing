from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
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
        self.button = QPushButton("Add 3D file")
        self.button.clicked.connect(self.open_file_dialog)

        # Create the VisPy canvas
        self.vispy_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')

        # Create the vertical layout and add the widgets
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.vispy_canvas.native)

        # Create a container widget and set the layout
        widget = QWidget()
        widget.setLayout(layout)

        # Set the container widget as the central widget
        self.setCentralWidget(widget)

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

    def update_visualization(self):
        """
        Updates the visualization of the scene in the VisPy canvas.
        """
        self.scene.vispy_display(self.vispy_canvas)

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