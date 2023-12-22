from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter, QAbstractItemView, QDialog, QDoubleSpinBox, QGridLayout, QLabel, QSizePolicy, QComboBox, QFormLayout, QProgressBar
from Scene import Scene
from Polyhedron import Polyhedron
from vispy import scene

test = True
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

        # Test only, insert the cup and the cube into the scene
        if test:
            self.scene.add_object(Polyhedron("resources/obj/cup.obj"))
            self.scene.add_object(Polyhedron("resources/obj/cube.obj"))

        # Create the author label
        self.author_label = QLabel("By Bryan Casanelli - bryancasanelli@gmail.com")
        self.author_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.author_label.setAlignment(Qt.AlignCenter)

        # Create the "Add object" button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.open_file_dialog)

        # Create the "Delete object" button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_object)

        # Create the "Move object" button
        self.move_button = QPushButton("Move")
        self.move_button.clicked.connect(self.move_selected_object)

        # Create the "Change reference point" button
        self.change_ref_button = QPushButton("Change reference point")
        self.change_ref_button.clicked.connect(self.change_reference_point)

        # Create the VisPy canvas
        self.vispy_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        self.update_visualization()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.itemSelectionChanged.connect(self.update_buttons_state)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Type", "Name", "Points", "Faces", "X [mm]", "Y [mm]", "Z [mm]"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table()

        # Create the progress bar
        self.progress_bar = QProgressBar()

        # Buttons pannel
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(1)
        self.buttons_layout.addWidget(self.add_button)
        self.buttons_layout.addWidget(self.delete_button)
        self.buttons_layout.addWidget(self.move_button)
        self.buttons_layout.addWidget(self.change_ref_button)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)

        # Left pannel
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.buttons_widget)
        splitter1.addWidget(self.table_widget)
        splitter1.addWidget(self.progress_bar)
        splitter1.setSizes([1, 10000, 1])

        # Left pannel + VisPy canvas
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.vispy_canvas.native)
        splitter2.setSizes([1, 10000])

        # All + author
        all_layout = QVBoxLayout()
        all_layout.setSpacing(5)
        all_layout.setContentsMargins(10, 10, 10, 5)
        all_layout.addWidget(splitter2)
        all_layout.addWidget(self.author_label)
        all_widget = QWidget()
        all_widget.setLayout(all_layout)

        # Set the splitter as the central widget
        self.setCentralWidget(all_widget)

        # Update the state of the buttons
        self.update_buttons_state()

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
            self.table_widget.setItem(row, 4, QTableWidgetItem(format(polyhedron.reference.x, '.2f')))
            self.table_widget.setItem(row, 5, QTableWidgetItem(format(polyhedron.reference.y, '.2f')))
            self.table_widget.setItem(row, 6, QTableWidgetItem(format(polyhedron.reference.z, '.2f')))
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

    def update_buttons_state(self):
        """
        Updates the state of the buttons based on the selection in the table widget.
        """
        if self.table_widget.selectedItems():
            self.delete_button.setEnabled(True)
            self.move_button.setEnabled(True)
            self.change_ref_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)
            self.move_button.setEnabled(False)
            self.change_ref_button.setEnabled(False)

    def move_selected_object(self):
        """
        Moves the currently selected objects based on user input.
        """
        dialog = MoveObjectDialog(self)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            dx, dy, dz = dialog.get_values()
            selected_rows = sorted(set(index.row() for index in self.table_widget.selectedIndexes()))
            for row in selected_rows:
                # Move the object in the scene
                self.scene.objects[row].translate(dx, dy, dz)

        # Update the visualization and the table
        self.update()

    def change_reference_point(self):
        """
        Opens a dialog to change the reference point.
        """
        selected_rows = sorted(set(index.row() for index in self.table_widget.selectedIndexes()))
        dialog = ChangeReferencePointDialog(self)
        if len(selected_rows) == 1:
                reference = self.scene.objects[selected_rows[0]].reference
                dialog.set_default_values(reference.x, reference.y, reference.z)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            ref_type, axis, x, y, z = dialog.get_values()
            for row in selected_rows:
                # Change the reference point
                self.scene.objects[row].change_reference_point(ref_type, axis, x, y, z)

        # Update the visualization and the table
        self.update()

