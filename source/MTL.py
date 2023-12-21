class MTL():
    """
    This class is used for handling material data for 3D models.
    It reads from a .mtl file, which is associated with .obj files in 3D modeling,
    and stores material properties in a dictionary.

    Attributes:
        materials (dict): A dictionary where each key is a material name and the value is 
                          another dictionary containing the properties of that material.
    """

    def __init__(self, mtl_path: str) -> None:
        """
        Initializes the Material instance by reading and parsing a .mtl file.

        Args:
            mtl_path (str): The path to the .mtl file to be read.

        The function reads the .mtl file line by line, ignoring comments and empty lines.
        It recognizes material properties and stores them in the materials dictionary.
        """
        self.materials = {}
        current_material = None

        with open(mtl_path, 'r') as file:
            for line in file:
                if line.startswith('#'):  # Skip comments
                    continue
                values = line.split()
                if not values:
                    continue
                if values[0] == 'newmtl':
                    current_material = values[1]
                    self.materials[current_material] = {}
                elif current_material is not None:
                    if values[0] in ['Ns', 'Ka', 'Kd', 'Ks', 'Ni', 'd']:
                        # These are typically floats
                        self.materials[current_material][values[0]] = list(map(float, values[1:]))
                    elif values[0] in ['map_Kd', 'map_Bump']:
                        # These are file paths
                        self.materials[current_material][values[0]] = values[1]