from Point import Point
from TriangularPlanarPolygon import TriangularPlanarPolygon
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Material import Material
import warnings
from pathlib import Path
from Ray import Ray
import numpy as np

class Polyhedron:
    """
    Represents a 3D object composed of TriangularPlanarPolygons and/or RectangularPlanarPolygons.

    Attributes:
        faces (list of TriangularPlanarPolygon): The faces of the 3D object.
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
        tmp_vertex = []
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
                    tmp_vertex.append(Point(float(parts[1]), float(parts[2]), float(parts[3])))
                elif line.startswith('f '):
                    parts = line.split()
                    indices = [int(part.split('/')[0]) - 1 for part in parts[1:]]  # OBJ indices start at 1
                    if len(indices) == 3:
                        # It's a triangle
                        triangle = TriangularPlanarPolygon([tmp_vertex[i].copy() for i in indices])    
                        self.add_face(triangle, False)
                    elif len(indices) == 4:
                        # It's a rectangle, create a RectangularPlanarPolygon
                        rectangle = RectangularPlanarPolygon([tmp_vertex[i].copy() for i in indices])
                        self.add_face(rectangle, False)
        self.clean_vertices()

    def _are_points_distinct(self, points):
        """
        Checks if all points in the list are distinct.

        Args:
            points (list of Point): A list of Point objects.

        Returns:
            bool: True if all points are distinct, False otherwise.
        """
        return len(points) == len(set((p.x, p.y, p.z) for p in points))

    def add_face(self, polygon, clean_vertices = True):
        """
        Adds a face to the 3D object.

        Args:
            polygon (TriangularPlanarPolygon or RectangularPlanarPolygon): The face to add to the 3D object.
        """
        if not isinstance(polygon, (TriangularPlanarPolygon, RectangularPlanarPolygon)):
            raise TypeError("Unsupported polygon type.")
        
        if isinstance(polygon, RectangularPlanarPolygon):
            self.add_face(polygon.triangle1)
            self.add_face(polygon.triangle2)
        else:
            # Add vertices from the polygon to the polyhedron's vertices list
            face_vertex_indices = []
            for vertex in polygon.vertices:
                self.vertices.append(vertex.copy())
                face_vertex_indices.append(len(self.vertices) - 1)  # Index of the newly added vertex

            # Add the new face's vertex indices to face_indices
            self.face_indices.append(face_vertex_indices)

            # Add the face to the faces list
            self.faces.append(polygon)

        # Clean the vertices if requested
        if clean_vertices:
            self.clean_vertices()

    def clean_vertices(self):
        """
        Removes duplicate vertices and updates the face indices.
        """
        unique_vertices = {}
        new_vertices = []
        new_face_indices = []

        # Identify unique vertices and assign them new indices
        for vertex in self.vertices:
            vertex_tuple = (vertex.x, vertex.y, vertex.z)
            if vertex_tuple not in unique_vertices:
                unique_vertices[vertex_tuple] = len(new_vertices)
                new_vertices.append(vertex)

        # Update face indices based on new vertex indices
        for face in self.face_indices:
            new_face = [unique_vertices[(self.vertices[i].x, self.vertices[i].y, self.vertices[i].z)] for i in face]
            new_face_indices.append(new_face)

        # Update the vertices and face_indices of the Polyhedron
        self.vertices = new_vertices
        self.face_indices = new_face_indices
        
    def translate(self, dx, dy, dz):
        """
        Translates the Polyhedron by the specified amounts in the x, y, and z directions.

        Args:
            dx (float): The amount to translate in the x direction.
            dy (float): The amount to translate in the y direction.
            dz (float): The amount to translate in the z direction.
        """
        if self.vertices:
            # Translate all vertices
            for i, vertex in enumerate(self.vertices):
                vertex.x += dx
                vertex.y += dy
                vertex.z += dz
                if self.progress_callback_function != None:
                    self.progress_callback_function((i+1) / len(self.vertices) * 100)

            # Translate all vertices of each face
            for i, face in enumerate(self.faces):
                for vertex in face.vertices:
                    vertex.x += dx
                    vertex.y += dy
                    vertex.z += dz
                if self.progress_callback_function != None:
                    self.progress_callback_function((i+1) / len(self.faces) * 100)

        # Translate the reference point
        self.reference.x += dx
        self.reference.y += dy
        self.reference.z += dz

    def change_reference_point(self, ref_type, axis, x=None, y=None, z=None):
        """
        Changes the reference point to the lowest or highest point on a specific axis,
        or to the manually specified coordinates.

        Args:
            ref_type (str): The reference type, either "Centroid", "Lowest", "Highest", or "Manual".
            axis (str): The axis, either "x", "y", or "z".
            x (float): The x-coordinate of the new reference point (optional).
            y (float): The y-coordinate of the new reference point (optional).
            z (float): The z-coordinate of the new reference point (optional).
        """
        if ref_type == "Centroid":
            self.reference = self.centroid()
        elif ref_type == "Lowest":
            if self.vertices:
                self.reference = min(self.vertices, key=lambda vertex: getattr(vertex, axis))
        elif ref_type == "Highest":
            if self.vertices:
                self.reference = max(self.vertices, key=lambda vertex: getattr(vertex, axis))
        elif ref_type == "Manual":
            if x is None or y is None or z is None:
                raise ValueError("Invalid coordinates for manual reference point.")
            self.reference = Point(x, y, z)
        else:
            raise ValueError(f"Invalid reference type: {ref_type}")
    
    def set_material(self, material_path):
        """
        Sets the material of the Polyhedron to a new Material object created from the given path.

        Args:
            material_path (str): The path to the material file.
        """
        self.material = Material(material_path)

    def area(self) -> float:
        """
        Calculates the total surface area of the Polyhedron.

        Returns:
            float: The total surface area of the Polyhedron.
        """
        area = 0
        for face in self.faces:
            area += face.area()
        return area

    def centroid(self) -> Point:
        """
        Calculates the centroid (middle point) of the Polyhedron.

        Returns:
            Point: The centroid of the Polyhedron.
        """
        if self.vertices: # Is not only a point
            centroid = np.array([0.0, 0.0, 0.0])
            for face in self.faces:
                centroid += face.centroid().get_coordinates()*face.area()
            centroid /= self.area()
            return Point(centroid)
        else:  # Is only a point
            return self.reference.copy()

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
    
    def get_intersections(self, ray: Ray):
        """
        Finds all intersections of the ray with the Polyhedron.

        Args:
            ray (Ray): The Ray object to find the intersections with.

        Returns:
            list of Point: The list of intersection points, or an empty list if no intersections were found.
        """
        intersections = []

        # Check if the ray intersects with any face of the polyhedron
        for face in self.faces:
            intersection = face.get_intersection(ray)
            if intersection is not None:
                intersections.append([intersection, face])

        return intersections

    def get_nearest_intersection(self, ray: Ray):
        """
        Finds the nearest intersection of the ray with the Polyhedron.

        Args:
            ray (Ray): The Ray object to find the intersection with.

        Returns:
            Point: The nearest intersection point, or None if no intersections were found.
        """
        intersections = self.get_intersections(ray)
        if intersections:
            return min(intersections, key=lambda p: p[0].distance(ray.origin))
        else:
            return None