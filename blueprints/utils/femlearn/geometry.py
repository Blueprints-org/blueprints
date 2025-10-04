import numpy as np
from matplotlib import pyplot as plt

from blueprints.utils.femlearn._base_classes import _PointsBaseClass


class Points(_PointsBaseClass):
    """
    Class for points, inheriting from _PointsBaseClass.
    """

    def __init__(self, coordinates=[], ids=[]):
        """
        Initialize a geometrical points object.

        Parameters:
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """
        super().__init__("point", coordinates, ids)


class Lines:
    type = "line"

    def __init__(self, pointIds=[], ids=[]):
        """
        Initialize a Lines object.

        Parameters:
        pointIds (list) -- List of points for each line
        ids (list) -- List of line identifiers
        """
        self.pointIds = np.array(pointIds)
        ids = np.array(ids)

        # Check if custom identifiers are given
        if ids.size == 0:
            self.ids = np.arange(1, self.pointIds.shape[0] + 1)
        else:
            self.ids = ids

    def setPoints(self, pointIds):
        """
        Set points for the lines.

        Parameters:
        pointIds (list) -- List of points for each line
        """
        self.pointIds = np.array(pointIds)

    def setIds(self, ids):
        """
        Set identifiers for the lines.

        Parameters:
        ids (list) -- List of identifiers
        """
        self.ids = np.array(ids)

    def _findIndexByLineIds(self, ids):
        """
        Get index for specific lines.

        Parameters:
        ids (list) -- List of line identifiers

        Returns:
        index (numpy.ndarray) -- Array with the positions of lines in the array
        """
        # Check if ids is a scalar, if so, convert it to a list
        if np.isscalar(ids):
            ids = [ids]

        ids = np.array(ids)
        index = [np.where(self.ids == id)[0][0] for id in ids]

        return index

    def printParameters(self):
        """
        Display the parameters of the Lines class in a structured manner.
        """
        print(f"Type: {self.type}")
        print(f"Number of Lines: {self.ids.shape[0]}")

        # Display coordinates
        print("Vertices:")
        if self.ids.shape[0] > 5:
            for point in self.pointIds[:5]:
                print(point)
            print("...")
        else:
            for point in self.pointIds:
                print(point)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)

    def add(self, referencePointId, id=None):
        """
        Add a single line to the existing lines.

        Parameters:
        referencePointId (list) -- A list of points for the new line
        id (int or None) -- Identifier for the new line (if None, auto-generated)
        """
        # Add the new point id to the existing array
        self.pointIds = np.vstack([self.pointIds, referencePointId])

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)


class Geometry:
    """
    Geometry class. Contains the geometrical points and lines of model.
    """

    def __init__(self, points=Points(), lines=Lines()):
        """
        Initialize a Mesh class

        Parameters:
        nodes (object) -- Object of type Nodes
        elements (object) -- Object of type Elements
        """
        self.points = points
        self.lines = lines

    def setPoints(self, points):
        """
        Set the Points object for the model.

        Parameters:
        points (Points) -- Object of type Points
        """
        if isinstance(points, Points):
            self.points = points
        else:
            raise TypeError("Object is not of type Points!")

    def setLines(self, lines):
        """
        Set the Lines object for the model.

        Parameters:
        lines (Lines) -- Object of type Lines
        """
        if isinstance(lines, Lines):
            self.lines = lines
        else:
            raise TypeError("Object is not of type Lines!")

    def makePolygon(self, coordinates):
        """
        Generates Points and Lines so that they form a polygon as defined by the vertices.
        Vertices have to be defined counterclockwise.

        Parameters:
        coordinates (list of list) -- coordinates of polygon vertices
        """
        self.points = Points(coordinates, ids=np.arange(1, len(coordinates) + 1))
        n = self.points.coordinates.shape[0]

        # Create lines connecting the points counterclockwise, for all vertices
        lineIds = np.ones([n, 2])
        lineIds[:, 0] = np.arange(1, n + 1)
        lineIds[0:-1:, 1] = np.arange(2, n + 1)
        self.lines = Lines(pointIds=lineIds)
        pass

    def plot(self):
        """
        Plots all Points and Lines defined in the model
        """
        self.points.plot()
        for label_id, ids in enumerate(self.lines.pointIds):
            # coords=self.points.coordinates[ids]
            coords = self.points.findCoordinatesByNodeIds(ids)[0]
            x = coords[:, 0]
            y = coords[:, 1]
            plt.plot(x, y, color="c")
            plt.text(np.mean(x), np.mean(y), self.lines.ids[label_id], fontsize=12, ha="right", color="c")
        plt.axis("square")

    def printParameters(self):
        """
        Display the parameters of the Geometry class in a structured manner.
        """
        print("-----------------------------\n\t POINTS\n-----------------------------")
        self.points.printParameters()
        print("-----------------------------\n\t LINES\n-----------------------------")
        self.lines.printParameters()
