import numpy as np

from blueprints.utils.femlearn import _LoadsBaseClass


class LoadsOnNodes(_LoadsBaseClass):
    """
    Inherits from the general _LoadsBaseClass class to define loads on nodes.
    """

    def __init__(self, loads=[], nodeIds=[], ids=[]):
        """
        Initialize a LoadsOnNodes object.

        Parameters:
        loads (list of lists) -- List of loads in x and y directions
        nodeIds (list) -- List of node identifiers
        ids (list) -- List of load identifiers
        """
        super().__init__("node load", loads, ids)
        self.nodeIds = np.array(nodeIds)

    def setNodeIds(self, nodeIds):
        """
        Set node identifiers for the loads.

        Parameters:
        nodeIds (list) -- List of node identifiers
        """
        self.nodeIds = np.array(nodeIds)

    def printParameters(self):
        """
        Display the parameters of the LoadsOnNodes class in a structured manner.
        """
        print(f"Type: {self.type}")
        print(f"Number of Loads on Nodes: {self.ids.shape[0]}")

        # Display loads
        print("Load:")
        if self.ids.shape[0] > 5:
            print(self.loads[:5, :], "...")
        else:
            print(self.loads)

        # Node ids
        print("Node IDs:")
        if len(self.nodeIds) > 5:
            print(self.nodeIds[:5], "...")
        else:
            print(self.nodeIds)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)

    def add(self, load, nodeId, id=None):
        """
        Add a single node load to the existing loads.

        Parameters:
        load (list) -- A list of loads in x and y directions
        nodeId (int) -- Identifier of the node the load is applied on
        id (int or None) -- Identifier for the new load (if None, auto-generated)
        """
        load = np.array(load)

        # Check if self.loads is empty (has size 0)
        if self.loads.size == 0:
            # Initialize self.loads with the correct shape
            self.loads = np.array([load])
        else:
            # Stack the new load to the existing loads array
            self.loads = np.vstack([self.loads, load])

        # Append the new nodeId
        self.nodeIds = np.append(self.nodeIds, nodeId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)


class LoadsOnPoints(_LoadsBaseClass):
    """
    Inherits from the general _LoadsBaseClass class to define loads on points.
    """

    def __init__(self, loads=[], pointIds=[], ids=[]):
        """
        Initialize a LoadsOnPoints object.

        Parameters:
        loads (list of lists) -- List of loads in x and y directions
        pointIds (list) -- List of point identifiers
        ids (list) -- List of load identifiers
        """
        super().__init__("point load", loads, ids)
        self.pointIds = np.array(pointIds)

    def setpointIds(self, pointIds):
        """
        Set point identifiers for the loads.

        Parameters:
        pointIds (list) -- List of point identifiers
        """
        self.pointIds = np.array(pointIds)

    def printParameters(self):
        """
        Display the parameters of the LoadsOnPoints class in a structured manner.
        """
        print(f"Type: {self.type}")
        print(f"Number of Loads on Points: {self.ids.shape[0]}")

        # Display loads
        print("Loads:")
        if self.ids.shape[0] > 5:
            print(self.loads[:5, :], "...")
        else:
            print(self.loads)

        #  point ids
        print("Point IDs:")
        if len(self.pointIds) > 5:
            print(self.pointIds[:5], "...")
            print(self.pointIds[-5:])
        else:
            print(self.pointIds)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)

    def add(self, load, referencePointId, id=None):
        """
        Add a single point load to the existing loads.

        Parameters:
        load (list) -- A list of loads in x and y directions
        pointIds (int) --  Identifier of the point the load is applied on
        id (int or None) -- Identifier for the new load (if None, auto-generated)
        """
        load = np.array(load)

        # Add the new load and point ids to the existing loads array
        self.loads = np.vstack([self.loads, load])
        self.pointIds = np.append(self.pointIds, referencePointId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)


