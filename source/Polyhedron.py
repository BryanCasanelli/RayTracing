from Point import Point
from TriangularPlanarPolygon import TriangularPlanarPolygon
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Material import Material
import warnings
from pathlib import Path

class Polyhedron:
    """
    Represents a 3D object composed of TriangularPlanarPolygons and/or RectangularPlanarPolygons.

    Attributes:
        faces (list of TriangularPlanarPolygon or RectangularPlanarPolygon): The faces of the 3D object.
        material (Material): The material of the Polyhedron. If no material path is provided,
                        a vacuum material (refractive index of 1) is created by default.
        vertices (list of Point): The vertices of the Polyhedron.
        face_indices (list of list of int): The indices of the vertices for each face.
        reference = self.vertices[0] if self.vertices else None
        name (str): The name of the Polyhedron.
    """

    def __init__(self, source=None, material_path=None, progress_callback_function=None):
        """
        Initializes a new Polyhedron object. Can optionally be initialized from an OBJ file or a list of 
        TriangularPlanarPolygons and/or RectangularPlanarPolygons, and a material file path.

        Args:
            source (str or list, optional): The path to the OBJ file to parse, or a list of 
                TriangularPlanarPolygons and RectangularPlanarPolygons.
                If None, initializes an empty Polyhedron.
            material_path (str, optional): The path to the material file. If None, a vacuum material
                                           (with a refractive index of 1) is created by default.
            progress_callback_function (function, optional): A callback function to track the progress of some methods.
                                                    Default is None.
        """
        self.faces = []
        self.material = Material(material_path)
        self.vertices = []
        self.face_indices = []
        self.name = None
        self.progress_callback_function = progress_callback_function

        if isinstance(source, str):
            self._parse_from_obj_file(source)
            self.name = Path(source).stem  # Set the name attribute using pathlib.Path
        elif isinstance(source, list):
            for polygon in source:
                self.add_face(polygon)

        # Set the position equals to the first vertex, if there is one
        self.reference = self.vertices[0].copy() if self.vertices else None

    def _parse_from_obj_file(self, filename):
        """
        Parses an OBJ file to generate the polyhedron's geometry, including rectangular faces.

        Args:
            filename (str): The path to the OBJ file.
        """
        current_line = 0
        with open(filename, 'r') as file:
            if self.progress_callback_function is not None:
                total_lines = sum(1 for _ in file)
                file.seek(0)
            for line in file:
                current_line += 1
                if self.progress_callback_function is not None:
                    progress = current_line / total_lines * 100
                    self.progress_callback_function(progress)
                if line.startswith('v '):
                    parts = line.split()
                    point = Point(float(parts[1]), float(parts[2]), float(parts[3]))
                    self.vertices.append(point)
                elif line.startswith('f '):
                    parts = line.split()
                    indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]  # OBJ indices start at 1
                    if len(indices) == 3:
                        # It's a triangle
                        triangle = TriangularPlanarPolygon([self.vertices[i].copy() for i in indices])
                        self.face_indices.append(indices)
                        self.add_face(triangle)
                    elif len(indices) == 4:
                        # It's a rectangle, create a RectangularPlanarPolygon
                        rectangle = RectangularPlanarPolygon([self.vertices[i].copy() for i in indices])
                        # Decompose the rectangle into two triangles
                        self.add_face(rectangle.triangle1)
                        self.face_indices.append([indices[0], indices[1], indices[2]])
                        self.add_face(rectangle.triangle2)
                        self.face_indices.append([indices[2], indices[3], indices[0]])

        

    def _are_points_distinct(self, points):
        """
        Checks if all points in the list are distinct.

        Args:
            points (list of Point): A list of Point objects.

        Returns:
            bool: True if all points are distinct, False otherwise.
        """
        return len(points) == len(set((p.x, p.y, p.z) for p in points))

    def add_face(self, polygon):
        """
        Adds a face to the 3D object only if all points are distinct. 
        Emits a warning otherwise.

        Args:
            polygon (TriangularPlanarPolygon or RectangularPlanarPolygon): The face to add to the 3D object.
        """
        if isinstance(polygon, TriangularPlanarPolygon):
            if self._are_points_distinct(polygon.vertices):
                self.faces.append(polygon)
            else:
                warnings.warn("Attempted to add a triangular face with non-distinct points.", RuntimeWarning)
        elif isinstance(polygon, RectangularPlanarPolygon):
            if self._are_points_distinct(polygon.points):
                # Decompose the rectangle into two triangles and add them
                self.faces.append(polygon.triangle1)
                self.faces.append(polygon.triangle2)
            else:
                warnings.warn("Attempted to add a rectangular face with non-distinct points.", RuntimeWarning)
        else:
            raise TypeError("Unsupported polygon type.")
        
    def translate(self, dx, dy, dz):
        """
        Translates the Polyhedron by the specified amounts in the x, y, and z directions.

        Args:
            dx (float): The amount to translate in the x direction.
            dy (float): The amount to translate in the y direction.
            dz (float): The amount to translate in the z direction.
        """
        for i, vertex in enumerate(self.vertices):
            vertex.x += dx
            vertex.y += dy
            vertex.z += dz
            if self.progress_callback_function != None:
                self.progress_callback_function((i+1) / len(self.vertices) * 100)

        for i, face in enumerate(self.faces):
            for vertex in face.vertices:
                vertex.x += dx
                vertex.y += dy
                vertex.z += dz
            if self.progress_callback_function != None:
                self.progress_callback_function((i+1) / len(self.faces) * 100)

    def change_reference_point(self, ref_type, axis, x=None, y=None, z=None):
        """
        Changes the reference point to the lowest or highest point on a specific axis,
        or to the manually specified coordinates.

        Args:
            ref_type (str): The reference type, either "Lowest", "Highest", or "Manual".
            axis (str): The axis, either "x", "y", or "z".
            x (float): The x-coordinate of the new reference point (optional).
            y (float): The y-coordinate of the new reference point (optional).
            z (float): The z-coordinate of the new reference point (optional).
        """
        if not self.vertices:
            return

        if ref_type == "Lowest":
            self.reference = min(self.vertices, key=lambda vertex: getattr(vertex, axis))
        elif ref_type == "Highest":
            self.reference = max(self.vertices, key=lambda vertex: getattr(vertex, axis))
        elif ref_type == "Manual":
            if x is None or y is None or z is None:
                raise ValueError("Invalid coordinates for manual reference point.")
            self.reference = Point(x, y, z)
        else:
            raise ValueError(f"Invalid reference type: {ref_type}")
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Polyhedron, showing all points of each face.

        Returns:
            str: The string representation of the Polyhedron.
        """
        face_descriptions = []
        for face in self.faces:
            vertices = ', '.join(f"({v.x}, {v.y}, {v.z})" for v in face.vertices)
            face_type = "Triangle" if isinstance(face, TriangularPlanarPolygon) else "Rectangle"
            face_descriptions.append(f"{face_type}({vertices})")

        faces_str = '; '.join(face_descriptions)
        return f"Polyhedron(Faces: {faces_str})"