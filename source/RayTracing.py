from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem, QHBoxLayout, QSplitter, QAbstractItemView, QDialog, QDoubleSpinBox, QGridLayout, QLabel, QSizePolicy, QComboBox, QFormLayout, QProgressBar, QCheckBox, QFrame
from Scene import Scene
from Polyhedron import Polyhedron
from Point import Point
from Vector import Vector
from RaySource import RaySource
from RectangularPlanarPolygon import RectangularPlanarPolygon
from vispy import scene
from pathlib import Path

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
            self.scene.add_object(Polyhedron("resources/obj/sphere.obj"))

        # Initialize the last used directory
        self.last_used_directory = None

        # Create the author label
        self.author_label = QLabel("By Bryan Casanelli - bryancasanelli@gmail.com")
        self.author_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.author_label.setAlignment(Qt.AlignCenter)

        # Create the "Add object" button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.show_add_dialog)

        # Create the "Delete object" button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_selected_object)

        # Create the "Move object" button
        self.move_button = QPushButton("Move")
        self.move_button.clicked.connect(self.move_selected_object)

        # Create the "Change reference point" button
        self.change_ref_button = QPushButton("Change reference point")
        self.change_ref_button.clicked.connect(self.change_reference_point)

        # Add "select material" button
        self.select_material_button = QPushButton("Select material")
        self.select_material_button.clicked.connect(self.show_material_dialog)

        # Add "save" button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        # Add "load" button
        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load)

        # Create the show/hide polyhedrons button
        self.show_polyhedrons = QCheckBox("Show polyhedrons")
        self.show_polyhedrons.setChecked(True)
        self.show_polyhedrons.stateChanged.connect(self.update_visualization)

        # Create the VisPy canvas
        self.vispy_canvas = scene.SceneCanvas(keys='interactive', bgcolor='white')
        self.vispy_canvas.native.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.update_visualization()

        # Create the table widget
        self.table_widget = QTableWidget()
        self.table_widget.itemSelectionChanged.connect(self.update_buttons_state)
        self.table_widget.setColumnCount(11)
        self.table_widget.setHorizontalHeaderLabels(["Type", "Name", "Points", "Faces", "X [mm]", "Y [mm]", "Z [mm]", "Material", "Nx [mm]", "Ny [mm]", "Nz [mm]"])
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.update_table()

        # Create the simulation button
        self.simulate_button = QPushButton("Simulate")
        self.simulate_button.clicked.connect(self.simulate)

        # Create the progress bar
        self.progress_bar = QProgressBar()

        # Left pannel
        self.left_pannel_layout = QVBoxLayout()
        self.left_pannel_layout.setSpacing(5)
        self.left_pannel_layout.setContentsMargins(0, 0, 0, 0)
        self.left_pannel_layout.addWidget(self.add_button)
        self.left_pannel_layout.addWidget(self.delete_button)
        self.left_pannel_layout.addWidget(self.move_button)
        self.left_pannel_layout.addWidget(self.change_ref_button)
        self.left_pannel_layout.addWidget(self.select_material_button)
        self.left_pannel_layout.addWidget(self.save_button)
        self.left_pannel_layout.addWidget(self.load_button)
        self.left_pannel_layout.addWidget(self.table_widget)
        self.left_pannel_layout.addWidget(self.simulate_button)
        self.left_pannel_layout.addWidget(self.progress_bar)
        self.left_pannel_widget = QWidget()
        self.left_pannel_widget.setLayout(self.left_pannel_layout)

        # Upper pannel
        self.upper_pannel_layout = QHBoxLayout()
        self.upper_pannel_layout.setContentsMargins(0, 0, 0, 0)
        self.upper_pannel_layout.addWidget(self.show_polyhedrons)
        self.upper_pannel_layout.addStretch()
        self.upper_pannel_widget = QWidget()
        self.upper_pannel_widget.setLayout(self.upper_pannel_layout)

        # Upper pannel + VisPy canvas
        self.plot_layout = QVBoxLayout()
        self.plot_layout.setSpacing(5)
        self.plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_layout.addWidget(self.upper_pannel_widget)
        self.plot_layout.addWidget(self.vispy_canvas.native)
        self.plot_widget = QWidget()
        self.plot_widget.setLayout(self.plot_layout)

        # Left + Plot
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.left_pannel_widget)
        splitter.addWidget(self.plot_widget)
        splitter.setSizes([1, 10000])

        # All + author
        all_layout = QVBoxLayout()
        all_layout.setSpacing(5)
        all_layout.setContentsMargins(10, 10, 10, 5)
        all_layout.addWidget(splitter)
        all_layout.addWidget(self.author_label)
        all_widget = QWidget()
        all_widget.setLayout(all_layout)

        # Set the splitter as the central widget
        self.setCentralWidget(all_widget)

        # Update the state of the buttons
        self.update_buttons_state()

    def update_visualization(self):
        """
        Updates the visualization of the scene in the VisPy canvas.
        """
        show_polyhedrons = self.show_polyhedrons.isChecked()
        self.scene.vispy_display(self.vispy_canvas, show_polyhedrons)

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
            if isinstance(polyhedron, Polyhedron):
                self.table_widget.setItem(row, 7, QTableWidgetItem(polyhedron.material.name))
                self.table_widget.setItem(row, 8, QTableWidgetItem("---"))
                self.table_widget.setItem(row, 9, QTableWidgetItem("---"))
                self.table_widget.setItem(row, 10, QTableWidgetItem("---"))
            else:
                self.table_widget.setItem(row, 7, QTableWidgetItem("---"))
                self.table_widget.setItem(row, 8, QTableWidgetItem(format(polyhedron.normal.x, '.2f')))
                self.table_widget.setItem(row, 9, QTableWidgetItem(format(polyhedron.normal.x, '.2f')))
                self.table_widget.setItem(row, 10, QTableWidgetItem(format(polyhedron.normal.x, '.2f')))
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        width = sum(self.table_widget.columnWidth(i) + 1 for i in range(self.table_widget.columnCount()))
        width += self.table_widget.verticalHeader().width()
        if self.table_widget.rowCount() > 0:
            width += 0
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
            
            # Check if any selected item is not a Polyhedron
            selected_rows = set(index.row() for index in self.table_widget.selectedIndexes())
            non_polyhedron_selected = any(not isinstance(self.scene.objects[row], Polyhedron) for row in selected_rows)
            
            # Special case for non-polyhedron objects
            if non_polyhedron_selected:
                self.select_material_button.setEnabled(False)
            else:
                self.select_material_button.setEnabled(True)
        else:
            self.delete_button.setEnabled(False)
            self.move_button.setEnabled(False)
            self.change_ref_button.setEnabled(False)
            self.select_material_button.setEnabled(False)

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
    
    def show_material_dialog(self):
        """
        Shows a dialog with a combo box to select the material for the selected rows of the table.
        """
        # Get the selected rows
        selected_rows = sorted(set(index.row() for index in self.table_widget.selectedIndexes()))
        # Get the current material of the selected rows
        current_material = set()
        for row in selected_rows:
            current_material.add(self.scene.objects[row].material.name)
        if len(current_material) == 1:
            current_material = current_material.pop()
        else:
            current_material = None
        # Create the dialog
        dialog = ChangeMaterialDialog(self, current_material)
        # Show the dialog and get the selected material
        if dialog.exec_() == QDialog.Accepted:
            material_path = dialog.get_selected_material_path()
            # Apply the material to the selected rows
            for row in selected_rows:
                self.scene.objects[row].set_material(material_path)
            # Update the visualization and the table
            self.update()

    def show_add_dialog(self):
        """
        Shows a dialog with a combo box to select an option ("3D object", "Light source", or "Camera").
        """
        # Create the dialog
        dialog = AddDialog(self)

        # Show the dialog and get the result
        result = dialog.exec_()

        # If the OK button was clicked
        if result == QDialog.Accepted:
            # Get the selected option
            selected_option = dialog.get_current_text()

            # Handle the selected option
            if selected_option == "3D object":
                self.add_object()
            elif selected_option == "Light source":
                self.add_ray_source()
            elif selected_option == "Camera":
                #self.add_camera()
                pass

    def add_object(self):
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

    def add_ray_source(self):
        """
        Adds a light source to the scene.

        This method opens a dialog to get the values for the light source, creates a new RaySource object
        with the provided values, and adds it to the scene. It then updates the visualization and the table.
        """
        dialog = AddRaySourceDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Get the values from the dialog
            origin, normal, aperture_angle, min_wavelength, max_wavelength, rectangle, mode, intensity = dialog.get_values()
            # Count the existing RaySource objects in the scene
            ray_source_count = sum(1 for obj in self.scene.objects if isinstance(obj, RaySource) and obj.mode == mode)
            # Generate a unique name for the new RaySource
            ray_source_name = f"{mode.capitalize()} Source {ray_source_count + 1}"
            # Create a new RaySource
            source = RaySource(origin, normal, aperture_angle, min_wavelength, max_wavelength, rectangle, mode, intensity, ray_source_name)
            # Add the RaySource to the Scene
            self.scene.add_object(source)
            # Update the visualization and the table
            self.update()

    def simulate(self):
        """
        Simulates the scene by tracing the rays from the light sources and calculating the intensity of each ray.
        """
        self.scene.simulate(10)
        self.update_visualization()

    def save(self):
        """
        Opens a file dialog to save the scene to a file.
        """
        directory = self.last_used_directory if self.last_used_directory is not None else str(Path.home())
        file_name, _ = QFileDialog.getSaveFileName(self, "Save scene", directory, "Scene Files (*.scene)")
        if file_name:
            self.last_used_directory = str(Path(file_name).parent)
            if not file_name.endswith(".scene"):
                file_name += ".scene"
            self.scene.save_to_file(file_name)

    def load(self):
        """
        Opens a file dialog to load a scene from a file.
        """
        directory = self.last_used_directory if self.last_used_directory is not None else str(Path.home())
        file_name, _ = QFileDialog.getOpenFileName(self, "Load scene", directory, "Scene Files (*.scene)")
        if file_name:
            self.last_used_directory = str(Path(file_name).parent)
            self.scene.load_from_file(file_name)
            self.update_visualization()

