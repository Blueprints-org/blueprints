import numpy as np
from matplotlib import pyplot as plt

from blueprints.utils.femlearn._base_classes import _PointsBaseClass


class Nodes(_PointsBaseClass):
    """
    Class for node objects, inheriting from _PointsBaseClass.
    """

    def __init__(self, coordinates=[], ids=[]):
        """
        Initialize a node object.

        Parameters
        ----------
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """
        super().__init__("node", coordinates, ids)


class Elements:
    type = "element"
    """
    Class representing elements with attributes such as nodes, thickness, Young's modulus, etc.
    """

    def __init__(
        self, nodeIds=[[]], integrationpointIds=[], integrationOrder=[], thickness=[], youngsModulus=[], poissonsRatio=[], planarAssumption=[], ids=[]
    ):
        """
        Initialize an Elements class with specific attributes.

        Parameters
        ----------
        nodeIds (list of lists) -- Lists containing node identifiers for each element
        integrationpointIds (list of lists) -- Lists containing integration point identifiers for each element
        integrationOrder (list) -- List of integration orders for each element
        thickness (list) -- List of thickness values for each element
        youngsModulus (list) -- List of Young's modulus values for each element
        poissonsRatio (list) -- List of Poisson's ratio values for each element
        planarAssumption (string)  -- Assumption ("plane stress","plane strain")
        ids (list) -- List of element identifiers
        """
        self.nodeIds = nodeIds
        self.integrationpointIds = integrationpointIds

        if np.isscalar(integrationOrder) or len(integrationOrder) == 1:
            self.integrationOrder = np.ones([len(self.nodeIds)]) * integrationOrder
        else:
            self.integrationOrder = np.array(integrationOrder)

        if np.isscalar(thickness) or len(thickness) == 1:
            self.thickness = np.ones([len(self.nodeIds)]) * thickness
        else:
            self.thickness = np.array(thickness)

        if np.isscalar(youngsModulus) or len(youngsModulus) == 1:
            self.youngsModulus = np.ones([len(self.nodeIds)]) * youngsModulus
        else:
            self.youngsModulus = np.array(youngsModulus)

        if np.isscalar(poissonsRatio) or len(poissonsRatio) == 1:
            self.poissonsRatio = np.ones([len(self.nodeIds)]) * poissonsRatio
        else:
            self.poissonsRatio = np.array(poissonsRatio)

        if isinstance(planarAssumption, str) or len(planarAssumption) == 1:
            self.planarAssumption = np.full([len(self.nodeIds)], planarAssumption)
        else:
            self.planarAssumption = np.array(planarAssumption)

        ids = np.array(ids)
        if ids.size == 0:
            self.ids = np.arange(1, len(self.nodeIds) + 1)
        else:
            self.ids = ids

    def setIds(self, ids):
        """
        Set identifiers.

        Parameters
        ----------
        ids (list) -- List of identifiers
        """
        self.ids = np.array(ids)

    def setNodeIds(self, nodeIds):
        """
        Set the nodeIds attribute.

        Parameters
        ----------
        nodeIds (list of lists) -- Lists containing node identifiers for each element
        """
        self.nodeIds = nodeIds

    def findIndexByElementIds(self, ids):
        """
        Get array index for specific elements.

        Parameters
        ----------
        ids (list) -- List of element identifiers

        Returns
        -------
        index (numpy.ndarray) -- Array with the positions of elements in the array
        """
        ids = np.array(ids)
        index = np.where(np.isin(self.ids, ids))[0]

        return index

    def findNodeIdsByElementId(self, id):
        """
        Get node identifiers for a specific element.

        Parameters
        ----------
        id (int) -- Element identifier

        Returns
        -------
        nodeIds (list) -- List with nodes of the specific element
        index (int) -- Position of the specific element in the array
        """
        index = next((i for i, element in enumerate(self.ids) if element == id), None)

        if index is None:
            return None, None

        nodeIds = self.nodeIds[index]

        return nodeIds, index

    def setIntegrationpointIds(self, integrationpointIds):
        """
        Set the integrationpointIds attribute.

        Parameters
        ----------
        integrationpointIds (list of lists) -- Lists containing integration point identifiers for each element
        """
        self.integrationpointIds = integrationpointIds

    def findIntegrationpointIdsByElementId(self, id):
        """
        Get integration point identifiers for a specific element.

        Parameters
        ----------
        id (int) -- Element identifier

        Returns
        -------
        integrationpointIds (list) -- List with integration points of the specific element
        index (int) -- Position of the specific element in the array
        """
        index = next((i for i, element in enumerate(self.ids) if element == id), None)

        if index is None:
            return None, None

        integrationpointIds = self.integrationpointIds[index]

        return integrationpointIds, index

    def setThickness(self, thickness):
        """
        Set the thickness attribute.

        Parameters
        ----------
        thickness (list) -- List of thickness values for each element
        """
        if np.isscalar(thickness) or len(thickness) == 1:
            self.thickness = np.ones([len(self.nodeIds)]) * thickness
        else:
            self.thickness = np.array(thickness)

    def setYoungsModulus(self, youngsModulus):
        """
        Set the youngsModulus attribute.

        Parameters
        ----------
        youngsModulus (list) -- List of Young's modulus values for each element
        """
        if np.isscalar(youngsModulus) or len(youngsModulus) == 1:
            self.youngsModulus = np.ones([len(self.nodeIds)]) * youngsModulus
        else:
            self.youngsModulus = np.array(youngsModulus)

    def setPoissonsRatio(self, poissonsRatio):
        """
        Set the poissonsRatio attribute.

        Parameters
        ----------
        poissonsRatio (list) -- List of Poisson's ratio values for each element
        """
        if np.isscalar(poissonsRatio) or len(poissonsRatio) == 1:
            self.poissonsRatio = np.ones([len(self.nodeIds)]) * poissonsRatio
        else:
            self.poissonsRatio = np.array(poissonsRatio)

    def setPlanarAssumption(self, planarAssumption):
        """
        Set the planarAssumption attribute.

        Parameters
        ----------
        planarAssumption (string)  -- Assumption ("plane stress" or "plane strain")
        """
        if isinstance(planarAssumption, str) or len(planarAssumption) == 1:
            self.planarAssumption = np.full([len(self.nodeIds)], planarAssumption)
        else:
            self.planarAssumption = np.array(planarAssumption)

    def printParameters(self):
        """
        Display the parameters of the Elements class in a structured manner.
        """
        print(f"Type: {self.type}")

        # Display node IDs
        print("Node IDs:")
        if len(self.nodeIds) > 20:
            print(self.nodeIds[:20])
        else:
            print(self.nodeIds)

        # Display integration point IDs
        print("Integration Point IDs:")
        if len(self.integrationpointIds) > 20:
            print(self.integrationpointIds[:20], "...")
        else:
            print(self.integrationpointIds)

        # Display thickness
        print("Thickness:")
        if len(self.thickness) > 20:
            print(self.thickness[:20], "...")
        else:
            print(self.thickness)

        # Display Young's modulus
        print("Young's Modulus:")
        if len(self.youngsModulus) > 20:
            print(self.youngsModulus[:20], "...")
        else:
            print(self.youngsModulus)

        # Display Poisson's ratio
        print("Poisson's Ratio:")
        if len(self.poissonsRatio) > 20:
            print(self.poissonsRatio[:20], "...")
        else:
            print(self.poissonsRatio)

        # Display ids
        print("Element IDs:")
        if len(self.ids) > 20:
            print(self.ids[:20], "...")
        else:
            print(self.ids)

        # Display ids
        print("Assumption:")
        if len(self.planarAssumption) > 20:
            print(self.planarAssumption[:20], "...")
        else:
            print(self.planarAssumption)

    def add(self, nodeId, integrationPointId, thickness, youngsModulus, poissonsRatio, planarAssumption, id=None):
        """
        Add a single element to the existing elements.

        Parameters
        ----------
        nodeId (list) -- A list of node identifiers for the new element
        integrationPointId (list) -- A list of integration point identifiers for the new element
        thickness (float) -- Thickness value of the new element
        youngsModulus (float) -- Young's modulus value of the new element
        poissonsRatio (float) -- Poisson's ratio value of the new element
        id (int or None) -- Identifier for the new element (if None, auto-generated)
        """
        # Add the new element's attributes to the existing lists
        self.nodeIds.append(nodeId)
        self.integrationpointIds.append(integrationPointId)
        self.thickness = np.append(self.thickness, thickness)
        self.youngsModulus = np.append(self.youngsModulus, youngsModulus)
        self.poissonsRatio = np.append(self.poissonsRatio, poissonsRatio)
        self.planarAssumption = np.append(self.planarAssumption, planarAssumption)

        # Add the new ID or generate an ID if not provided
        if id is None:
            newId = self.ids.max() + 1 if self.ids.size > 0 else 1
        else:
            newId = id
        self.ids = np.append(self.ids, newId)


