from Point import Point
from Vector import Vector

class Ray:
    """
    Represents a ray in three-dimensional space.

    Attributes:
        origin (Point): The origin point of the ray.
        normal (Vector): The normal vector indicating the direction of the ray.
        wavelength (float): The wavelength of the ray.
        intensity (float): The intensity of the ray, ranging from 0.0 to 1.0.
    """

    def __init__(self, origin: Point, normal: Vector, wavelength: float, intensity = 1.0) -> None:
        """
        Initializes the Ray instance with the specified origin, normal vector, and wavelength.

        Args:
            origin (Point): The origin point of the ray.
            normal (Vector): The normal vector indicating the direction of the ray.
            wavelength (float): The wavelength of the ray.
            intensity (float): The intensity of the ray, ranging from 0.0 to 1.0.
        """
        self.origin = origin
        self.normal = normal
        self.wavelength = wavelength
        self.intensity = intensity

    def __str__(self) -> str:
        """
        Returns a string representation of the Ray.

        Returns:
            str: The string representation of the Ray.
        """
        return (f"Ray(Origin: ({self.origin.x}, {self.origin.y}, {self.origin.z}), "
                f"Direction: ({self.normal.x}, {self.normal.y}, {self.normal.z}), "
                f"Wavelength: {self.wavelength})")
    
    def wavelength_to_rgba(self):
        """
        Convert the wavelength in nanometers to an RGBA color using the CIE 1931 color space approximation.

        Returns:
            tuple: RGBA color represented as (R, G, B, Alpha), values in the range [0, 255] for RGB and [0,1] for Alpha.
        """
        gamma = 0.8
        intensity_max = 255
        factor = 0.0
        R, G, B = 0, 0, 0

        if (self.wavelength >= 380) and (self.wavelength < 440):
            R = -(self.wavelength - 440) / (440 - 380)
            G = 0.0
            B = 1.0
        elif (self.wavelength >= 440) and (self.wavelength < 490):
            R = 0.0
            G = (self.wavelength - 440) / (490 - 440)
            B = 1.0
        elif (self.wavelength >= 490) and (self.wavelength < 510):
            R = 0.0
            G = 1.0
            B = -(self.wavelength - 510) / (510 - 490)
        elif (self.wavelength >= 510) and (self.wavelength < 580):
            R = (self.wavelength - 510) / (580 - 510)
            G = 1.0
            B = 0.0
        elif (self.wavelength >= 580) and (self.wavelength < 645):
            R = 1.0
            G = -(self.wavelength - 645) / (645 - 580)
            B = 0.0
        elif (self.wavelength >= 645) and (self.wavelength <= 750):
            R = 1.0
            G = 0.0
            B = 0.0

        # Adjust intensity
        if (self.wavelength >= 380) and (self.wavelength < 420):
            factor = 0.3 + 0.7 * (self.wavelength - 380) / (420 - 380)
        elif (self.wavelength >= 420) and (self.wavelength < 645):
            factor = 1.0
        elif (self.wavelength >= 645) and (self.wavelength <= 750):
            factor = 0.3 + 0.7 * (750 - self.wavelength) / (750 - 645)

        R = int(intensity_max * (R * factor) ** gamma)
        G = int(intensity_max * (G * factor) ** gamma)
        B = int(intensity_max * (B * factor) ** gamma)

        return (R, G, B, self.intensity)
