from Point import Point
from TriangularPlanarPolygon import TriangularPlanarPolygon
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Material import Material
import warnings

class Polyhedron:
    """
    Represents a 3D object composed of TriangularPlanarPolygons and/or RectangularPlanarPolygons.

    Attributes:
        faces (list of TriangularPlanarPolygon or RectangularPlanarPolygon): The faces of the 3D object.
        material (Material): The material of the Polyhedron. If no material path is provided,
                        a vacuum material (refractive index of 1) is created by default.
        vertices (list of Point): The vertices of the Polyhedron.
        face_indices (list of list of int): The indices of the vertices for each face.
    """

    def __init__(self, source=None, material_path=None):
        """
        Initializes a new Polyhedron object. Can optionally be initialized from an OBJ file or a list of 
        TriangularPlanarPolygons and/or RectangularPlanarPolygons, and a material file path.

        Args:
            source (str or list, optional): The path to the OBJ file to parse, or a list of 
                TriangularPlanarPolygons and RectangularPlanarPolygons.
                If None, initializes an empty Polyhedron.
            material_path (str, optional): The path to the material file. If None, a vacuum material
                                           (with a refractive index of 1) is created by default.
        """
        self.faces = []
        self.material = Material(material_path)
        self.vertices = []
        self.face_indices = []

        if isinstance(source, str):
            self._parse_from_obj_file(source)
        elif isinstance(source, list):
            for polygon in source:
                self.add_face(polygon)

    def _parse_from_obj_file(self, filename):
        """
        Parses an OBJ file to generate the polyhedron's geometry, including rectangular faces.

        Args:
            filename (str): The path to the OBJ file.
        """
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    parts = line.split()
                    point = Point(float(parts[1]), float(parts[2]), float(parts[3]))
                    self.vertices.append(point)
                elif line.startswith('f '):
                    parts = line.split()
                    indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]  # OBJ indices start at 1
                    if len(indices) == 3:
                        # It's a triangle
                        triangle = TriangularPlanarPolygon([self.vertices[i] for i in indices])
                        self.face_indices.append(indices)
                        self.add_face(triangle)
                    elif len(indices) == 4:
                        # It's a rectangle, create a RectangularPlanarPolygon
                        rectangle = RectangularPlanarPolygon([self.vertices[i] for i in indices])
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