class IntegrationPoints(_PointsBaseClass):
    """
    Class for integration points, inheriting from _PointsBaseClass.
    """

    def __init__(self, coordinates=[], ids=[]):
        """
        Initialize an integration points object.

        Parameters
        ----------
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """
        super().__init__("integration point", coordinates, ids)


class Mesh:
    """
    Mesh class. Contains Nodes and Elements of model.
    """

    def __init__(self, nodes=Nodes(), elements=Elements()):
        """
        Initialize a Mesh class

        Parameters
        ----------
        nodes (object) -- Object of type Nodes
        elements (object) -- Object of type Elements
        """
        self.nodes = nodes
        self.elements = elements
        self.integrationPoints = IntegrationPoints()

    @property
    def numberOfElements(self):
        """Number of elements in the mesh"""
        return self.elements.ids.shape[0]

    @property
    def numberOfNodes(self):
        """Number of nodes in the mesh"""
        return self.nodes.ids.shape[0]

    def setNodes(self, nodes):
        """
        Set the nodes object for the model.

        Parameters
        ----------
        nodes (Nodes) -- Object of type Nodes
        """
        if isinstance(nodes, Nodes):
            self.nodes = nodes
            # self.numberOfNodes = nodes.ids.shape[0]
        else:
            raise TypeError("Object is not of type Nodes!")

    def getNodes(self):
        """
        Get the nodes object of the model.

        Returns
        -------
        nodes (Nodes) -- Object of type Nodes
        """
        return self.nodes

    def getNodeSelection(self, ids):
        """
        Get nodes object of model based on their identifier.

        Parameters
        ----------
        ids (list) -- List with identifiers

        Return:
        nodes (Nodes) -- Object of type Nodes
        """
        nodeIndex = self.nodes.findIndexByNodeIds(ids)

        return Nodes(self.nodes.getCoordinates()[nodeIndex], self.nodes.ids[nodeIndex])

    def setElements(self, elements):
        """
        Set the Elements object for the model.

        Parameters
        ----------
        elements (Elements) -- Object of type Elements
        """
        if isinstance(elements, Elements):
            self.elements = elements
            # self.numberOfElements = elements.ids.shape[0]
        else:
            raise TypeError("Object is not of type Elements!")

    def getElements(self):
        """
        Get the Elements object of the model.

        Returns
        -------
        elements (Elements) -- Object of type Elements
        """
        return self.elements

    def getElementSelection(self, ids):
        """
        Get element object of model based on their identifier.

        Parameters
        ----------
        ids (list) -- List with element identifiers

        Return:
        elements (Elements) -- Object of type Elements
        """
        elementIndex = self.elements.findIndexByElementIds(ids)

        return Elements(
            self.elements.nodeIds[elementIndex],
            self.elements.integrationpointIds[elementIndex],
            self.elements.thickness[elementIndex],
            self.elements.youngsModulus[elementIndex],
            self.elements.poissonsRatio[elementIndex],
            self.elements.ids[elementIndex],
        )

    def getNodesOfElementId(self, id):
        """
        Find and return a Node object with just the nodes that belong to a specific element.

        Parameters
        ----------
        id (int)-- Single element identifier

        Return:
        nodes (Nodes) -- Object of type Nodes
        """
        # Find node ids of specific element by using element method
        nodeIds, index = self.elements.findNodeIdsByElementId(id)

        # Find position of node ids in model Nodes object
        nodeCoordinates, nodeIndex = self.nodes.findCoordinatesByNodeIds(nodeIds)

        #  create new Nodes object with specific nodes from model
        nodesFound = Nodes(nodeCoordinates, self.nodes.ids[nodeIndex])

        return nodesFound

    def setIntegrationPoints(self, integrationPoints):
        """
        Set the IntegrationPoints object for the model.

        Parameters
        ----------
        integrationPoints (IntegrationPoints) -- Object of type IntegrationPoints
        """
        if isinstance(integrationPoints, IntegrationPoints):
            self.integrationPoints = integrationPoints
        else:
            raise TypeError("Object is not of type IntegrationPoints!")

    def getIntegrationPoints(self):
        """
        Get the IntegrationPoints object of the model.

        Returns
        -------
        integrationPoints (IntegrationPoints) -- Object of type IntegrationPoints
        """
        return self.integrationPoints

    def plotMesh(self, color_test=False, show_ids=False):
        """
        Plots the mesh

        Parameters
        ----------
        color_test (bool) -- ???
        show_ids (bool) -- True displays node identifiers
        """
        for elementIndex, elementNodeIds in enumerate(self.elements.nodeIds):
            elementNodeIds = np.array(elementNodeIds)
            # If elementtype is TRIA6: use defined order to get correct nodes
            if len(elementNodeIds) == 6:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds[[0, 3, 1, 4, 2, 5]])
            # If elementtype is Quad8: use defined order to get correct nodes
            elif len(elementNodeIds) == 8:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds[[0, 4, 1, 5, 2, 6, 3, 7]])
            else:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds)

            coords = self.nodes.coordinates[elementNodeIndex]

            midpoint = np.mean(coords, axis=0)
            if color_test == False:
                color = "none"
            else:
                cmap = plt.get_cmap("jet")
                color = cmap(elementIndex / self.elements.ids.shape[0])

            plt.fill(coords[:, 0], coords[:, 1], edgecolor="cyan", facecolor=color)

            if show_ids == True:
                plt.text(midpoint[0], midpoint[1], self.elements.ids[elementIndex], fontsize=12, color="cyan", ha="center", va="center")

            plt.axis("square")

    def printParameters(self):
        """
        Display the parameters of the Mesh class in a structured manner.
        """
        print("-----------------------------\n\t NODES\n-----------------------------")
        self.nodes.printParameters()
        print("-----------------------------\n\t ELEMENTS\n-----------------------------")
        self.elements.printParameters()
