import csv
import numpy as np
from scipy.interpolate import interp1d

class Material:
    def __init__(self, file_path=None):
        """
        Initializes the Material instance. If file_path is None, creates a vacuum material with refractive index 1.

        Args:
            file_path (str, optional): The path to the CSV file containing wavelength and refractive index data.
                                       If None, a vacuum material is created.
        """
        if file_path:
            self.wavelengths, self.refractive_indices = self._read_data(file_path)
            self.real_interpolator = interp1d(self.wavelengths, [n.real for n in self.refractive_indices], kind='linear', fill_value="extrapolate")
            self.imag_interpolator = interp1d(self.wavelengths, [n.imag for n in self.refractive_indices], kind='linear', fill_value="extrapolate")
        else:
            self.wavelengths = [0, float('inf')]  # Represents all wavelengths
            self.refractive_indices = [1, 1]  # Refractive index of vacuum is 1

            # Interpolators return 1 regardless of wavelength
            self.real_interpolator = lambda wavelength: 1
            self.imag_interpolator = lambda wavelength: 0

    def _read_data(self, file_path):
        """
        Reads data from the specified tab-separated CSV file and converts the wavelength from micrometers to nanometers.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            tuple: Two lists containing wavelengths (in nanometers) and complex refractive indices, respectively.
        """
        wavelengths = []
        refractive_indices = []

        with open(file_path, 'r') as file:
            reader = csv.reader(file, delimiter=' ')
            for row in reader:
                wavelength_micrometers, real_n, imag_n = row
                wavelength_nanometers = float(wavelength_micrometers) * 1000  # Convert from micrometers to nanometers
                complex_n = complex(float(real_n), float(imag_n))  # Create a complex number for the refractive index
                wavelengths.append(wavelength_nanometers)
                refractive_indices.append(complex_n)

        return wavelengths, refractive_indices

    def get_refractive_index(self, wavelength):
        """
        Gets the complex refractive index for a given wavelength in nanometers by interpolating the data.

        Args:
            wavelength (float): The wavelength in nanometers for which to find the refractive index.

        Returns:
            complex: The interpolated complex refractive index.
        """
        real_part = self.real_interpolator(wavelength)
        imag_part = self.imag_interpolator(wavelength)
        return complex(real_part, imag_part)
