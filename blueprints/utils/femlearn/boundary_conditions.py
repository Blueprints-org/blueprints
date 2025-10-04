import numpy as np

from blueprints.utils.femlearn import _DisplacementBaseClass


class DisplacementOnNodes(_DisplacementBaseClass):
    def __init__(self, displacements=[[]], nodeIds=[], ids=[]):
        """
        Initialize a DisplacementOnNodes object with specific attributes.

        Parameters:
        displacement (list of lists) -- List of displacement constraints in x and y directions ("0" for fixed, "1" for free)
        nodeIds (list) -- List of node ids to apply constraint
        ids (list) -- List of identifiers
        """
        super().__init__("displacement on node", displacements, ids)
        self.nodeIds = np.array(nodeIds)

    def setNodeIds(self, nodeIds):
        """
        Sets the node ids to which the displacements are applied.

        Parameters:
        nodeIds (list) -- List of new node ids
        """
        self.nodeIds = np.array(nodeIds)

    def _getNodeIdsWithFixationX(self):
        """
        Returns the node Ids for which the displacements in x directions is zero.
        """
        xFixationNodeId = []
        for index, id in enumerate(self.nodeIds):
            if self.x[index] == 0:
                xFixationNodeId.append(id)
        return np.array(xFixationNodeId)

    def _getNodeIdsWithFixationY(self):
        """
        Returns the node Ids for which the displacements in y directions is zero.
        """
        yFixationNodeId = []
        for index, id in enumerate(self.nodeIds):
            if self.y[index] == 0:
                yFixationNodeId.append(id)
        return np.array(yFixationNodeId)

    def _getPrescribedNodalDispalcementX(self):
        """
        Returns the prescriped nodal displacement and Ids for which the displacements in x directions is not or free zero.
        """
        xDispNodeId = []
        xDisp = []
        for index, id in enumerate(self.nodeIds):
            if not (self.x[index] in [0, "free", None]):
                xDispNodeId.append(id)
                xDisp.append(float(self.x[index]))
        return np.array(xDisp), np.array(xDispNodeId)

    def _getPrescribedNodalDispalcementY(self):
        """
        Returns the prescriped nodal displacement and Ids for which the displacements in y directions is not or free zero.
        """
        yDispNodeId = []
        yDisp = []
        for index, id in enumerate(self.nodeIds):
            if not (self.y[index] in [0, "free", None]):
                yDispNodeId.append(id)
                yDisp.append(float(self.y[index]))
        return np.array(yDisp), np.array(yDispNodeId)

    def add(self, displacement, nodeId, id=None):
        """
        Add a single displacement on a node.

        Parameters:
        displacement (list) -- A list of displacement constraints (x, y) for the new boundary
        nodeId (int) -- Node identifier for the new boundary
        id (int or None) -- Identifier for the new boundary (if None, auto-generated)
        """

        # Check if self.displacement is empty
        if len(self.displacements[0]) == 0:
            # Initialize self.displacement with the correct shape
            self.displacements = [displacement]
        else:
            # Stack the new displacement to the existing displacement list
            self.displacements.append(displacement)

        self.nodeIds = np.append(self.nodeIds, nodeId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)

    def printParameters(self):
        """
        Display the parameters of the DisplacementOnNodes class in a structured manner.
        """
        super().printParameters()

        # Display point IDs
        print("Node IDs:")
        if len(self.nodeIds) > 5:
            print(self.nodeIds[:5], "...")
        else:
            print(self.nodeIds)

    def remove(self, id):
        """
        Removes the displacement associated with the given identifier of the nodal displacement boundary condition.

        Parameters:
        id (int) -- The identifier of the nodal displacement boundary condition to be removed

        Returns:
        bool -- True if removal was successful, False if id not found
        """
        # Find the index of the id to remove
        index = np.where(self.ids == id)[0]

        if len(index) == 0:
            # nodeId not found
            return False

        index = index[0]

        # Remove the displacement, nodeId, and id at the found index
        self.displacements = np.delete(self.displacements, index, axis=0)
        self.nodeIds = np.delete(self.nodeIds, index)
        self.ids = np.delete(self.ids, index)

        return True


class DisplacementOnPoints(_DisplacementBaseClass):
    def __init__(self, displacements=[], pointIds=[], ids=[]):
        """
        Initialize a DisplacementOnPoints object with specific attributes.

        Parameters:
        displacement (list of lists) -- List of displacement constraints in x and y directions ("0" for fixed, "1" for free)
        pointIds (list) -- List of point ids to apply constraint
        ids (list) -- List of identifiers
        """
        super().__init__("displacement on point", displacements, ids)
        self.pointIds = np.array(pointIds)

    def setpointIds(self, pointIds):
        """
        Sets the point ids to which the displacements are applied.

        Parameters:
        pointIds (list) -- List of new point ids
        """
        self.pointIds = np.array(pointIds)
        self.pointIds = self.pointIds.shape[0]

    def add(self, displacement, referencePointId, id=None):
        """
        Add a single displacement on a point.

        Parameters:
        displacement (list) -- A list of displacement constraints (x, y) for the new boundary
        referencePointId (int) --  point identifier for the new boundary
        id (int or None) -- Identifier for the new boundary (if None, auto-generated)
        """

        # Check if self.displacement is empty
        if len(self.displacements[0]) == 0:
            # Initialize self.displacement with the correct shape
            self.displacements = [displacement]
        else:
            # Stack the new displacement to the existing displacement list
            self.displacements.append(displacement)

        self.pointIds = np.append(self.pointIds, referencePointId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)

    def printParameters(self):
        """
        Display the parameters of the DisplacementOnPoints class in a structured manner.
        """
        super().printParameters()

        # Display point IDs
        print("Point IDs:")
        if len(self.pointIds) > 5:
            print(self.pointIds[:5], "...")
        else:
            print(self.pointIds)


