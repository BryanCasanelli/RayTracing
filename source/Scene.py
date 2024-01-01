from TriangularPlanarPolygon import TriangularPlanarPolygon
from Polyhedron import Polyhedron
from RectangularPlanarPolygon import RectangularPlanarPolygon
from Point import Point
from RaySource import RaySource
import numpy as np
from vispy import scene
from vispy.visuals.filters import ShadingFilter
from Vector import Vector
from Ray import Ray
from Material import Material

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
        self.rays = []
        self._camera_parameters = {'center': (0, 0, 0),'elevation': 30,'azimuth': 120} # Default camera parameters
        

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

    def vispy_display(self, canvas, show_polyhedrons=True):
        """
        Shows the faces of each Polyhedron as a mesh surface using VisPy.

        Args:
            canvas (VisPy canvas): The VisPy canvas to display the scene.
            show_polyhedrons (bool, optional): Flag to indicate whether to show Polyhedrons or not. 
                                                Defaults to True.

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

        # Restore the camera parameters
        view.camera.set_state(self._camera_parameters)

        # Connect the callback to the transform_updated event
        view.camera.events.transform_change.connect(self._save_camera_parameters)

        # Add each Polyhedron to the scene
        for obj in self.objects:

            if not show_polyhedrons and isinstance(obj, Polyhedron):
                continue

            # Get the vertices and face indices of the object
            vertices = np.array([vertex.get_coordinates() for vertex in obj.vertices])
            faces = np.array(obj.face_indices)

            if len(faces) > 0:  # Not all polyhedrons/associated Polyhedron have faces, e.g. Point RaySource
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
                light_dir = (-1, -1, 0, 0)
                shading_filter.light_dir = light_dir[:3]
                view.camera.transform.imap(light_dir)

            # Add a marker at the position of the Polyhedron / associated Polyhedron
            position_marker = scene.visuals.Markers()
            position_marker.set_data(np.array([obj.reference.get_coordinates()]), face_color='yellow', size=10)
            view.add(position_marker)

            # Check if the object is an instance of RaySource and display its normal
            if isinstance(obj, RaySource):
                # Calculate the endpoint of the normal vector
                normal_end = np.array(obj.reference.get_coordinates()) + np.array(obj.normal.get_coordinates())
                
                # Create a line visual for the normal vector
                normal_line = scene.visuals.Line(
                    pos=np.array([obj.reference.get_coordinates(), normal_end]), 
                    color='cyan', 
                    width=2
                )
                view.add(normal_line)

        # Add each ray to the scene
        for ray in self.rays:
            if ray.final_point != None:
                # Get the start and end points of the ray
                start = ray.origin.get_coordinates()
                end = ray.final_point.get_coordinates()

                # Ray color
                color = ray.wavelength_to_rgba()

                # Create a line visual for the ray
                ray_line = scene.visuals.Line(pos=np.array([start, end]), color=color, width=2)
                view.add(ray_line)

        # Add coordinate axes to the scene
        length = 1e20
        axis_x = scene.visuals.Line(pos=np.array([[0, 0, 0], [length, 0, 0]]), color='red')
        view.add(axis_x)
        axis_y = scene.visuals.Line(pos=np.array([[0, 0, 0], [0, length, 0]]), color='green')
        view.add(axis_y)
        axis_z = scene.visuals.Line(pos=np.array([[0, 0, 0], [0, 0, length]]), color='blue')
        view.add(axis_z)

    def _save_camera_parameters(self, event):
        """
        Saves the parameters of the camera.

        Args:
            event (vispy Event): The event that triggered the callback.
        """
        self._camera_parameters = event.source.get_state()

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
                object_descriptions.append(f"RaySource at {obj.reference} with aperture angle {obj.aperture_angle}")

        scene_description = '; '.join(object_descriptions)
        return f"Scene(Objects: {scene_description})"
    
    def simulate(self, num_rays: int, min_intensity: float = 0.1, final_length: float = 20, max_reflections: int = 1):
        """
        Simulates the propagation of rays through the scene.

        Parameters:
        - num_rays (int): The number of rays to simulate.
        - min_intensity (float): The minimum intensity of a ray to continue simulating.
        - final_length (float): The length of the ray for the last segment of the simulation.
        """
        # Clear the list of rays
        self.rays = []
        # Interate over each object in the scene until find a RaySource
        for obj in self.objects:
            if isinstance(obj, RaySource):
                # Generate the specified number of rays
                for n in range(num_rays):
                    ray = obj.get_next_ray()
                    # Propagate the ray through the scene
                    self._propagate(ray, min_intensity, final_length, max_reflections)
                    
    def _propagate(self, ray, min_intensity, final_length, max_reflections):
        """
        Propagates a ray through the scene, checking for intersections with polyhedrons.

        Parameters:
        - num_rays (int): The number of rays to simulate.
        - min_intensity (float): The minimum intensity of a ray to continue simulating.
        - final_length (float): The length of the ray for the last segment of the simulation.
        """
        # Check if the ray's intensity is below the minimum
        if ray.intensity < min_intensity:
            return
        # Search for intersections with Polyhedrons
        intersections = []
        for polyhedron in self.objects:
            if isinstance(polyhedron, Polyhedron):
                intersection = polyhedron.get_nearest_intersection(ray)
                # If an intersection is found
                if intersection is not None:
                    intersections.append(intersection + [polyhedron])
        # If intersections were found
        if intersections:
            # Get the nearest intersection
            intersection = min(intersections, key=lambda i: i[0].distance(ray.origin))
            # Get the intersection data
            intersection_point = intersection[0]
            intersection_face = intersection[1]
            intersection_polyhedron = intersection[2]
            # Get all the vectors needed
            ray_normal = ray.normal
            face_normal = intersection_face.normal
            # If the angle between the inverse ray normal and the intersection face normal is greater than 90 degrees, flip the normal
            ray_normal_inverted = ray.normal.copy()
            ray_normal_inverted.invert()
            if ray_normal_inverted.angle_with(face_normal) > np.pi/2:
                face_normal.invert()
            # Set final point, automatically compute the loss of intensity
            ray.set_final_point(intersection_point)
            # Finish current ray
            self.rays.append(ray.copy())
            # Materials, reffractive index and angles
            m1 = ray.medium
            m2 = intersection_polyhedron.material
            if m1.name == m2.name:
                m2 = Material()  # This condicion can happen when the ray is going out the polyhedron, set the outside material as Vacuum
            n1 = m1.get_refractive_index(ray.wavelength).real
            n2 = m2.get_refractive_index(ray.wavelength).real
            n1_n2_ratio = (n1/n2)
            theta_1 = ray_normal_inverted.angle_with(face_normal)
            theta_2 = np.arcsin(n1_n2_ratio * np.sin(theta_1))
            # Reflectance
            r_parallel = np.abs((n1*np.cos(theta_1) - n2*np.cos(theta_2)) / (n1*np.cos(theta_1) + n2*np.cos(theta_2)))**2
            r_perpendicular = np.abs((n2*np.cos(theta_1) - n1*np.cos(theta_2)) / (n2*np.cos(theta_1) + n1*np.cos(theta_2)))**2
            reflectance = (r_parallel + r_perpendicular) / 2
            # Transmittance
            transmittance = 1 - reflectance
            # Calculate the reflected ray
            if max_reflections > 0:
                reflected_vector = Vector(ray_normal.get_coordinates() - 2 * face_normal.get_coordinates() * ray_normal.dot(face_normal))
                reflected_intensity = ray.intensity * reflectance
                reflected_ray = Ray(intersection_point, reflected_vector, ray.wavelength, reflected_intensity)
                reflected_ray.medium = m1
                max_reflections -= 1
                self._propagate(reflected_ray, min_intensity, final_length, max_reflections)
            # Calculate the transmitted ray
            transmitted_vector = Vector(n1_n2_ratio*ray.normal.get_coordinates() + (n1_n2_ratio*np.cos(theta_1) - np.cos(theta_2))*face_normal.get_coordinates())
            transmitted_intensity = ray.intensity * transmittance
            transmitted_ray = Ray(intersection_point, transmitted_vector, ray.wavelength, transmitted_intensity)
            transmitted_ray.medium = intersection_polyhedron.material
            self._propagate(transmitted_ray, min_intensity, final_length, max_reflections)
        # No intersection found, add the ray to the list
        else:
            ray.set_final_point(Point(ray.origin.get_coordinates() + ray.normal.get_coordinates() * final_length))
            self.rays.append(ray)
