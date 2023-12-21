from TriangularPlanarPolygon import TriangularPlanarPolygon
from Polyhedron import Polyhedron
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Point import Point
from RaySource import RaySource
import numpy as np
from vispy import scene
from vispy.visuals.filters import ShadingFilter

class Scene:
    """
    Represents a 3D scene composed of various objects like Points, Polyhedrons, 
    TriangularPlanarPolygons, and RectangularPlanarPolygons.

    Attributes:
        objects (list): The objects in the scene, including Points, Polyhedrons, 
                        TriangularPlanarPolygons, and RectangularPlanarPolygons.
    """

    def __init__(self):
        """
        Initializes a new Scene object.
        """
        self.objects = []

    def add_object(self, object):
        """
        Adds an object to the scene. Converts TriangularPlanarPolygon and RectangularPlanarPolygon
        into Polyhedron objects before adding, and directly adds RaySource objects.

        Args:
            object: The object to add to the scene.
        """
        if isinstance(object, TriangularPlanarPolygon):
            polyhedron = Polyhedron()
            polyhedron.add_face(object)
            self.objects.append(polyhedron)
        elif isinstance(object, RectangularPlanarPolygon):
            polyhedron = Polyhedron()
            polyhedron.add_face(object.triangle1)
            polyhedron.add_face(object.triangle2)
            self.objects.append(polyhedron)
        else:
            self.objects.append(object)

    def remove_object(self, index):
        """
        Removes an object from the scene based on its index.

        Args:
            index (int): The index of the object to remove.
        """
        if index >= 0 and index < len(self.objects):
            del self.objects[index]

    def vispy_display(self, canvas):
        """
        Shows the faces of each Polyhedron as a mesh surface using VisPy.

        Args:
            canvas (VisPy canvas): The VisPy canvas to display the scene.

        """

        # Remove all children from the central widget
        for child in list(canvas.central_widget.children):
            canvas.central_widget.remove_widget(child)

        # Add a view to the central widget
        view = canvas.central_widget.add_view()

        # Set the camera parameters
        view.camera = 'turntable'
        view.camera.fov = 0
        view.camera.scale_factor = 300

        # Add each Polyhedron to the scene
        for obj in self.objects:
            if isinstance(obj, Polyhedron):

                # Get the vertices and face indices of the Polyhedron
                vertices = np.array([vertex.get_coordinates() for vertex in obj.vertices])
                faces = np.array(obj.face_indices)

                # Create a colored `MeshVisual` using the vertices and faces
                face_colors = np.tile((0.5, 0.0, 0.5, 1.0), (len(faces), 1))
                mesh = scene.visuals.Mesh(
                    vertices,
                    faces,
                    face_colors=face_colors.copy()
                )
                view.add(mesh)

                # Add shading to the mesh
                shading_filter = ShadingFilter()
                mesh.attach(shading_filter)

                # Attach headlight to the scene
                light_dir = (0, 1, 0, 0)
                shading_filter.light_dir = light_dir[:3]
                view.camera.transform.imap(light_dir)

                # Add a marker at the position of the Polyhedron
                position_marker = scene.visuals.Markers()
                position_marker.set_data(np.array([obj.position.get_coordinates()]), face_color='yellow', size=10)
                view.add(position_marker)

        # Add coordinate axes to the scene
        axis_x = scene.visuals.Line(pos=np.array([[0, 0, 0], [1e4, 0, 0]]), color='red')
        view.add(axis_x)
        axis_y = scene.visuals.Line(pos=np.array([[0, 0, 0], [0, 1e4, 0]]), color='green')
        view.add(axis_y)
        axis_z = scene.visuals.Line(pos=np.array([[0, 0, 0], [0, 0, 1e4]]), color='blue')
        view.add(axis_z)

    def __str__(self) -> str:
        """
        Returns a string representation of the Scene.

        Returns:
            str: The string representation of the Scene.
        """
        object_descriptions = []

        for obj in self.objects:
            if isinstance(obj, Point):
                object_descriptions.append(f"Point({obj.x}, {obj.y}, {obj.z})")
            elif isinstance(obj, Polyhedron):
                object_descriptions.append(f"Polyhedron with {len(obj.faces)} faces")
            elif isinstance(obj, TriangularPlanarPolygon):
                object_descriptions.append("TriangularPlanarPolygon")
            elif isinstance(obj, RectangularPlanarPolygon):
                object_descriptions.append("RectangularPlanarPolygon")
            elif isinstance(obj, RaySource):
                object_descriptions.append(f"RaySource at {obj.origin} with aperture angle {obj.aperture_angle}")

        scene_description = '; '.join(object_descriptions)
        return f"Scene(Objects: {scene_description})"