class ChangeReferencePointDialog(QDialog):
    """
    A dialog window for changing the reference point.

    Methods:
        __init__(self, parent=None): Initializes the ChangeReferencePointDialog.
        set_default_values(self, default_x, default_y, default_z): Sets the default values for the spin boxes.
        get_values(self): Returns the selected reference type and axis.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Change reference point")

        self.ref_type_combo_box = QComboBox(self)
        self.ref_type_combo_box.addItems(["Lowest", "Highest", "Manual"])
        self.ref_type_combo_box.currentTextChanged.connect(self.update_axis_combo_box)

        self.axis_combo_box = QComboBox(self)
        self.axis_combo_box.addItems(["x", "y", "z"])

        self.x_spin_box = QDoubleSpinBox(self)
        self.x_spin_box.setDecimals(2)
        self.x_spin_box.setRange(-float('inf'), float('inf'))
        self.x_spin_box.setMinimumWidth(70)

        self.y_spin_box = QDoubleSpinBox(self)
        self.y_spin_box.setDecimals(2)
        self.y_spin_box.setRange(-float('inf'), float('inf'))
        self.y_spin_box.setMinimumWidth(70)

        self.z_spin_box = QDoubleSpinBox(self)
        self.z_spin_box.setDecimals(2)
        self.z_spin_box.setRange(-float('inf'), float('inf'))
        self.z_spin_box.setMinimumWidth(70)

        form_layout = QFormLayout()
        form_layout.addRow("Reference type :", self.ref_type_combo_box)
        form_layout.addRow("Axis :", self.axis_combo_box)
        form_layout.addRow("X [mm] :", self.x_spin_box)
        form_layout.addRow("Y [mm] :", self.y_spin_box)
        form_layout.addRow("Z [mm] :", self.z_spin_box)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.ref_type_combo_box.setCurrentIndex(1)
        self.ref_type_combo_box.setCurrentIndex(0)

    def set_default_values(self, default_x, default_y, default_z):
        """
        Sets the default values for the spin boxes.

        Args:
            default_x (float): The default value for the x spin box.
            default_y (float): The default value for the y spin box.
            default_z (float): The default value for the z spin box.
        """
        self.x_spin_box.setValue(default_x)
        self.y_spin_box.setValue(default_y)
        self.z_spin_box.setValue(default_z)

    def get_values(self):
        """
        Get the values from the GUI elements.

        Returns:
            tuple: A tuple containing the current text of the reference type combo box,
                    the current text of the axis combo box, and the values of the x, y, and z spin boxes.
        """
        return self.ref_type_combo_box.currentText(), self.axis_combo_box.currentText(), self.x_spin_box.value(), self.y_spin_box.value(), self.z_spin_box.value()

    def update_axis_combo_box(self, text):
        """
        Enables or disables the axis combo box based on the current text of the reference type combo box.

        Args:
            text (str): The current text of the reference type combo box.
        """
        if text == "Manual":
            self.axis_combo_box.setEnabled(False)
            self.x_spin_box.setEnabled(True)
            self.y_spin_box.setEnabled(True)
            self.z_spin_box.setEnabled(True)
        else:
            self.axis_combo_box.setEnabled(True)
            self.x_spin_box.setEnabled(False)
            self.y_spin_box.setEnabled(False)
            self.z_spin_box.setEnabled(False)

class MoveObjectDialog(QDialog):
    """
    A dialog window for moving an object in a 3D space.

    Methods:
        __init__(self, parent=None): Initializes the MoveObjectDialog.
        get_values(self): Returns the entered displacement values as floats.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Move object")

        self.dx_spin_box = QDoubleSpinBox()
        self.dx_spin_box.setDecimals(2)
        self.dx_spin_box.setRange(-float('inf'), float('inf'))
        self.dx_spin_box.setFixedWidth(70)

        self.dy_spin_box = QDoubleSpinBox()
        self.dy_spin_box.setDecimals(2)
        self.dy_spin_box.setRange(-float('inf'), float('inf'))
        self.dy_spin_box.setFixedWidth(70)

        self.dz_spin_box = QDoubleSpinBox()
        self.dz_spin_box.setDecimals(2)
        self.dz_spin_box.setRange(-float('inf'), float('inf'))
        self.dz_spin_box.setFixedWidth(70)

        form_layout = QFormLayout()
        form_layout.addRow("dx [mm] :", self.dx_spin_box)
        form_layout.addRow("dy [mm] :", self.dy_spin_box)
        form_layout.addRow("dz [mm] :", self.dz_spin_box)

        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_values(self):
        """
        Returns the entered displacement values as floats.

        Returns:
            Tuple[float, float, float]: The displacement values entered in the dialog.
        """
        return float(self.dx_spin_box.value()), float(self.dy_spin_box.value()), float(self.dz_spin_box.value())


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