class LoadsOnLines(_LoadsBaseClass):
    """
    Inherits from the general _LoadsBaseClass class to define loads on lines.
    """

    def __init__(self, loads=[], lineIds=[], ids=[]):
        """
        Initialize a LoadsOnLines object.

        Parameters:
        loads (list of lists) -- List of loads in x and y directions
        lineIds (list) -- List of line identifiers
        ids (list) -- List of load identifiers
        """
        super().__init__("line load", loads, ids)
        self.lineIds = np.array(lineIds)

    def setLineIds(self, lineIds):
        """
        Set line identifiers for the loads.

        Parameters:
        lineIds (list) -- List of line identifiers
        """
        self.lineIds = np.array(lineIds)

    def printParameters(self):
        """
        Display the parameters of the LoadsOnLines class in a structured manner.
        """
        print(f"Type: {self.type}")
        print(f"Number of Loads on Lines: {self.ids.shape[0]}")

        # Display loads
        print("Loads:")
        if self.ids.shape[0] > 5:
            print(self.loads[:5, :], "...")
        else:
            print(self.loads)

        # Line ids
        print("Line IDs:")
        if len(self.lineIds) > 5:
            print(self.lineIds[:5], "...")
        else:
            print(self.lineIds)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)

    def add(self, load, lineId, id=None):
        """
        Add a single line load to the existing loads.

        Parameters:
        load (list) -- A list of loads in x and y directions
        lineId (int) --  Identifier of the line the load is applied on
        id (int or None) -- Identifier for the new load (if None, auto-generated)
        """
        load = np.array(load)

        # Add the new load and line ids to the existing loads array
        self.loads = np.vstack([self.loads, load])
        self.lineIds = np.append(self.lineIds, lineId)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)


class Loads:
    """
    Loads class. Contains the different types of loads defined in the model
    """

    def __init__(self, loadsOnNodes=LoadsOnNodes(), loadsOnPoints=LoadsOnPoints(), loadsOnLines=LoadsOnLines()):
        """
        Initialize a Mesh class

        Parameters:
        nodes (object) -- Object of type Nodes
        elements (object) -- Object of type Elements
        """
        self.loadsOnNodes = loadsOnNodes
        self.loadsOnPoints = loadsOnPoints
        self.loadsOnLines = loadsOnLines

    def setLoadsOnNodes(self, loadsOnNodes):
        """
        Set the LoadsOnNodes object for the model.

        Parameters:
        loadsOnNodes (LoadsOnNodes) -- Object of type LoadsOnNodes
        """
        if isinstance(loadsOnNodes, LoadsOnNodes):
            self.loadsOnNodes = loadsOnNodes
        else:
            raise TypeError("Object is not of type LoadsOnNodes!")

    def getLoadsOnNodes(self):
        """
        Get the LoadsOnNodes object of the model.

        Returns:
        loadsOnNodes (LoadsOnNodes) -- Object of type LoadsOnNodes
        """
        return self.loadsOnNodes

    def setLoadsOnPoints(self, loadsOnPoints):
        """
        Set the LoadsOnPoints object for the model.

        Parameters:
        loadsOnPoints (LoadsOnPoints) -- Object of type LoadsOnPoints
        """
        if isinstance(loadsOnPoints, LoadsOnPoints):
            self.loadsOnPoints = loadsOnPoints
        else:
            raise TypeError("Object is not of type LoadsOnPoints!")

    def getLoadsOnPoints(self):
        """
        Get the LoadsOnPoints object of the model.

        Returns:
        loadsOnPoints (LoadsOnPoints) -- Object of type LoadsOnPoints
        """
        return self.loadsOnPoints

    def setLoadsOnLines(self, loadsOnLines):
        """
        Set the LoadsOnLines object for the model.

        Parameters:
        loadsOnLines (LoadsOnLines) -- Object of type LoadsOnLines
        """
        if isinstance(loadsOnLines, LoadsOnLines):
            self.loadsOnLines = loadsOnLines
        else:
            raise TypeError("Object is not of type LoadsOnLines!")

    def getLoadsOnLines(self):
        """
        Get the LoadsOnLines object of the model.

        Returns:
        loadsOnLines (LoadsOnLines) -- Object of type LoadsOnLines
        """
        return self.loadsOnLines

    def printParameters(self):
        """
        Display the parameters of the Loads class in a structured manner.
        """
        print("-----------------------------\n\t LOADS ON NODES\n-----------------------------")
        self.loadsOnNodes.printParameters()
        print("-----------------------------\n\t LOADS ON POINTS\n-----------------------------")
        self.loadsOnPoints.printParameters()
        print("-----------------------------\n\t LOADS ON LINES\n-----------------------------")
        self.loadsOnLines.printParameters()
