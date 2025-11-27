import numpy as np
from matplotlib import pyplot as plt


class _PointsBaseClass:
    """Base class for points, used for nodes, geometrical points, integration points, etc."""

    def __init__(self, type="default", coordinates=[[]], ids=[]) -> None:
        """
        Initialize a base points class.

        Parameters
        ----------
        type (str) -- Type of points (default: "default")
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """
        self.coordinates = np.array(coordinates, dtype=np.float64)
        self.type = type

        ids = np.array(ids)

        # Check if custom identifiers are given
        if ids.size == 0:
            self.ids = np.arange(1, self.coordinates.shape[0] + 1)
        else:
            self.ids = ids

    @property
    def x(self) -> np.ndarray:
        """X Coordinates"""
        return self.coordinates[:, 0]

    @property
    def y(self) -> np.ndarray:
        """Y Coordinates"""
        return self.coordinates[:, 1]

    def setCoordinates(self, coordinates):
        """
        Set coordinates.

        Parameters
        ----------
        coordinates (list of lists) -- List of x, y coordinates
        """
        self.coordinates = np.array(coordinates, dtype=np.float64)

        if self.ids.shape == 0:
            self.ids = np.arange(1, self.coordinates.shape[0] + 1)

    def setIds(self, ids):
        """
        Set identifiers.

        Parameters
        ----------
        ids (list) -- List of identifiers
        """
        self.ids = np.array(ids)

    def findIndexByNodeIds(self, ids):
        """
        Get index for specific nodes.

        Parameters
        ----------
        ids (list) -- List of node identifiers

        Returns
        -------
        index (numpy.ndarray) -- Array with the positions of points in the array
        """
        ids = np.array(ids)
        # index = np.where(np.isin(self.ids, ids))[0]
        index = [np.where(self.ids == id)[0][0] for id in ids]

        return index

    def findCoordinatesByNodeIds(self, ids):
        """
        Get coordinates and index for specific nodes.

        Parameters
        ----------
        ids (list) -- List of node identifiers

        Returns
        -------
        coordinates (numpy.ndarray) -- Array of coordinates for the specified nodes
        index (numpy.ndarray) -- Array with the positions of points in the array
        """
        ids = np.array(ids)
        # index = np.where(np.isin(self.ids, ids))[0]
        index = [np.where(self.ids == id)[0][0] for id in ids]
        coordinates = self.coordinates[index, :]

        return coordinates, index

    def printParameters(self):
        """
        Display the parameters of the _PointsBaseClass class in a structured manner.
        """
        print(f"Type: {self.type}")

        # Display coordinates
        print("Coordinates:")
        if self.coordinates.shape[0] > 20:
            print(self.coordinates[:20, :], "...")
        else:
            print(self.coordinates)

        # Display ids
        print("IDs:")
        if len(self.ids) > 20:
            print(self.ids[:20], "...")
        else:
            print(self.ids)

    def add(self, coordinate, id=None):
        """
        Add a single point (or node) to the existing ones.

        Parameters
        ----------
        coordinate (list) -- A list of x, y coordinates of the point to add
        id (int or None) -- Identifier for the new point (if None, auto-generated)
        """
        coordinate = np.array(coordinate)

        # Add the new coordinate to the coordinates array
        self.coordinates = np.vstack([self.coordinates, coordinate])

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id

        self.ids = np.append(self.ids, newId)
        return newId

    def plot(self, color="red"):
        """
        Plots the specific points
        """
        plt.scatter(self.x, self.y, c=color, s=50)
        for i, label in enumerate(self.ids):
            plt.text(self.x[i], self.y[i], label, fontsize=12, ha="right", c="red")
        plt.axis("square")


class _LoadsBaseClass:
    def __init__(self, type="default", loads=[], ids=[]):
        """
        Initialize a general loads object with specific attributes.

        Parameters
        ----------
        type (str) -- Load type identifier
        loads (list of lists) -- List of loads in x and y directions
        ids (list) -- List of load identifiers
        """
        self.type = type
        self.loads = np.array(loads)

        ids = np.array(ids)
        # Check if custom identifiers are given
        if ids.size == 0:
            self.ids = np.arange(1, self.loads.shape[0] + 1)
        else:
            self.ids = ids

    @property
    def x(self):
        """X loads"""
        return self.loads[:, 0]

    @property
    def y(self):
        """Y loads"""
        return self.loads[:, 1]

    def setLoads(self, loads):
        """
        Set loads in x and y directions.

        Parameters
        ----------
        loads (list of lists) -- List of loads in x and y directions
        """
        self.loads = np.array(loads)

    def setIds(self, ids):
        """
        Set identifiers for the loads.

        Parameters
        ----------
        ids (list) -- List of load identifiers
        """
        self.ids = np.array(ids)


class _DisplacementBaseClass:
    """
    Base class for boundaries, used for boundaries on nodes, points, lines
    """

    def __init__(self, type="default", displacements=[], ids=[]):
        """
        Initialize a _DisplacementBaseClass object.

        Parameters
        ----------
        type (str) -- Type of points (default: "default")
        displacements (list of lists) -- List of displacement contraints in x and y directions ("0" for fixed, "free" for free)
        ids (list) -- List of identifiers
        """
        self.displacements = displacements
        self.type = type

        ids = np.array(ids)
        # Check if custom identifiers are given
        if ids.size == 0:
            self.ids = np.arange(1, len(self.displacements) + 1)
        else:
            self.ids = ids

    @property
    def x(self):
        """Displacement in x direction"""
        return [disp[0] for disp in self.displacements]

    @property
    def y(self):
        """Displacement in y direction"""
        return [disp[1] for disp in self.displacements]

    def setDisplacements(self, displacements):
        """
        Sets the displacement constraints for the nodes.

        Parameters
        ----------
        displacement (list of lists) -- new displacement constraints in x and y directions ("0" for fixed, "1" for free)
        """
        self.displacements = displacements

    def setIds(self, ids):
        """
        Set identifiers for the loads.

        Parameters
        ----------
        ids (list) -- List of boundary identifiers
        """
        self.ids = np.array(ids)

    def printParameters(self):
        """
        Display the parameters of the _DisplacementBaseClass class in a structured manner.
        """
        print(f"Type: {self.type}")

        # Display displacements
        print("Displacements:")
        if len(self.displacements) > 5:
            print(self.displacements[:5, :], "...")
        else:
            print(self.displacements)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)