class AddRaySourceDialog(QDialog):
    """
    A dialog window for adding a ray source.

    This dialog allows the user to input various parameters for a ray source, such as the mode (point or rectangle),
    origin, normal, aperture angle, wavelength range, intensity, and rectangle vertices.

    The user can retrieve the values entered in the dialog using the `get_values` method.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Ray Source")

        # Input fields
        self.mode_input = QComboBox(self)
        self.mode_input.addItems(['point', 'rectangle'])
        self.origin_x_input, self.origin_y_input, self.origin_z_input = [self._create_spin_box() for _ in range(3)]
        self.normal_x_input, self.normal_y_input, self.normal_z_input = [self._create_spin_box() for _ in range(3)]
        self.normal_z_input.setValue(1)
        self.vertex_inputs = [[self._create_spin_box() for _ in range(3)] for _ in range(4)]  # 4 vertices, each with x, y, z
        self.vertex_inputs[1][0].setValue(10)
        self.vertex_inputs[2][0].setValue(10)
        self.vertex_inputs[2][1].setValue(10)
        self.vertex_inputs[3][1].setValue(10)
        self.aperture_angle_input = QDoubleSpinBox(self)
        self.aperture_angle_input.setRange(0, 360)
        self.aperture_angle_input.setMinimumWidth(70)
        self.min_wavelength_input = QDoubleSpinBox(self)
        self.min_wavelength_input.setRange(380, 740)
        self.min_wavelength_input.setValue(380)
        self.min_wavelength_input.setMinimumWidth(70)
        self.max_wavelength_input = QDoubleSpinBox(self)
        self.max_wavelength_input.setRange(380, 740)
        self.max_wavelength_input.setValue(740)
        self.max_wavelength_input.setMinimumWidth(70)
        self.intensity_input = QDoubleSpinBox(self)
        self.intensity_input.setRange(0, 1)
        self.intensity_input.setSingleStep(0.01)
        self.intensity_input.setValue(1)
        self.intensity_input.setMinimumWidth(70)

        # OK and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Layouts
        main_layout = QVBoxLayout(self)
        form_layout = QHBoxLayout()
        left_layout = QFormLayout()
        right_layout = QFormLayout()

        # Layout
        left_layout.addRow("Mode :", self.mode_input)
        left_layout.addRow("Origin X [mm] :", self.origin_x_input)
        left_layout.addRow("Origin Y [mm] :", self.origin_y_input)
        left_layout.addRow("Origin Z [mm] :", self.origin_z_input)
        left_layout.addRow("Normal X [mm] :", self.normal_x_input)
        left_layout.addRow("Normal Y [mm] :", self.normal_y_input)
        left_layout.addRow("Normal Z [mm] :", self.normal_z_input)
        left_layout.addRow("Aperture Angle [degrees] :", self.aperture_angle_input)
        left_layout.addRow("Min Wavelength [nm] :", self.min_wavelength_input)
        left_layout.addRow("Max Wavelength [nm] :", self.max_wavelength_input)
        left_layout.addRow("Intensity :", self.intensity_input)

        # Populate right layout with the rectangle vertex inputs
        for i, vertex in enumerate(self.vertex_inputs):
            for j, axis in enumerate(['X', 'Y', 'Z']):
                right_layout.addRow(f"Rectangle vertex {i+1} {axis} [mm]:", vertex[j])

        # Combine left and right layouts
        form_layout.addLayout(left_layout)
        form_layout.addLayout(right_layout)
        main_layout.addLayout(form_layout)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Set main layout
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # Signals
        self.mode_input.currentTextChanged.connect(self._update_vertex_input_state)
        self._update_vertex_input_state(self.mode_input.currentText())

    def _create_spin_box(self, min_val=-float('inf'), max_val=float('inf')):
        """
        Creates a QDoubleSpinBox widget with the specified minimum and maximum values.

        Args:
            min_val (float, optional): The minimum value for the spin box. Defaults to -inf.
            max_val (float, optional): The maximum value for the spin box. Defaults to inf.

        Returns:
            QDoubleSpinBox: The created spin box widget.
        """
        spin_box = QDoubleSpinBox(self)
        spin_box.setDecimals(2)
        spin_box.setRange(min_val, max_val)
        spin_box.setMinimumWidth(70)
        return spin_box
    
    def _update_vertex_input_state(self, mode):
        """
        Update the state of the vertex input spin boxes based on the given mode.

        Parameters:
        - mode (str): The mode to determine the state of the spin boxes. If mode is 'rectangle', the spin boxes will be enabled. Otherwise, they will be disabled.
        """
        is_rectangle = mode == 'rectangle'
        for vertex in self.vertex_inputs:
            for spin_box in vertex:
                spin_box.setEnabled(is_rectangle)
        self.origin_x_input.setEnabled(not is_rectangle)
        self.origin_y_input.setEnabled(not is_rectangle)
        self.origin_z_input.setEnabled(not is_rectangle)

    def get_values(self):
            """
            Get the values from the input fields and return them as a tuple.

            Returns:
                tuple: A tuple containing the following values:
                    - origin (Point): The origin point.
                    - normal (Vector): The normal vector.
                    - aperture_angle (float): The aperture angle.
                    - min_wavelength (float): The minimum wavelength.
                    - max_wavelength (float): The maximum wavelength.
                    - rectangle_vertices (list): A list of Point representing the vertices of a rectangle.
                    - mode (str): The mode.
                    - intensity (float): The intensity.
            """
            mode = self.mode_input.currentText()
            origin = Point(self.origin_x_input.value(), self.origin_y_input.value(), self.origin_z_input.value())
            normal = Vector(self.normal_x_input.value(), self.normal_y_input.value(), self.normal_z_input.value())
            aperture_angle = self.aperture_angle_input.value()
            min_wavelength = self.min_wavelength_input.value()
            max_wavelength = self.max_wavelength_input.value()
            rectangle = RectangularPlanarPolygon([Point([spin_box.value() for spin_box in vertex]) for vertex in self.vertex_inputs])
            intensity = self.intensity_input.value()

            return origin, normal, aperture_angle, min_wavelength, max_wavelength, rectangle, mode, intensity


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle("Select option")

        # Create the combo box
        self.combo_box = QComboBox()
        self.combo_box.addItem("3D object")
        self.combo_box.addItem("Light source")
        #self.combo_box.addItem("Camera")

        # Create the form layout
        form_layout = QFormLayout()
        form_layout.addRow("Option :", self.combo_box)

        # Create the OK and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def get_current_text(self):
        """
        Returns the current text of the combo box.
        """
        return self.combo_box.currentText()

class ChangeMaterialDialog(QDialog):
    def __init__(self, parent = None, current_material = None):
        super().__init__(parent)

        # Set the window title
        self.setWindowTitle("Select material")

        # Create the combo box
        self.combo_box = QComboBox()
        self.combo_box.addItem("vacuum")

        # Create the form layout
        form_layout = QFormLayout()
        form_layout.addRow("Material :", self.combo_box)

        # Get the list of available materials
        self.materials = self.get_available_materials()

        # Add the materials to the combo box
        for material in self.materials:
            self.combo_box.addItem(material[0])

        # Set the current material
        if current_material is not None:
            self.combo_box.setCurrentText(current_material)

        # Create the OK and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)

        # Create the button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        # Create the main layout
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def get_available_materials(self):
        """
        Returns a list of available materials in the 'resources/materials' folder.

        Returns:
            list: A list of file vectors, where each file vector contains the stem and path of a material file.
        """
        material_folder = Path("resources/materials")
        file_vectors = []
        for file_path in material_folder.iterdir():
            if file_path.is_file() and file_path.suffix == ".csv":
                file_vector = [file_path.stem, str(file_path)]
                file_vectors.append(file_vector)
        return file_vectors

    def get_selected_material_path(self):
        """
        Returns the path of the selected material.
        
        Returns:
            str: The path of the selected material.
        """
        if self.combo_box.currentIndex() == 0:
            return None
        return self.materials[self.combo_box.currentIndex()-1][1]

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