class DisplacementOnLines(_DisplacementBaseClass):
    def __init__(self, displacements=[], lineIds=[], ids=[]):
        """
        Initialize a DisplacementOnLines object with specific attributes.

        Parameters:
        displacement (list of lists) -- List of displacement constraints in x and y directions ("0" for fixed, "1" for free)
        lineIds (list) -- List of line ids to apply constraint
        ids (list) -- List of identifiers
        """
        super().__init__("displacement on line", displacements, ids)
        self.lineIds = np.array(lineIds)

    def setLineIds(self, lineIds):
        """
        Sets the line ids to which the displacements are applied.

        Parameters:
        lineIds (list) -- List of new line ids
        """
        self.lineIds = np.array(lineIds)
        self.lineIds = self.lineIds.shape[0]

    def add(self, displacement, lineId, id=None):
        """
        Add a single displacement on a line.

        Parameters:
        displacement (list) -- A list of displacement constraints (x, y) for the new boundary
        lineId (int) --  line identifier for the new boundary
        id (int or None) -- Identifier for the new boundary (if None, auto-generated)
        """

        # Check if self.displacement is empty
        if len(self.displacements[0]) == 0:
            # Initialize self.displacement with the correct shape
            self.displacements = [displacement]
        else:
            # Stack the new displacement to the existing displacement list
            self.displacements.append(displacement)

        self.lineIds = np.append(self.lineIds, lineId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)

    def printParameters(self):
        """
        Display the parameters of the DisplacementOnLines class in a structured manner.
        """
        super().printParameters()

        # Display line IDs
        print("Line IDs:")
        if len(self.lineIds) > 5:
            print(self.lineIds[:5], "...")
        else:
            print(self.lineIds)


class Boundaries:
    """
    Boundaries class. Contains the different types of boundary conditions defined in the model
    """

    def __init__(
        self, displacementOnNodes=DisplacementOnNodes(), displacementOnPoints=DisplacementOnPoints(), displacementOnLines=DisplacementOnLines()
    ):
        """
        Initialize a Mesh class

        Parameters:
        nodes (object) -- Object of type Nodes
        elements (object) -- Object of type Elements
        """
        self.displacementOnNodes = displacementOnNodes
        self.displacementOnPoints = displacementOnPoints
        self.displacementOnLines = displacementOnLines

    def setDisplacementOnNodes(self, displacementOnNodes):
        """
        Set the displacement on nodes for the model.

        Parameters:
        DisplacementOnNodes (DisplacementOnNodes) -- Object of type DisplacementOnNodes
        """
        if isinstance(displacementOnNodes, DisplacementOnNodes):
            self.displacementOnNodes = displacementOnNodes
        else:
            raise TypeError("Object is not of type DisplacementOnNodes!")

    def getDisplacementOnNodes(self):
        """
        Get the displacement on nodes for the model.

        Returns:
        DisplacementOnNodes (DisplacementOnNodes) -- Object of type DisplacementOnNodes
        """
        return self.displacementOnNodes

    def setDisplacementOnPoints(self, displacementOnPoints):
        """
        Set the displacement on geometrical points for the model.

        Parameters:
        DisplacementOnPoints (DisplacementOnPoints) -- Object of type DisplacementOnPoints
        """
        if isinstance(displacementOnPoints, DisplacementOnPoints):
            self.displacementOnPoints = displacementOnPoints
        else:
            raise TypeError("Object is not of type DisplacementOnPoints!")

    def getDisplacementOnPoints(self):
        """
        Get the displacement on points for the model.

        Returns:
        DisplacementOnPoints (DisplacementOnPoints) -- Object of type DisplacementOnPoints
        """
        return self.displacementOnPoints

    def setDisplacementOnLines(self, displacementOnLines):
        """
        Set the displacement on lines for the model.

        Parameters:
        DisplacementOnLines (DisplacementOnLines) -- Object of type DisplacementOnLines
        """
        if isinstance(displacementOnLines, DisplacementOnLines):
            self.displacementOnLines = displacementOnLines
        else:
            raise TypeError("Object is not of type DisplacementOnLines!")

    def getDisplacementOnLines(self):
        """
        Get the displacement on lines for the model.

        Returns:
        DisplacementOnLines (DisplacementOnLines) -- Object of type DisplacementOnLines
        """
        return self.displacementOnLines

    def printParameters(self):
        """
        Display the parameters of the Boundaries class in a structured manner.
        """
        print("-----------------------------\n\t DISPLACEMENT ON NODES\n-----------------------------")
        self.displacementOnNodes.printParameters()
        print("-----------------------------\n\t DISPLACEMENT ON POINTS\n-----------------------------")
        self.displacementOnPoints.printParameters()
        print("-----------------------------\n\t DISPLACEMENT ON LINES\n-----------------------------")
        self.displacementOnLines.printParameters()
