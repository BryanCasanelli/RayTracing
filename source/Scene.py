import plotly.graph_objects as go
from TriangularPlanarPolygon import TriangularPlanarPolygon
from Polyhedron import Polyhedron
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Point import Point
from RaySource import RaySource

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

    def show(self, num_rays_per_source=1000, ray_preview_radius=30):
        """
        Visualizes all the objects in the scene using Plotly, including rays from RaySources.

        Args:
            num_rays_per_source (int): Number of rays to generate per RaySource.
            ray_preview_radius (float): Radius of ray previsualization.
        """
        # Initialize Plotly figure
        fig = go.Figure()

        # Visualize Polyhedrons and Points
        for object in self.objects:
            if isinstance(object, Polyhedron):
                x, y, z = [], [], []
                i, j, k = [], [], []
                for face in object.faces:
                    start_index = len(x)
                    for vertex in face.vertices:
                        x.append(vertex.x)
                        y.append(vertex.y)
                        z.append(vertex.z)

                    for n in range(1, len(face.vertices) - 1):
                        i.append(start_index)
                        j.append(start_index + n)
                        k.append(start_index + n + 1)

                # Add the polyhedron as a mesh to the plot
                fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, opacity=0.5))

            elif isinstance(object, Point):
                fig.add_trace(go.Scatter3d(x=[object.x], y=[object.y], z=[object.z], mode='markers'))

        # Visualize rays from RaySource objects
        for object in self.objects:
            if isinstance(object, RaySource):
                for _ in range(num_rays_per_source):
                    ray = object.get_next_ray()
                    end_point = Point(ray.origin.x + ray_preview_radius * ray.normal.x, 
                                    ray.origin.y + ray_preview_radius * ray.normal.y, 
                                    ray.origin.z + ray_preview_radius * ray.normal.z)

                    fig.add_trace(go.Scatter3d(x=[ray.origin.x, end_point.x],
                                            y=[ray.origin.y, end_point.y],
                                            z=[ray.origin.z, end_point.z],
                                            mode='lines',
                                            line=dict(color=f'rgba{ray.wavelength_to_rgba()}')))

        # Configure and display the figure
        fig.update_layout(scene=dict(xaxis_title='X',
                                    yaxis_title='Y',
                                    zaxis_title='Z',
                                    xaxis=dict(visible=True),
                                    yaxis=dict(visible=True),
                                    zaxis=dict(visible=True)))
        fig.show()

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