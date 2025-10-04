# -----------------------------------
# 
# femlearn.py
# 
# Authors: Victor Lueddemann and Emile Breyer
# 
# -----------------------------------

import copy
import math
from platform import node
import numpy as np
import time
import matplotlib.pyplot  as plt
import matplotlib.transforms as mtransforms


np.set_printoptions(precision=4, suppress=True, linewidth=300) # allows for more readable numpy arrays

# --- Base Classes ---
class _PointsBaseClass():
    """
    Base class for points, used for nodes, geometrical  points, integration points, etc.
    """    
    def __init__(self, type="default", coordinates=[[]], ids=[]):
    
        """
        Initialize a base points class.

        Parameters:
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
    def x(self):
        """X Coordinates"""
        return self.coordinates[:,0]
    
    @property
    def y(self):
        """Y Coordinates"""
        return self.coordinates[:,1]

    def setCoordinates(self, coordinates):
        """
        Set coordinates.

        Parameters:
        coordinates (list of lists) -- List of x, y coordinates
        """    
        self.coordinates = np.array(coordinates, dtype=np.float64)

        if self.ids.shape == 0:
            self.ids = np.arange(1, self.coordinates.shape[0] + 1)

    def setIds(self, ids):
        """
        Set identifiers.

        Parameters:
        ids (list) -- List of identifiers
        """           
        self.ids = np.array(ids)
    
    def findIndexByNodeIds(self, ids):
        """
        Get index for specific nodes.

        Parameters:
        ids (list) -- List of node identifiers

        Returns:
        index (numpy.ndarray) -- Array with the positions of points in the array
        """   
        ids = np.array(ids)
        #index = np.where(np.isin(self.ids, ids))[0]
        index = [np.where(self.ids == id)[0][0] for id in ids]

        return index     

    def findCoordinatesByNodeIds(self, ids):
        """
        Get coordinates and index for specific nodes.

        Parameters:
        ids (list) -- List of node identifiers

        Returns:
        coordinates (numpy.ndarray) -- Array of coordinates for the specified nodes
        index (numpy.ndarray) -- Array with the positions of points in the array
        """   
        ids = np.array(ids)
        #index = np.where(np.isin(self.ids, ids))[0]
        index = [np.where(self.ids == id)[0][0] for id in ids]
        coordinates = self.coordinates[index,:]

        return coordinates, index        

    def printParameters(self):
        """
        Display the parameters of the _PointsBaseClass class in a structured manner.
        """
        print(f"Type: {self.type}")
                
        # Display coordinates
        print("Coordinates:")
        if self.coordinates.shape[0] > 20:
            print(self.coordinates[:20,:], "...")
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

        Parameters:
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
    def plot(self,color = 'red'):
        """
        Plots the specific points
        """
        plt.scatter(self.x,self.y,c=color,s=50)
        for i,label in enumerate(self.ids):
            plt.text(self.x[i], self.y[i], label, fontsize=12, ha='right',c='red')
        plt.axis('square')

class _LoadsBaseClass():
    def __init__(self, type="default", loads=[], ids=[]):
        """
        Initialize a general loads object with specific attributes.

        Parameters:
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
        return self.loads[:,0]
    
    @property
    def y(self):
        """Y loads"""
        return self.loads[:,1]

    def setLoads(self, loads):
        """
        Set loads in x and y directions.

        Parameters:
        loads (list of lists) -- List of loads in x and y directions
        """
        self.loads = np.array(loads)

    def setIds(self, ids):
        """
        Set identifiers for the loads.

        Parameters:
        ids (list) -- List of load identifiers
        """
        self.ids = np.array(ids)

class _DisplacementBaseClass():
    """
    Base class for boundaries, used for boundaries on nodes, points, lines
    """    
    def __init__(self, type="default", displacements=[], ids=[]):
        """
        Initialize a _DisplacementBaseClass object.

        Parameters:
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

        Parameters:
        displacement (list of lists) -- new displacement constraints in x and y directions ("0" for fixed, "1" for free)
        """
        self.displacements = displacements

    def setIds(self, ids):
        """
        Set identifiers for the loads.

        Parameters:
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
            print(self.displacements[:5,:], "...")
        else:
            print(self.displacements)

        # Display ids
        print("IDs:")
        if len(self.ids) > 5:
            print(self.ids[:5], "...")
        else:
            print(self.ids)


# --- Mesh ---
class Nodes(_PointsBaseClass):
    """
    Class for node objects, inheriting from _PointsBaseClass.
    """
    def __init__(self, coordinates=[], ids=[]):
        """
        Initialize a node object.

        Parameters:
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """ 
        super().__init__("node", coordinates, ids)

class Elements():
    type = "element"
    """
    Class representing elements with attributes such as nodes, thickness, Young's modulus, etc.
    """
    def __init__(self, nodeIds=[[]], integrationpointIds=[],integrationOrder=[], thickness=[], youngsModulus=[], poissonsRatio=[], planarAssumption=[], ids=[]):
        """
        Initialize an Elements class with specific attributes.

        Parameters:
        nodeIds (list of lists) -- Lists containing node identifiers for each element
        integrationpointIds (list of lists) -- Lists containing integration point identifiers for each element
        integrationOrder (list) -- List of integration orders for each element
        thickness (list) -- List of thickness values for each element
        youngsModulus (list) -- List of Young's modulus values for each element
        poissonsRatio (list) -- List of Poisson's ratio values for each element
        planarAssumption (string)  -- Assumption ("plane stress","plane strain")
        ids (list) -- List of element identifiers
        """
         
        self.nodeIds                = nodeIds                   
        self.integrationpointIds    = integrationpointIds

        if np.isscalar(integrationOrder) or len(integrationOrder) ==1:
            self.integrationOrder = np.ones([len(self.nodeIds)])*integrationOrder
        else:
            self.integrationOrder       = np.array(integrationOrder)

        if np.isscalar(thickness) or len(thickness) ==1:
            self.thickness = np.ones([len(self.nodeIds)])*thickness
        else:
            self.thickness       = np.array(thickness)

        if np.isscalar(youngsModulus) or len(youngsModulus) ==1:
            self.youngsModulus = np.ones([len(self.nodeIds)])*youngsModulus
        else:
            self.youngsModulus       = np.array(youngsModulus)
            
        if np.isscalar(poissonsRatio) or len(poissonsRatio) ==1:
            self.poissonsRatio = np.ones([len(self.nodeIds)])*poissonsRatio
        else:
            self.poissonsRatio       = np.array(poissonsRatio)

        if isinstance(planarAssumption, str) or len(planarAssumption) == 1:
            self.planarAssumption = np.full([len(self.nodeIds)], planarAssumption)
        else:
            self.planarAssumption       = np.array(planarAssumption)

        ids = np.array(ids)
        if ids.size == 0:
            self.ids = np.arange(1, len(self.nodeIds) + 1)
        else:
            self.ids = ids

    def setIds(self, ids):
        """
        Set identifiers.

        Parameters:
        ids (list) -- List of identifiers
        """           
        self.ids = np.array(ids)
    
    def setNodeIds(self, nodeIds):
        """
        Set the nodeIds attribute.

        Parameters:
        nodeIds (list of lists) -- Lists containing node identifiers for each element
        """
        self.nodeIds = nodeIds
    
    def findIndexByElementIds(self, ids):
        """
        Get array index for specific elements.

        Parameters:
        ids (list) -- List of element identifiers

        Returns:
        index (numpy.ndarray) -- Array with the positions of elements in the array
        """   
        ids = np.array(ids)
        index = np.where(np.isin(self.ids, ids))[0]

        return index   
    
    def findNodeIdsByElementId(self, id):
        """
        Get node identifiers for a specific element.

        Parameters:
        id (int) -- Element identifier

        Returns:
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

        Parameters:
        integrationpointIds (list of lists) -- Lists containing integration point identifiers for each element
        """
        self.integrationpointIds = integrationpointIds

    def findIntegrationpointIdsByElementId(self, id):
        """
        Get integration point identifiers for a specific element.

        Parameters:
        id (int) -- Element identifier

        Returns:
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

        Parameters:
        thickness (list) -- List of thickness values for each element
        """
        if np.isscalar(thickness) or len(thickness) ==1:
            self.thickness = np.ones([len(self.nodeIds)])*thickness
        else:
            self.thickness       = np.array(thickness)

    def setYoungsModulus(self, youngsModulus):
        """
        Set the youngsModulus attribute.

        Parameters:
        youngsModulus (list) -- List of Young's modulus values for each element
        """
        if np.isscalar(youngsModulus) or len(youngsModulus) ==1:
            self.youngsModulus = np.ones([len(self.nodeIds)])*youngsModulus
        else:
            self.youngsModulus       = np.array(youngsModulus)

    def setPoissonsRatio(self, poissonsRatio):
        """
        Set the poissonsRatio attribute.

        Parameters:
        poissonsRatio (list) -- List of Poisson's ratio values for each element
        """
        if np.isscalar(poissonsRatio) or len(poissonsRatio) ==1:
            self.poissonsRatio = np.ones([len(self.nodeIds)])*poissonsRatio
        else:
            self.poissonsRatio       = np.array(poissonsRatio)

    def setPlanarAssumption(self, planarAssumption):
        """
        Set the planarAssumption attribute.

        Parameters:
        planarAssumption (string)  -- Assumption ("plane stress" or "plane strain")
        """
        if isinstance(planarAssumption, str) or len(planarAssumption) == 1:
            self.planarAssumption = np.full([len(self.nodeIds)], planarAssumption)
        else:
            self.planarAssumption       = np.array(planarAssumption)

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

        Parameters:
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

        Parameters:
        coordinates (list of lists) -- List of x, y coordinates
        ids (list) -- List of identifiers
        """ 
        super().__init__("integration point", coordinates, ids)

class Mesh():
    """
    Mesh class. Contains Nodes and Elements of model.
    """    
    def __init__(self, nodes=Nodes(), elements=Elements()):
    
        """
        Initialize a Mesh class

        Parameters:
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

        Parameters:
        nodes (Nodes) -- Object of type Nodes
        """
        if isinstance(nodes, Nodes):
            self.nodes = nodes
            #self.numberOfNodes = nodes.ids.shape[0]
        else:
            raise TypeError("Object is not of type Nodes!")

    def getNodes(self):
        """
        Get the nodes object of the model.

        Returns:
        nodes (Nodes) -- Object of type Nodes
        """
        return self.nodes

    def getNodeSelection(self,ids):
        """
        Get nodes object of model based on their identifier.

        Parameters:
        ids (list) -- List with identifiers

        Return:
        nodes (Nodes) -- Object of type Nodes
        """
        nodeIndex = self.nodes.findIndexByNodeIds(ids)
        
        return Nodes(self.nodes.getCoordinates()[nodeIndex],self.nodes.ids[nodeIndex])

    def setElements(self, elements):
        """
        Set the Elements object for the model.

        Parameters:
        elements (Elements) -- Object of type Elements
        """
        if isinstance(elements, Elements):
            self.elements = elements
            #self.numberOfElements = elements.ids.shape[0]
        else:
            raise TypeError("Object is not of type Elements!")

    def getElements(self):
        """
        Get the Elements object of the model.

        Returns:
        elements (Elements) -- Object of type Elements
        """
        return self.elements

    def getElementSelection(self,ids):
        """
        Get element object of model based on their identifier.

        Parameters:
        ids (list) -- List with element identifiers

        Return:
        elements (Elements) -- Object of type Elements
        """
        elementIndex = self.elements.findIndexByElementIds(ids)
        
        return Elements(self.elements.nodeIds[elementIndex],self.elements.integrationpointIds[elementIndex],self.elements.thickness[elementIndex],
                        self.elements.youngsModulus[elementIndex],self.elements.poissonsRatio[elementIndex],self.elements.ids[elementIndex])

    def getNodesOfElementId(self,id):
        """
        Find and return a Node object with just the nodes that belong to a specific element.

        Parameters:
        id (int)-- Single element identifier

        Return:
        nodes (Nodes) -- Object of type Nodes
        """

        # Find node ids of specific element by using element method
        nodeIds, index = self.elements.findNodeIdsByElementId(id)
        
        # Find position of node ids in model Nodes object
        nodeCoordinates, nodeIndex = self.nodes.findCoordinatesByNodeIds(nodeIds)

        #  create new Nodes object with specific nodes from model
        nodesFound = Nodes(nodeCoordinates,self.nodes.ids[nodeIndex])
 
        return nodesFound

    def setIntegrationPoints(self, integrationPoints):
        """
        Set the IntegrationPoints object for the model.

        Parameters:
        integrationPoints (IntegrationPoints) -- Object of type IntegrationPoints
        """
        if isinstance(integrationPoints, IntegrationPoints):
            self.integrationPoints = integrationPoints
        else:
            raise TypeError("Object is not of type IntegrationPoints!")

    def getIntegrationPoints(self):
        """
        Get the IntegrationPoints object of the model.

        Returns:
        integrationPoints (IntegrationPoints) -- Object of type IntegrationPoints
        """
        return self.integrationPoints

    def plotMesh(self,color_test = False,show_ids = False):
        """
        Plots the mesh

        Parameters:
        color_test (bool) -- ???
        show_ids (bool) -- True displays node identifiers
        """
        
        for elementIndex,elementNodeIds in enumerate(self.elements.nodeIds):
            elementNodeIds =np.array(elementNodeIds)
           # If elementtype is TRIA6: use defined order to get correct nodes
            if len(elementNodeIds) == 6:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds[[0,3,1,4,2,5]])
            # If elementtype is Quad8: use defined order to get correct nodes
            elif len(elementNodeIds) == 8:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds[[0,4,1,5,2,6,3,7]])
            else:
                elementNodeIndex = self.nodes.findIndexByNodeIds(elementNodeIds)

            coords = self.nodes.coordinates[elementNodeIndex]
            
            midpoint = np.mean(coords,axis=0)
            if color_test == False:
                color = 'none'
            else:
                cmap = plt.get_cmap('jet')
                color = cmap(elementIndex/self.elements.ids.shape[0])
                
            plt.fill(coords[:,0],coords[:,1], edgecolor='cyan', facecolor=color)
            
            if show_ids == True:
                plt.text(midpoint[0],midpoint[1], self.elements.ids[elementIndex], fontsize=12,color='cyan',ha='center',va='center')

            plt.axis('square')

    def printParameters(self):
        """
        Display the parameters of the Mesh class in a structured manner.
        """
        print("-----------------------------\n\t NODES\n-----------------------------")
        self.nodes.printParameters()
        print("-----------------------------\n\t ELEMENTS\n-----------------------------")
        self.elements.printParameters()


# --- Geometry ---
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

class Lines():
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

class Geometry():
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
        self.lines  = lines

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
        self.points = Points(coordinates, ids=np.arange(1,len(coordinates)+1))
        n = self.points.coordinates.shape[0]
        
        # Create lines connecting the points counterclockwise, for all vertices
        lineIds = np.ones([n,2])
        lineIds[:,0] = np.arange(1,n+1)
        lineIds[0:-1:,1] = np.arange(2,n+1)
        self.lines = Lines(pointIds=lineIds)
        pass
    
    def plot(self):
        """
        Plots all Points and Lines defined in the model
        """
        self.points.plot()
        for label_id,ids in enumerate(self.lines.pointIds):
            #coords=self.points.coordinates[ids]
            coords = self.points.findCoordinatesByNodeIds(ids)[0]
            x = coords[:, 0]
            y = coords[:, 1]
            plt.plot(x,y,color='c')
            plt.text(np.mean(x), np.mean(y),self.lines.ids[label_id], fontsize=12, ha='right',color='c')
        plt.axis('square')
    
    def printParameters(self):
        """
        Display the parameters of the Geometry class in a structured manner.
        """
        print("-----------------------------\n\t POINTS\n-----------------------------")
        self.points.printParameters()
        print("-----------------------------\n\t LINES\n-----------------------------")
        self.lines.printParameters()

# --- Boundary Conditions ---
class DisplacementOnNodes(_DisplacementBaseClass):
    def __init__(self, displacements=[[]], nodeIds=[], ids=[]):
        """
        Initialize a DisplacementOnNodes object with specific attributes.

        Parameters:
        displacement (list of lists) -- List of displacement constraints in x and y directions ("0" for fixed, "1" for free)
        nodeIds (list) -- List of node ids to apply constraint
        ids (list) -- List of identifiers
        """
        super().__init__("displacement on node",displacements, ids)
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
        for index, id  in enumerate(self.nodeIds):
            if self.x[index] == 0:
                xFixationNodeId.append(id)
        return(np.array(xFixationNodeId))
    
    def _getNodeIdsWithFixationY(self):
        """
        Returns the node Ids for which the displacements in y directions is zero.
        """
        yFixationNodeId = []
        for index, id in enumerate(self.nodeIds):
            if self.y[index] == 0:
                yFixationNodeId.append(id)
        return(np.array(yFixationNodeId))

    def _getPrescribedNodalDispalcementX(self):
        """
        Returns the prescriped nodal displacement and Ids for which the displacements in x directions is not or free zero.
        """
        xDispNodeId = []
        xDisp = []
        for index, id  in enumerate(self.nodeIds):
            if not (self.x[index] in [0,"free",None]):
                xDispNodeId.append(id)
                xDisp.append(float(self.x[index]))
        return np.array(xDisp), np.array(xDispNodeId)

    def _getPrescribedNodalDispalcementY(self):
        """
        Returns the prescriped nodal displacement and Ids for which the displacements in y directions is not or free zero.
        """
        yDispNodeId = []
        yDisp = []
        for index, id  in enumerate(self.nodeIds):
            if not (self.y[index] in [0,"free",None]):
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
    def __init__(self, displacements=[], pointIds =[], ids=[]):
        """
        Initialize a DisplacementOnPoints object with specific attributes.

        Parameters:
        displacement (list of lists) -- List of displacement constraints in x and y directions ("0" for fixed, "1" for free)
        pointIds (list) -- List of point ids to apply constraint
        ids (list) -- List of identifiers
        """
        super().__init__("displacement on point", displacements, ids)
        self.pointIds  = np.array(pointIds)
    
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
        super().__init__("displacement on line",displacements, ids)
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

class Boundaries():
    """
    Boundaries class. Contains the different types of boundary conditions defined in the model
    """    
    def __init__(self, displacementOnNodes=DisplacementOnNodes(), displacementOnPoints=DisplacementOnPoints(), displacementOnLines=DisplacementOnLines()):
        """
        Initialize a Mesh class

        Parameters:
        nodes (object) -- Object of type Nodes
        elements (object) -- Object of type Elements
        """        
        self.displacementOnNodes   = displacementOnNodes
        self.displacementOnPoints  = displacementOnPoints
        self.displacementOnLines   = displacementOnLines  

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

# --- Loads ----
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
            print(self.loads[:5,:], "...")
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
            print(self.loads[:5,:], "...")
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
            print(self.loads[:5,:], "...")
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

class Loads():
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
        self.loadsOnNodes   = loadsOnNodes
        self.loadsOnPoints  = loadsOnPoints
        self.loadsOnLines   = loadsOnLines

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

# --- Solver Data ---
class _ShapeFunctions():
    def __init__(self):
        """
        Contains pre defined shape function matrices
        """
        self._matrixTRIA3 = np.array([[1, 0, 0],
                                      [-1, 1, 0],
                                      [-1, 0, 1]])

        self._matrixTRIA6 = np.array([[1,0,0,0,0,0],
                                     [-3,-1,0,4,0,0],
                                     [-3,0,-1,0,0,4],
                                     [4,0,0,-4,4,-4],
                                     [2,2,0,-4,0,0],
                                     [2,0,2,0,0,-4]])

        self._matrixQUAD4 = np.array([[1, 1, 1, 1],
                                      [-1, 1, 1, -1],
                                      [-1, -1, 1, 1],
                                      [1, -1, 1, -1]]) / 4

        self._matrixQUAD8 = np.array([[-1, -1, -1, -1, 2, 2, 2, 2],
                                      [0, 0, 0, 0, 0, 2, 0, -2],
                                      [0, 0, 0, 0, -2, 0, 2, 0],
                                      [1, -1, 1, -1, 0, 0, 0, 0],
                                      [1, 1, 1, 1, -2, 0, -2, 0],
                                      [1, 1, 1, 1, 0, -2, 0, -2],
                                      [-1, -1, 1, 1, 2, 0, -2, 0],
                                      [-1, 1, 1, -1, 0, -2, 0, 2]]) / 4
        
        self._lineLoadLinear = [1/2, 1/2]
        self._lineLoadQuadtratic = [1/6, 1/6, 4/6]

    def _getShapeFunctionCoefficients(self, xi=0.0, eta=0.0, eType=0):
        """
        Get the shape functions result for a specific coordinate [xi,eta] as an array [N1,N2,N3,N4,...]
        eType in ["TRIA3" = 3, "QUAD4" = 4, "TRIA6" = 6, "QUAD8" = 8]
        """
        if eType in ["TRIA3", 3]:
            N = np.array([1, xi, eta]) @ self._matrixTRIA3
        elif eType in ["TRIA6", 6]:
            N = np.array([1, xi, eta, xi * eta, xi**2, eta**2]) @ self._matrixTRIA6
        elif eType in ["QUAD4", 4]:
            N = np.array([1, xi, eta, xi * eta]) @ self._matrixQUAD4
        elif eType in ["QUAD8", 8]:
            N = np.array([1, xi, eta, xi * eta, xi**2, eta**2, xi**2 * eta, xi * eta**2]) @ self._matrixQUAD8
        else:
            raise Exception(f"Element type {eType} not implemented")
        return N

    def _getShapeFunctionDerivateCoefficients(self, xi=0.0, eta=0.0, eType=0):
        """
        Get the partial derivates of the shape functions in respect to xi and eta at a specific coordinate
        eType in ["TRIA3" = 3, "QUAD4" = 4, "TRIA6" = 6, "QUAD8" = 8]
        """
        if eType in ["TRIA3", 3]:
            dNdXi = np.array([0, 1, 0]) @ self._matrixTRIA3
            dNdEta = np.array([0, 0, 1]) @ self._matrixTRIA3
        elif eType in ["TRIA6", 6]:
            dNdXi = np.array([0, 1, 0, eta, 2*xi, 0]) @ self._matrixTRIA6
            dNdEta = np.array([0, 0, 1, xi, 0, 2*eta]) @ self._matrixTRIA6
        elif eType in ["QUAD4", 4]:
            dNdXi = np.array([0, 1, 0, eta]) @ self._matrixQUAD4
            dNdEta = np.array([0, 0, 1, xi]) @ self._matrixQUAD4
        elif eType in ["QUAD8", 8]:
            dNdXi = np.array([0, 1, 0, eta, 2*xi, 0, 2*xi*eta, eta**2]) @ self._matrixQUAD8
            dNdEta = np.array([0, 0, 1, xi, 0, 2*eta, xi**2, xi*eta*2]) @ self._matrixQUAD8
        else:
            raise Exception(f"Element type {eType} not implemented")
        return dNdXi, dNdEta

    def _getLineLoadCoefficients(self, eType=0):
        """
        Get the line load coefficients in the order of the element nodeIds.
        eType in ["TRIA3" = 3, "QUAD4" = 4, "TRIA6" = 6, "QUAD8" = 8]
        """
        if eType in ["TRIA3", 3, "QUAD4", 4]:
            return self._lineLoadLinear    
        elif eType in ["TRIA6", 6, "QUAD8", 8]:
            return self._lineLoadQuadtratic
        else:
            raise Exception(f"Element type {eType} not implemented")

class _GaussPoints():
    def __init__(self):
        """
        Pre defined integration points and weights
        """
        
        # Integration wheights
        self._triaWeightsOrder1 = np.array([0.5])
        self._triaWeightsOrder3 = np.array([1/6, 1/6, 1/6])
        self._triaWeightsOrder4 = np.array([-9/32, 25/96, 25/96, 25/96])
        self._triaWeightsOrder7 = np.array([1/40, 1/15, 1/40, 1/15, 1/40, 1/15, 9/40])
        
        self._quadWeightsOrder1 = np.array([4])
        self._quadWeightsOrder4 = np.array([1, 1, 1, 1])
        self._quadWeightsOrder9 = np.array([25/81, 40/81, 25/81, 
                                           40/81, 64/81, 40/81,
                                           25/81, 40/81, 25/81])


        # Integration point coordinates
        self._triaPointOrder1 = np.array([[1/3, 1/3]])
        self._triaPointOrder3 = np.array([[1/6, 1/6],
                                         [2/3, 1/6],
                                         [1/6, 2/3]])
        self._triaPointOrder4 = np.array([[1/3, 1/3],
                                         [3/5, 1/5],
                                         [1/5, 3/5],
                                         [1/5, 1/5]])
        self._triaPointOrder7 = np.array([[0, 0],
                                         [1/2, 0],
                                         [1, 0],
                                         [1/2, 1/2],
                                         [0, 1],
                                         [0, 1/2],
                                         [1/3, 1/3]])    
        
        self._quadPointOrder1 = np.array([[0, 0]])
        self._quadPointOrder4 = np.array([[-1/math.sqrt(3) , -1/math.sqrt(3)],
                                         [1/math.sqrt(3) , -1/math.sqrt(3)],
                                         [1/math.sqrt(3) , 1/math.sqrt(3)],
                                         [-1/math.sqrt(3) , 1/math.sqrt(3)]])
        self._quadPointOrder9 = np.array([[-math.sqrt(0.6) , -math.sqrt(0.6)],
                                         [0               , -math.sqrt(0.6)],
                                         [math.sqrt(0.6)  , -math.sqrt(0.6)],
                                         [-math.sqrt(0.6) , 0],
                                         [0               , 0],
                                         [math.sqrt(0.6)  , 0],
                                         [-math.sqrt(0.6) , math.sqrt(0.6)],
                                         [0               , math.sqrt(0.6)],
                                         [math.sqrt(0.6)  , math.sqrt(0.6)]])
        
    def _getTriaGaussPoint(self, order=0):
        """
        Return the 1D gauss points in regards to a 1D integration order
        """
        if order == 1:
            return self._triaPointOrder1
        elif order == 3:
            return self._triaPointOrder3
        elif order == 4:
            return self._triaPointOrder4
        elif order == 7:
            return self._triaPointOrder7
        else:
            raise Exception(f"Integration Order {order} not implemented!")

    def _getQuadGaussPoint(self, order=0):
        """
        Return the 1D gauss points in regards to a 1D integration order
        """
        if order == 1:
            return self._quadPointOrder1
        elif order == 4:
            return self._quadPointOrder4
        elif order == 9:
            return self._quadPointOrder9
        else:
            raise Exception(f"Integration Order {order} not implemented!")

    def _getTriaGaussWeights(self, order=0):
        """
        Return the 2D integration weights in regards to a 1D integration order
        """
        if order == 1:
            return self._triaWeightsOrder1
        elif order == 3:
            return self._triaWeightsOrder3
        elif order == 4:
            return self._triaWeightsOrder4
        elif order == 7:
            return self._triaWeightsOrder7
        else:
            raise Exception(f"Integration Order {order} not implemented!")

    def _getQuadGaussWeights(self, order=0):
        """
        Return the 2D integration weights in regards to a 1D integration order
        """
        if order == 1:
            return self._quadWeightsOrder1
        elif order == 4:
            return self._quadWeightsOrder4
        elif order == 9:
            return self._quadWeightsOrder9
        else:
            raise Exception(f"Integration Order {order} not implemented!")

class SolverData(_GaussPoints, _ShapeFunctions):

    def __init__(self, mesh=Mesh(), meshDeformed=Mesh()):
        """
        Contains all the data that is generated during the solving process
        """
        _GaussPoints.__init__(self)
        _ShapeFunctions.__init__(self)

        self.status             = "unfinished"
        self.elapsedTime        = None

        self.mesh               = mesh # original mesh
        self.meshDeformed       = meshDeformed # deformed mesh

        self.numberDOF          = 0 # number of DOFs (fixed DOFs are not included)
        self.fixedDOF           = [] # DOFs (refers to column index in the stiffness matrix) that are fixed
        self.openDOF            = [] # DOFs (refers to column index in the stiffness matrix) that are free

        self.nodalLoads         = Loads().loadsOnNodes # all loads compremised to only nodal loads object
        self.nodalDisplacements = Boundaries().displacementOnNodes # all loads compremised to only nodal displacements objcect

        self.stiffnessMatrix    = [] # global stiffness matrix
        self.displacementVector = [] # displacement vector
        self.loadVector         = [] # load vector

        self.reducedStiffnessMatrix     = [] # reduced  global stiffness matrix
        self.reducedDisplacementVector  = [] # reduced  displacement vector
        self.reducedLoadVector          = [] # reduced  load vector

    def _getIntegrationPointsCoordinates(self,nodeCoords=np.empty([1, 2]), xi=0.0, eta=0.0):
        """
        Return the global coordinates ot the integration points based on the element nodes
        """
        nodeCoords = np.array(nodeCoords)
        N = self._getShapeFunctionCoefficients(xi, eta, nodeCoords.shape[0])
        coords = N@nodeCoords # [x,y] coordinates

        return coords
    
    def _getElementDMatrix(self, E=0.0, nu=0.0, behaviour=""):
        """
        Returns the material behaviour as a matrix (D Matrix)
        """
        if behaviour.lower() in [0, "plane stress","planestress","stress"]:
            D = E / (1 - nu**2) * np.array([[1, nu, 0],
                                            [nu, 1, 0],
                                            [0, 0, (1 - nu) / 2]])
        elif behaviour.lower() in [1, "plane strain","planestrain","strain"]:
            D = E / ((1 + nu) * (1 - 2 * nu)) * np.array([[1 - nu, nu, 0],
                                                          [nu, 1 - nu, 0],
                                                          [0, 0, 1 / 2 - nu]])
        else:
            raise Exception(f"Behaviour type {behaviour} not defined! (0 for plane stress, 1 for plane strain)")
        return D

    def _getElementBMatrixandJacobiDeterminant(self, nodeCoords=np.empty([1, 2]), xi=0.0, eta=0.0):
        """
        Returns the B Matrix and the jacobi determinant
        """
        # Use derivates to calculate jacobi matrix
        dNdXi, dNdEta = self._getShapeFunctionDerivateCoefficients(xi, eta, nodeCoords.shape[0])

        dXdXi   = dNdXi @ nodeCoords[:, 0]
        dXdEta  = dNdEta @ nodeCoords[:, 0]
        dYdXi   = dNdXi @ nodeCoords[:, 1]
        dYdEta  = dNdEta @ nodeCoords[:, 1]

        J = np.array([[dXdXi, dXdEta],
                      [dYdXi, dYdEta]])
        
        J_inv = np.linalg.inv(J)

        # B1 Matrix
        B1 = np.array([[1, 0, 0, 0],
                       [0, 0, 0, 1],
                       [0, 1, 1, 0]])

        # B2 matrix
        B2 = np.zeros((4, 4))
        B2[0:2, 0:2] = np.transpose(J_inv)
        B2[2:4, 2:4] = np.transpose(J_inv)

        # B3 matrix
        B3 = np.zeros((4, 2 * nodeCoords.shape[0]))
        B3[0:2, 0::2] = np.vstack((dNdXi, dNdEta))
        B3[2:4, 1::2] = np.vstack((dNdXi, dNdEta))

        # B matrix is the product of B1, B2 and B3
        B = B1 @ B2 @ B3

        return B,np.linalg.det(J)

    def _getElementKMatrix(self, nodeCoords=np.empty([1, 2]), order=0, E=.0, nu=.0, t=.0, behaviour=""):
        """
        Return the stiffness matrix for a single element
        """
        nodeSize = nodeCoords.shape[0]
        ke = np.zeros((2*nodeSize, 2*nodeSize)) # pre allocate element stiffness matrix
        
        D = self._getElementDMatrix(E,nu,behaviour) # get element D matrix
        
        if nodeSize in [3,6]: # triangle
            gaussPoints = self._getTriaGaussPoint(order) 
            gaussWeights = self._getTriaGaussWeights(order)
        elif nodeSize in [4,8]: # quad
            gaussPoints = self._getQuadGaussPoint(order) 
            gaussWeights = self._getQuadGaussWeights(order)

        # iterate trough all integration points and sum up matrices
        for index, [xi,eta] in enumerate(gaussPoints):
            B, detJ = self._getElementBMatrixandJacobiDeterminant(nodeCoords,xi,eta)
            ke = ke + gaussWeights[index]*np.transpose(B)@D@B*detJ

        return ke*t

    def _getMatrixGuideVector(self, nodeIndex=np.empty([1, 1])):
        """
        Return a guide vector that contains the position of a DOF in the global stiffness matrix based on the node index
        """
        nodeSize = len(nodeIndex)  # Number of nodes
        g = np.zeros(2 * nodeSize, dtype=int)  # Preallocate guide vector

        for i in range(nodeSize):
            g[2*i] = 2*nodeIndex[i]  # x direction (even numbers)
            g[2*i + 1] = 2*nodeIndex[i]+1  # y direction (odd numbers)
        return g

    def _findNearestNeighbour(self, coordinates, refCoordinates):
            """
            Find the index of the nearest neighbor for each point in refCoordinates from the coordinates array.

            Parameters:
            coordinates : numpy array
                An Nx2 array of coordinates (x, y) to find nearest neighbors from.
            refCoordinates : numpy array
                An Mx2 array of reference coordinates (x, y).

            Returns:
            nearest_indices : numpy array
                An array of indices in the coordinates array corresponding to the nearest neighbors for each reference point.
            """
            nearest_indices = []
            
            for ref in refCoordinates:
                # Calculate squared distances to avoid unnecessary sqrt computation
                squared_distances = np.sum((coordinates - ref) ** 2, axis=1)
                nearest_index = np.argmin(squared_distances)  # Get the index of the minimum distance
                nearest_indices.append(nearest_index)

            return np.array(nearest_indices)

    def _findNodesBetweenTwoPoints(self, nodeCoords, pointCoords, tolerance=1E-15):
        """
        Find all nodes that lie on a line segment between two points within a given tolerance.

        Parameters:
        nodeCoords : numpy array
            An Nx2 array of node coordinates (x, y).
        pointCoords : numpy array
            A 2x2 array of coordinates defining the endpoints of the line (start, end).
        tolerance : float
            The maximum allowable distance from the line for a node to be considered "on" the line segment.

        Returns:
        numpy array
            An array of indices of nodes that lie on the line segment between the two points within the tolerance.
        """
        
        # Extract the start and end points
        start = pointCoords[0]
        end = pointCoords[1]
        
        # Calculate the direction vector of the line
        line_vector = end - start
        line_length = np.linalg.norm(line_vector)
        
        # Normalize the line vector
        if line_length == 0:
            return np.array([])  # No valid line if start and end are the same
        line_unit_vector = line_vector / line_length
        
        # Create an array to hold the indices of nodes that are close to the line segment
        node_indices = []
        
        # Iterate through all node coordinates
        for index, node in enumerate(nodeCoords):
            # Create a vector from the start point to the node
            point_vector = node - start
            
            # Project point_vector onto the line_unit_vector
            projection_length = np.dot(point_vector, line_unit_vector)
            
            # Find the projected point on the line
            projected_point = start + projection_length * line_unit_vector
            
            # Calculate the distance from the node to the projected point
            distance = np.linalg.norm(node - projected_point)

            # Check if the distance is within the specified tolerance
            if distance <= tolerance:
                # Check if the projected point is between the start and end points
                if (min(start[0], end[0]) <= projected_point[0] <= max(start[0], end[0]) and
                    min(start[1], end[1]) <= projected_point[1] <= max(start[1], end[1])):
                    node_indices.append(index)
        
        return np.array(node_indices)

    def _resolveDuplicateDisplacements(self):
        """
        Resolve cases where the same node has multiple displacements defined
        by applying rules for x and y displacement priorities.
        """
        nodeIds = self.nodalDisplacements.nodeIds
        displacements = self.nodalDisplacements.displacements

        uniqueNodeIds, counts = np.unique(nodeIds, return_counts=True)

        # Check for nodes that appear more than once
        duplicateNodes = uniqueNodeIds[counts > 1]

        if len(duplicateNodes) > 0:
            print(f"Warning: Multiple displacements defined for the same nodes: {duplicateNodes}")

        for nodeId in duplicateNodes:
            # Find all occurrences of the node
            indices = np.where(nodeIds == nodeId)[0]

            # Get all displacements for this node
            x_displacements = displacements[indices, 0]
            y_displacements = displacements[indices, 1]

            # Rule for X displacements: If at least one is 0, set all to 0
            if 0 in x_displacements:
                x_resolved = 0
            else:
                # If no zero, choose the first non-"free" value, else keep "free"
                non_zero_x = [x for x in x_displacements if x != "free"]
                x_resolved = non_zero_x[0] if non_zero_x else "free"

            # Rule for Y displacements: If at least one is 0, set all to 0
            if 0 in y_displacements:
                y_resolved = 0
            else:
                # If no zero, choose the first non-"free" value, else keep "free"
                non_zero_y = [y for y in y_displacements if y != "free"]
                y_resolved = non_zero_y[0] if non_zero_y else "free"

            # Set the resolved displacement to the first occurrence and remove others
            displacements[indices[0], :] = [x_resolved, y_resolved]
            displacements = np.delete(displacements, indices[1:], axis=0)
            nodeIds = np.delete(nodeIds, indices[1:])
            self.nodalDisplacements.ids = np.delete(self.nodalDisplacements.ids, indices[1:])

        # Update nodalDisplacements with the resolved values
        self.nodalDisplacements.displacements = displacements
        self.nodalDisplacements.nodeIds = nodeIds

    def _resolveDuplicateLoads(self):
        """
        Resolve cases where the same node has multiple loads defined by summing them up.
        """
        loadIds = self.nodalLoads.ids
        nodeIds = self.nodalLoads.nodeIds
        loads = self.nodalLoads.loads

        # Create dictionaries to hold the summed loads for each nodeId
        node_load_dict = {}
        
        # Traverse through all nodeIds and sum up their respective loads
        for i in range(len(nodeIds)):
            node_id = nodeIds[i]
            load = loads[i]
            load_id = loadIds[i]
            
            if node_id in node_load_dict:
                # Sum up loads for the same nodeId
                node_load_dict[node_id]["load"] += load
            else:
                # Initialize entry for the nodeId
                node_load_dict[node_id] = {
                    "load": load,
                    "loadId": load_id
                }

        # After resolving duplicates, update nodalLoads arrays
        new_node_ids = []
        new_loads = []
        new_load_ids = []

        # Build the new lists from the dictionary
        for node_id, data in node_load_dict.items():
            new_node_ids.append(node_id)
            new_loads.append(data["load"])
            new_load_ids.append(data["loadId"])

        # Update the arrays in nodalLoads
        self.nodalLoads.nodeIds = np.array(new_node_ids)
        self.nodalLoads.loads = np.array(new_loads)
        self.nodalLoads.ids = np.array(new_load_ids)

    def _combineBoundaries(self, geometry=Geometry(), boundaries=Boundaries()):
        """
        Combine all the boundaries defined in the model to only nodal displacements
        """

        # make a deep copy of displacement on Nodes
        self.nodalDisplacements = copy.deepcopy(boundaries.displacementOnNodes)

        # get node coordinates
        nodeCoords  = self.mesh.nodes.coordinates
        nodeIds     = self.mesh.nodes.ids
        
        # transfer boundaries on geometrical points to nodes
        if not (boundaries.displacementOnPoints.pointIds.shape[0] == 0 or len(boundaries.displacementOnPoints.displacements) == 0):
            pointIds                = boundaries.displacementOnPoints.pointIds
            pointDisp               = boundaries.displacementOnPoints.displacements
            pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
            nodeIndices              = self._findNearestNeighbour(nodeCoords,pointCoords)
            for pointIndex,nodeIndex in enumerate(nodeIndices):
                self.nodalDisplacements.add(pointDisp[pointIndex],nodeIds[nodeIndex])

        # transfer boundaries on geometrical lines to nodes
        if not (boundaries.displacementOnLines.lineIds.shape[0] == 0 or len(boundaries.displacementOnLines.displacements) == 0):
            # iterate trough all line displacements and get nodes that lie on the current line
            for lineDispIndex,lineId in enumerate(boundaries.displacementOnLines.lineIds):
                lineDisp                = boundaries.displacementOnLines.displacements[lineDispIndex] # displacement amplitude
                lineIndex               = geometry.lines._findIndexByLineIds(lineId) # line index
                pointIds                = geometry.lines.pointIds[lineIndex][0]
                pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
                nodeIndices               = self._findNodesBetweenTwoPoints(nodeCoords,pointCoords)
                if nodeIndices.size != 0:
                    for nodeIndex in nodeIndices:
                        self.nodalDisplacements.add(lineDisp,nodeIds[nodeIndex])
                else:
                    print(f"No nodes were found on line {lineId}!")

        # Resolve conflicts for nodes with multiple displacements
        self._resolveDuplicateDisplacements()

    def _combineLoads(self,geometry=Geometry(), loads = Loads()):
        """
        Combine all the loads defined in the model to only nodal displacements
        """
        # make a deep copy of loads on Nodes
        self.nodalLoads = copy.deepcopy(loads.loadsOnNodes)

        # get node coordinates
        nodeCoords  = self.mesh.nodes.coordinates
        nodeIds     = self.mesh.nodes.ids
        
        # transfer loads on geometrical points to nodes
        if not (loads.loadsOnPoints.pointIds.shape[0] == 0 or loads.loadsOnPoints.loads.shape[0] == 0):
            pointIds                = loads.loadsOnPoints.pointIds
            pointLoads              = loads.loadsOnPoints.loads
            pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
            nodeIndices             = self._findNearestNeighbour(nodeCoords,pointCoords)
            for pointIndex,nodeIndex in enumerate(nodeIndices):
                self.nodalLoads.add(pointLoads[pointIndex],nodeIds[nodeIndex])

        # transfer loads on geometrical lines to nodes
        if not (loads.loadsOnLines.lineIds.shape[0] == 0 or loads.loadsOnLines.loads.shape[0] == 0):

            # iterate trough all line loads and get nodes that lie on the current line
            for lineLoadIndex,lineId in enumerate(loads.loadsOnLines.lineIds):
                lineLoad                = loads.loadsOnLines.loads[lineLoadIndex] # load amplitude
                lineIndex               = geometry.lines._findIndexByLineIds(lineId) # line index
                pointIds                = geometry.lines.pointIds[lineIndex][0] # vertices of line
                pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds) # coordinates of line vertices
                nodesOnLineIndex        = self._findNodesBetweenTwoPoints(nodeCoords,pointCoords) # nodes between vertices
                if nodesOnLineIndex.size != 0: 
                    nodesOnLineIds           = self.mesh.nodes.ids[nodesOnLineIndex]
                    # iterate through all elements in mesh
                    for elementIndex,elementId in enumerate(self.mesh.elements.ids):

                        # find node properties of current element
                        elementNodeIds  = self.mesh.elements.nodeIds[elementIndex]
                        elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(elementNodeIds)

                        # find all nodes of the current element that are on the current line
                        elementNodeIndexOnLine = [nodeIndex for nodeIndex in elementNodeIndex if nodeIndex in nodesOnLineIndex] 
                        elementNodeIdsOnLine = self.mesh.nodes.ids[elementNodeIndexOnLine]
                        elementCoordsOnLine = self.mesh.nodes.coordinates[elementNodeIndexOnLine]

                        # get element edge length (based on the numbering convention element vertices must follow each other)
                        if len(elementNodeIndexOnLine)>1:
                            edgeLength = math.sqrt((elementCoordsOnLine[1,0]-elementCoordsOnLine[0,0])**2 + 
                                                    (elementCoordsOnLine[1,1]-elementCoordsOnLine[0,1])**2)
                            
                            # check if definitions are wrong
                            if len(elementNodeIds) in [3,4]: # linear shape function
                                if len(elementNodeIndexOnLine)!=2:
                                    raise ValueError(f"Linear element {elementId} appears to have more than two nodes on line {lineId}!")
                                    
                            elif len(elementNodeIds) in [6,8,9]: # quadratic shape function
                                if len(elementNodeIndexOnLine)==2:
                                    raise ValueError(f"Load on line {lineId} appears to not end on quadratic element {elementId} vertices!")
                                elif len(elementNodeIndexOnLine)!=3:
                                    raise ValueError(f"Quadratic element {elementId} appears to have more than three nodes on line {lineId}!")
                
                            # get line coefficients and add nodal force for each node
                            loadCoefficients = self._getLineLoadCoefficients(len(elementNodeIds))
                            for index, coeff in enumerate(loadCoefficients):
                                # this loop relies on the numbering convention -> vertix nodes allways come first in list
                                self.nodalLoads.add([coeff*edgeLength*lineLoad[0],coeff*edgeLength*lineLoad[1]],elementNodeIdsOnLine[index])
                else:
                    print(f"No nodes were found on line {lineId}!")

        # Resolve conflicts for nodes with multiple displacements
        self._resolveDuplicateLoads()
        
    def _buildStiffnessMatrix(self):
        """
        Assemble the global stiffness matrix based on the model mesh
        """

        # pre-allocation based on the DOFs
        self.stiffnessMatrix = np.zeros([2*self.mesh.numberOfNodes,2*self.mesh.numberOfNodes])

        # iterate trough all elements in the mesh and insert element stiffness matrix
        for elementIndex,id in enumerate(self.mesh.elements.ids):
            nodeIds         = self.mesh.elements.nodeIds[elementIndex]
            nodeCoords, nodeIndex = self.mesh.nodes.findCoordinatesByNodeIds(nodeIds)
            order           = self.mesh.elements.integrationOrder[elementIndex]
            E               = self.mesh.elements.youngsModulus[elementIndex]
            nu              = self.mesh.elements.poissonsRatio[elementIndex]
            t               = self.mesh.elements.thickness[elementIndex]
            behaviour       = self.mesh.elements.planarAssumption[elementIndex]
            
            # element stiffness
            ke = self._getElementKMatrix(nodeCoords,order,E,nu,t,behaviour)

            # insert element stiffness using the guide vectors
            g = self._getMatrixGuideVector(nodeIndex)
            self.stiffnessMatrix[np.ix_(g, g)] = self.stiffnessMatrix[np.ix_(g, g)] + ke

    def _buildLoadVector(self):
        """
        Build load vector
        """

        # pre-allocation of load vector
        self.loadVector = np.zeros([2*self.mesh.numberOfNodes,1])

        # get DOF index in the global load vector for each node with a load
        index = np.array(self.mesh.nodes.findIndexByNodeIds(self.nodalLoads.nodeIds))

        # align x and y direction into a single vector
        loads = self.nodalLoads.loads.flatten()  

        # insert loads at the right position of the load vector
        g = self._getMatrixGuideVector(index)
        self.loadVector[g,0] = loads 

    def _applyPrescribedDisplacements(self):
        """
        Consider prescribed nodal displacements by adjusting stiffness matrix and load vector
        """

        # Get node index for prescribed displacements other than 0
        xDisp, xDispNodeId  = self.nodalDisplacements._getPrescribedNodalDispalcementX()
        xDispNodeIndex      = self.mesh.nodes.findIndexByNodeIds(xDispNodeId)
        yDisp, yDispNodeId  = self.nodalDisplacements._getPrescribedNodalDispalcementY()
        yDispNodeIndex      = self.mesh.nodes.findIndexByNodeIds(yDispNodeId)

        # create line with all zeros for adjusting the stiffness matrix
        zeroLine = np.zeros(self.stiffnessMatrix.shape[1])

        # consider x dislacements
        for dispIndex,nodeIndex in enumerate(xDispNodeIndex):
            self.stiffnessMatrix[nodeIndex*2,:] = zeroLine
            self.stiffnessMatrix[nodeIndex*2,nodeIndex*2] = 1
            self.loadVector[nodeIndex*2] = xDisp[dispIndex]

        # consider y dislacements
        for dispIndex,nodeIndex in enumerate(yDispNodeIndex):
            self.stiffnessMatrix[nodeIndex*2+1,:] = zeroLine
            self.stiffnessMatrix[nodeIndex*2+1,nodeIndex*2+1] = 1
            self.loadVector[nodeIndex*2+1] = yDisp[dispIndex]

    def _reduceStiffnesMatrixAndLoadVector(self):
        """
        Reduces sitffness matrix and load vector based on fixated nodes
        """

        # Get index of nodes that are fixated
        xFixationNodeId     = self.nodalDisplacements._getNodeIdsWithFixationX() # fixated nodes in x
        xFixationNodeIndex  = self.mesh.nodes.findIndexByNodeIds(xFixationNodeId)
        yFixationNodeId     = self.nodalDisplacements._getNodeIdsWithFixationY() # fixated nodes in y
        yFixationNodeIndex  = self.mesh.nodes.findIndexByNodeIds(yFixationNodeId)

        # get number of degrees of freedom
        self.numberDOF = self.stiffnessMatrix.shape[0]-(xFixationNodeId.size + yFixationNodeId.size)

        # align reducable columns and rows in new list
        for index in xFixationNodeIndex:
            self.fixedDOF.append(index*2)  # x-Direction
        for index in yFixationNodeIndex:
            self.fixedDOF.append(index*2+1)  # y-Direction

        # Find the free DOF (those that are not fixed)
        self.openDOF = np.setdiff1d(np.arange(self.stiffnessMatrix.shape[0]), self.fixedDOF)

        # Create reduced stiffness matrix by deleting rows and columns
        self.reducedStiffnessMatrix = np.delete(self.stiffnessMatrix, self.fixedDOF, axis=0)
        self.reducedStiffnessMatrix  = np.delete(self.reducedStiffnessMatrix , self.fixedDOF, axis=1)
        self.reducedLoadVector = np.delete(self.loadVector,self.fixedDOF,axis=0)

    def _solveLinearEquation(self):
        """
        Solves the linear FEM equation K*U=F by using inverse of K 
        """
        start_time = time.perf_counter()

#        if np.linalg.det(self.reducedStiffnessMatrix) <1E-300:
#            raise ValueError("Global stiffness matrix appears to be close to singluar!\n"
#                             "Check for faulty boundries, integration orders, unconnected nodes!")
                             
        # solve the fem  equation
        self.reducedDisplacementVector = np.linalg.inv(self.reducedStiffnessMatrix)@self.reducedLoadVector
    
        # transfer the reduced displacement vector to the comlete displacement vector
        self.displacementVector = np.zeros([self.stiffnessMatrix.shape[0],1])
        self.displacementVector[self.openDOF, 0] = self.reducedDisplacementVector.flatten()

    def _getNodalSolution(self):
        """
        Return nodal solution and update deformed mesh
        """
        # Nodal displacements
        dispX       = self.displacementVector[0::2]
        dispY       = self.displacementVector[1::2]
        dispTotal   = np.sqrt(dispX**2 + dispY**2) 

        # Deformed mesh coordinates
        self.meshDeformed.nodes.coordinates = self.mesh.nodes.coordinates + np.hstack([dispX,dispY])

        return dispX, dispY, dispTotal

    def _getFullSolution(self):
        """
        Return all solution variables, create integration points and update meshes
        """

        # get nodal displacements and update deformed node coordinates
        dispX, dispY, dispTotal = self._getNodalSolution()

        # get total number of integration points
        numberOfIntPoint = int(np.sum(self.mesh.elements.integrationOrder))

        # pre-allocation of integration points lists for inital and deformed mesh
        self.mesh.elements.integrationpointIds          = [[] for i in range(self.mesh.numberOfElements)]
        self.meshDeformed.elements.integrationpointIds  = [[] for i in range(self.meshDeformed.numberOfElements)] 
        self.mesh.integrationPoints.ids                 = np.arange(1,numberOfIntPoint+1)
        self.meshDeformed.integrationPoints.ids         = np.arange(1,numberOfIntPoint+1)
        self.mesh.integrationPoints.coordinates         = np.zeros([numberOfIntPoint,2],np.float64)
        self.meshDeformed.integrationPoints.coordinates = np.zeros([numberOfIntPoint,2],np.float64)

        curIntPointIndex = 0 # current integer point index (serves as a counter)

        # pre-allocation of element result arrays
        strainX     = np.zeros([numberOfIntPoint,1],np.float64)
        strainY     = np.zeros([numberOfIntPoint,1],np.float64)
        strainXY    = np.zeros([numberOfIntPoint,1],np.float64)
        stressX     = np.zeros([numberOfIntPoint,1],np.float64)
        stressY     = np.zeros([numberOfIntPoint,1],np.float64)
        stressZ     = np.zeros([numberOfIntPoint,1],np.float64)
        stressXY    = np.zeros([numberOfIntPoint,1],np.float64)
        stress11    = np.zeros([numberOfIntPoint,1],np.float64)
        stress22    = np.zeros([numberOfIntPoint,1],np.float64)
        stress33    = np.zeros([numberOfIntPoint,1],np.float64)
        stressMises = np.zeros([numberOfIntPoint,1],np.float64)

        # iterate trough each element and gather element result and integration point data
        for elementIndex,id in enumerate(self.mesh.elements.ids):
            nodeIds         = self.mesh.elements.nodeIds[elementIndex]
            nodeCoords, nodeIndex = self.mesh.nodes.findCoordinatesByNodeIds(nodeIds)
            deformedCoords, nodeIndex = self.meshDeformed.nodes.findCoordinatesByNodeIds(nodeIds)
            nodeSize        = nodeCoords.shape[0]
            order           = self.mesh.elements.integrationOrder[elementIndex]
            E               = self.mesh.elements.youngsModulus[elementIndex]
            nu              = self.mesh.elements.poissonsRatio[elementIndex]
            t               = self.mesh.elements.thickness[elementIndex]
            behaviour       = self.mesh.elements.planarAssumption[elementIndex]
            
            # get guide vector to extract current DOFs
            g = self._getMatrixGuideVector(nodeIndex)

            # gauss points for which the element result is determined
            if nodeSize in [3,6]: # triangle
                gaussPoints = self._getTriaGaussPoint(order) 
            elif nodeSize in [4,8]: # quad
                gaussPoints = self._getQuadGaussPoint(order) 

            # element D matrix for stress results
            D = self._getElementDMatrix(E,nu,behaviour) 

            # iterate trough all integration points of the elements
            for [xi,eta] in gaussPoints:
                B, detJ = self._getElementBMatrixandJacobiDeterminant(nodeCoords,xi,eta)

                # calculate strain and stress vector at current integration point
                strainVector = B@self.displacementVector[g]
                stressVector = D@B@self.displacementVector[g]
                
                # extract scalars form strain and stress vector
                strainX[curIntPointIndex]   = strainVector[0]
                strainY[curIntPointIndex]   = strainVector[1]
                strainXY[curIntPointIndex]  = strainVector[2]
                stressX[curIntPointIndex]   = stressVector[0]
                stressY[curIntPointIndex]   = stressVector[0]
                stressXY[curIntPointIndex]  = stressVector[0]

                # create the full 3x3 stress tensor for principal stresses
                sigX    = stressVector[0].item() 
                sigY    = stressVector[1].item() 
                sigXY   = stressVector[2].item() 
                
                # determine stress in z direction bases on behaviour
                if behaviour.lower() in [0, "plane stress","planestress","stress"]:
                    sigZ = 0
                else:
                    sigZ = nu * (sigX + sigY)

                # 3x3 stress tensor
                stressTensor = np.array([[sigX, sigXY, 0],
                                            [sigXY, sigY, 0],
                                            [0, 0, sigZ]])

                stressZ[curIntPointIndex]  = sigZ

                # calculate principal stresses (eigenvalues)
                eigenValues = np.linalg.eigvals(stressTensor)
                principalstresses = np.sort(eigenValues)[::-1]  # Sort in descending order
                sig1, sig2, sig3 = principalstresses

                stress11[curIntPointIndex] = sig1
                stress22[curIntPointIndex] = sig2
                stress33[curIntPointIndex] = sig3

                # calculate mises stress
                misesstress = np.sqrt(0.5 * ((sig1 - sig2)**2 + (sig2 - sig3)**2 + (sig3 - sig1)**2))
                stressMises[curIntPointIndex] = misesstress

                # assign integration point ids to element
                self.mesh.elements.integrationpointIds[elementIndex].append(curIntPointIndex+1)
                self.meshDeformed.elements.integrationpointIds[elementIndex].append(curIntPointIndex+1)

                # calculate integration point coordinates for mesh and deformed mesh
                self.mesh.integrationPoints.coordinates[curIntPointIndex,:]         = self._getIntegrationPointsCoordinates(nodeCoords,xi,eta)
                self.meshDeformed.integrationPoints.coordinates[curIntPointIndex,:] = self._getIntegrationPointsCoordinates(deformedCoords,xi,eta)

                # update current integration point index
                curIntPointIndex = curIntPointIndex+1

        # combine nodal solutions
        nodalSolution = (np.array(dispX), np.array(dispY), np.array(dispTotal))

        # combine element solutions
        elementSolution = (np.array(strainX), np.array(strainY), np.array(strainXY), np.array(stressX), np.array(stressY), np.array(stressXY), 
                            np.array(stress11), np.array(stress22), np.array(stress33), np.array(stressMises), np.array(stressMises))

        return nodalSolution, elementSolution

# --- Solution --- 
class Solution():
    def __init__(self, mesh=Mesh(), meshDeformed=Mesh(),
                 dispX=[], dispY=[], dispTotal=[],
                 strainX=[], strainY=[], strainXY=[], 
                stressX=[], stressY=[], stressXY=[],
                stress11=[], stress22=[], stress33=[],
                stressMises=[], stressZ=[]):
        
        """
        Contains all the solution variables of the model
        """

        self.mesh           = mesh
        self.meshDeformed   = meshDeformed
        self.dispX          = dispX
        self.dispY          = dispY
        self.dispTotal      = dispTotal
        self.strainX        = strainX
        self.strainY        = strainY
        self.strainXY       = strainXY
        self.stressX        = stressX        
        self.stressY        = stressY       
        self.stressXY       = stressXY
        self.stress11       = stress11       
        self.stress22       = stress22  
        self.stress33       = stress33
        self.stressMises    = stressMises
        self.stressZ        = stressZ

        # Complete the variables dictionary
        self.variables = {
            "dispX": self.dispX,
            "dispY": self.dispY,
            "dispTotal": self.dispTotal,
            "strainX": self.strainX,
            "strainY": self.strainY,
            "strainXY": self.strainXY,
            "stressX": self.stressX,
            "stressY": self.stressY,
            "stressXY": self.stressXY,
            "stress11": self.stress11,
            "stress22": self.stress22,
            "stress33": self.stress33,
            "stressMises": self.stressMises,
            "stressZ": self.stressZ
        }
    
    def _getAveragedResult(self,variableName):
        variable = self.variables[variableName]
        averagedResult = np.zeros([self.mesh.numberOfElements,1],dtype=np.float64)

        for elementIndex, pointIds in enumerate(self.mesh.elements.integrationpointIds):
            pointIndex = self.mesh.integrationPoints.findIndexByNodeIds(pointIds)
            averagedResult[elementIndex] = np.mean(variable[pointIndex])

        return averagedResult

# --- Model ---
class Model2d():
    """
    Model class that holds all data for a 2D FEM model.
    """
    def __init__(self, geometry=Geometry(), mesh=Mesh(), boundaries = Boundaries(), loads=Loads(), solverData = SolverData(), solution = Solution()):
        self.geometry   = geometry
        self.mesh = mesh
        self.meshDeformed = mesh
        self.boundaries = boundaries
        self.loads = loads 
        self.solverData = solverData
        self.solution = solution

    def printParameters(self):
        """
        Display all parameters of the model in a structured way.
        """
        print("Model parameters:")
        self.geometry.printParameters()
        self.mesh.printParameters()
        self.boundaries.printParameters()
        self.loads.printParameters()  
        
    def _checkParameters(self):
        """
        Check if all model parameters are valid and well defined.
        """
        #print("Check model parameters:")
        
        if not (self.mesh.elements.ids.shape[0] == len(self.mesh.elements.nodeIds) == self.mesh.elements.youngsModulus.shape[0]
                == self.mesh.elements.poissonsRatio.shape[0]  == self.mesh.elements.thickness.shape[0]  == self.mesh.elements.integrationOrder.shape[0]):
            raise ValueError("Elements not correctly defined!")
        if not (self.mesh.nodes.ids.shape[0] == self.mesh.nodes.coordinates.shape[0]):
            raise ValueError("Nodes not correctly defined!")
        if self.mesh.numberOfElements == 0 or self.mesh.numberOfNodes == 0:
            raise ValueError("Empty mesh!")
        
        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] !=0:
                raise ValueError("No points were defined for lines!")
            if self.boundaries.displacementOnPoints.ids.shape[0] !=0:
                raise ValueError("No points were defined for displacement on points!")
            
        if self.geometry.lines.ids.shape[0] == 0:
            if self.boundaries.displacementOnLines.ids.shape[0] !=0:
                raise ValueError("No points were defined for displacement on lines!")

    def generateQuadMesh(self, nx=1, ny=1, type = 4, specified_nodes=None, integrationOrder=4, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]):
        """Generates a Quad mesh for a rectangle

        Args:
            nx (int): Number of nodes in x direction
            ny (int): Number of nodes in y direction
            type (str, optional): "Quad4" or "Quad8". Defaults to 'Quad4'.
            specified_nodes (array, optional): Specify coordinates where aditional nodes should be placed . Defaults to None.
        """        
        if type in ['Quad4',4]:
            xmin = np.min(self.geometry.points.x)
            xmax = np.max(self.geometry.points.x)
            ymin = np.min(self.geometry.points.y)
            ymax = np.max(self.geometry.points.y)
            x = np.linspace(xmin, xmax,nx)
            y = np.linspace(ymin, ymax,ny)
            #Füge spezifische nodes hinzu die in specified_nodes angegeben sind
            #Wird vor allem für die mesh_polygon funktion gebraucht
            if specified_nodes is not None:
                x = np.union1d(x,specified_nodes[:,0])
                nx=x.size
                y = np.union1d(y,specified_nodes[:,1])
                ny=y.size
            xx,yy = np.meshgrid(x,y)
            self.mesh.nodes= Nodes(np.vstack([xx.ravel(), yy.ravel()]).T)
            #self.mesh.nodes.setIds(self.mesh.nodes.ids)

        
            connectivity = []
        
            # Schleife über alle elemente, bei jedem element alle vier knoten die dazugehören berechnen
            for i in range(ny-1): #durch zeilen iterieren; n knoten in x richting => n-1 elemente in x richtung
                for j in range(nx-1): # durch spalten iterieren
                    n0 = i * (nx) + j + 1
                    # erklärung für n0: i * (nx) => Erster knoten in der Zeile + j => die jeweilige spalte
                    n1 = n0 + 1 # 1 nach rechts von n0
                    n3 = n0 + nx #zuers n3 alos oben links berechen
                    n2 = n3 + 1 # 1 nach rechts von n3
                    connectivity.append([n0, n1, n2, n3])
            connectivity = np.array(connectivity)
            self.mesh.elements = Elements(nodeIds = connectivity, thickness=thickness, youngsModulus=youngsModulus, 
                                          poissonsRatio=poissonRation, planarAssumption=planarAssumption)
        elif type in ['Quad8',8]:
           raise("Quad8 not supportet yet")

        self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])

    def generateTriangleMesh(self,size, type=3, integrationOrder=1, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]):
        """Creates a triangle mesh using the pygmsh library

        Args:
            size (float): element size
            type (int, optional): type of the element 3=>tria3; 6 => tria6. Defaults to 3.
            integrationOrder (int,optional): number of integration points per element. Deaults to 4
        """     
        import pygmsh #externe meshing bibliothek         
        vertices = self.geometry.points.coordinates
        with pygmsh.geo.Geometry() as pygeom:
            pygeom.add_polygon(
                vertices,
                mesh_size=size,)

            if type == 3:
                keyType = 1
            elif type == 6:
                keyType = 2
            else:
                raise ValueError(f"Type TRIA-{type} not implemented!")

            gmsh = pygeom.generate_mesh(order=keyType)
            keys = ["triangle","triangle6","triangle10"]
            connectivity = np.array(gmsh.cells_dict[keys[keyType-1]])+1
            points = np.array(gmsh.points)
            self.mesh.nodes = Nodes(coordinates = points[:,[0,1]])
            self.mesh.nodes.setIds(self.mesh.nodes.ids)

            self.mesh.elements = Elements(nodeIds = connectivity, thickness=thickness, youngsModulus=youngsModulus, 
                                          poissonsRatio=poissonRation, planarAssumption=planarAssumption)
            self.mesh.elements.setIds(self.mesh.elements.ids)
            self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])
            pass
    
    def importNasFile(self,filename,integrationOrder=1, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]):
        from pyNastran.bdf.bdf import BDF
        model = BDF()

        model.read_bdf(filename,xref=False)


        coords = model.get_xyz_in_coord()[:,[0,2]]
        all_node_ids = list(model.node_ids)
        number_of_node = model.nnodes

        #nodeIDs = np.array([model.get_node_ids_with_elements([i],return_array=True) for i in model.element_ids])
        nodeIDs = np.array([model.elements[i].node_ids for i in model.element_ids])

        if nodeIDs.shape[1] not in [3,4,6,8]:
            # If elements have Three nodes, the colummns are already in the correct order
            raise('Import is only implemented for elements of type: {Tria3;Tria3; Quad4; Quad8}') 

        
        self.mesh.nodes = Nodes(coordinates = coords,ids = all_node_ids)
        self.mesh.elements = Elements(nodeIds = nodeIDs, thickness=thickness, youngsModulus=youngsModulus, 
                                          poissonsRatio=poissonRation, planarAssumption=planarAssumption)
        self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])

    def solve(self):
        """
        Assemble the equation matrices from mesh, boundaries and load definitions and solve them
        """
        self._checkParameters()
        start_time = time.perf_counter()
        self.meshDeformed = copy.deepcopy(self.mesh)
        self.solverData = SolverData(self.mesh,self.meshDeformed)
        self.solverData._combineBoundaries(self.geometry, self.boundaries)
        self.solverData._combineLoads(self.geometry, self.loads)
        self.solverData._buildStiffnessMatrix()
        self.solverData._buildLoadVector()
        self.solverData._applyPrescribedDisplacements()
        self.solverData._reduceStiffnesMatrixAndLoadVector()
        self.solverData._solveLinearEquation()

        end_time = time.perf_counter()
        self.solverData.elapsedTime = end_time - start_time

        self.solverData.status = "finished"

        nodalSolution, elementSolution = self.solverData._getFullSolution()
        self.solution = Solution(self.mesh,self.meshDeformed,
                                 nodalSolution[0],nodalSolution[1],nodalSolution[2],
                                 elementSolution[0],elementSolution[1],elementSolution[2],
                                 elementSolution[3],elementSolution[4],elementSolution[5], 
                                 elementSolution[6],elementSolution[7],elementSolution[8],
                                 elementSolution[9],elementSolution[10])
        pass

    def plotSolution(self,variableName,averaged=False,deformed=True):
        """Plots the deformed mesh with each element colored according the value of "variable".


        For each element the average of the value at its integration points or nodes is calculated and plotted.
        Args:
            variableName (_string_): Name of the variable to be plotted. Options are:
              ['dispX', 'dispY', 'dispTotal', 'strainX', 'strainY', 'strainXY', 'stressX', 'stressY', 'stressXY', 'stress11', 'stress22', 'stress33', 'stressMises']
        """
        
        variable = self.solution.variables[variableName]

        if deformed == True:
            coords = self.solution.meshDeformed.nodes.coordinates
        else:
            coords = self.solution.mesh.nodes.coordinates
        
        var_min = variable.min()
        var_max = variable.max()
        # Setup for the plot
        fig = plt.figure(1)
        ax = fig.add_subplot()

        if averaged == True:
            # If variable is calculted at the integration points: get the average value of the variable for each element
            # If the variable calculated at the nodes(displacement): the averageing is done inside the plotting loop to save computational cost
            if variableName[:4] != 'disp':
                averagedResult = self.solution._getAveragedResult(variableName)

            # Iterate through all elements by iterating through the nodeIDs vector
            for index,nodeIds in enumerate(self.mesh.elements.nodeIds):
                # Get the the deformed coordinates of the nodes belonging to the current element
                # If elementtype is TRIA6: use only first three coordinates for plotting
                if len(nodeIds) == 6:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds[[0,3,1,4,2,5]])
                # If elementtype is Quad8: use only first four coordinates for plotting
                elif len(nodeIds) == 8:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds[[0,4,1,5,2,6,3,7]])
                else:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds)
                element_coords = coords[elementNodeIndex]
                    
                # If the variable is a deformation, the average is calculated inside the loop.
                # This way the "nodeIDs" that were calculated via "findIndexByNodeIds()" can be reused
                if variableName[:4] == 'disp':
                    # Get the average deformation of the nodes belonging to the urrent element
                    average_variable = variable[elementNodeIndex].mean() #nodeIds can be used since deformations are stored in the same order as the nodes
                else:
                    average_variable = averagedResult[index]

                # map deformation to colormap
                cmap = plt.get_cmap('jet')
                color = cmap((average_variable - var_min)/(var_max - var_min))
                
                ax.fill(element_coords[:,0],element_coords[:,1], edgecolor='cyan', facecolor=color)
                ax.set_aspect('equal', adjustable='box')

        # If averaged = false   
        else:

            if variableName[:4] != 'disp':
                if deformed == True:
                    coords = self.solution.meshDeformed.integrationPoints.coordinates
                    mesh = self.solution.meshDeformed
                else:
                    coords = self.solution.mesh.integrationPoints.coordinates
                    mesh = self.solution.mesh
            else:
                if deformed == True:
                    coords = self.solution.meshDeformed.nodes.coordinates
                    mesh = self.solution.meshDeformed
                else:
                    coords = self.solution.mesh.nodes.coordinates
                    mesh = self.solution.mesh
            # map value to colormap 
            cmap = plt.get_cmap('jet')
            color = cmap((variable - var_min)/(var_max - var_min))
            
            plt.scatter(coords[:,0],coords[:,1],c=color,s=150)
            mesh.plotMesh()
            ax.set_aspect('equal', adjustable='box')
                
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=var_min, vmax=var_max))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax) 
        cbar.set_label(variableName)
        return fig
            
    def plotBoundaries(self, deformed=False):

        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] !=0:
                raise ValueError("No points were defined for lines!")
            if self.boundaries.displacementOnPoints.ids.shape[0] !=0:
                raise ValueError("No points were defined for displacement on points!")
            if self.loads.loadsOnPoints.ids.shape[0] !=0:
                raise ValueError("No points were defined for loads on points!")
            
        if self.geometry.lines.ids.shape[0] == 0:
            if self.boundaries.displacementOnLines.ids.shape[0] !=0:
                raise ValueError("No points were defined for displacement on lines!")
            if self.loads.loadsOnLines.ids.shape[0] !=0:
                raise ValueError("No points were defined for loads on lines!")

        if self.solverData.status == "unfinished":
            temp_solverData = SolverData(mesh=self.mesh)
            temp_solverData._combineBoundaries(geometry=self.geometry, boundaries=self.boundaries)
            displacementOnNodes = temp_solverData.nodalDisplacements
        else:
            displacementOnNodes = self.solverData.nodalDisplacements

        x_fixed_ids = displacementOnNodes._getNodeIdsWithFixationX()
        y_fixed_ids = displacementOnNodes._getNodeIdsWithFixationY()
        x_displacement_values, x_displacement_ids = displacementOnNodes._getPrescribedNodalDispalcementX()
        y_displacement_values, y_displacement_ids = displacementOnNodes._getPrescribedNodalDispalcementY()

        if deformed:
            mesh = self.solution.meshDeformed
        else:
            mesh = self.mesh

        x_fixed_coords = mesh.nodes.findCoordinatesByNodeIds(x_fixed_ids)[0]
        y_fixed_coords = mesh.nodes.findCoordinatesByNodeIds(y_fixed_ids)[0]
        x_displacement_coords = mesh.nodes.findCoordinatesByNodeIds(x_displacement_ids)[0]
        y_displacement_coords = mesh.nodes.findCoordinatesByNodeIds(y_displacement_ids)[0]

        plt.scatter(x_fixed_coords[:, 0], x_fixed_coords[:, 1], marker=5, s=100, c='magenta', label="x fixed")
        plt.scatter(y_fixed_coords[:, 0], y_fixed_coords[:, 1], marker=6, s=100, c='lime', label="y fixed")

        # Adjust markers based on displacement direction
        x_displacement_markers = []
        for value in x_displacement_values:
            if isinstance(value, (int, float)):
                if value < 0:
                    x_displacement_markers.append('$\\leftarrow$')
                elif value > 0:
                    x_displacement_markers.append('$\\rightarrow$')
                else:
                    x_displacement_markers.append('')  # For zero
            else:
                x_displacement_markers.append('')  # For None string values

        y_displacement_markers = []
        for value in y_displacement_values:
            if isinstance(value, (int, float)):
                if value < 0:
                    y_displacement_markers.append('$\\downarrow$')
                elif value > 0:
                    y_displacement_markers.append('$\\uparrow$')
                else:
                    y_displacement_markers.append('')  # For zero
            else:
                y_displacement_markers.append('')  # For None or string values

        for i, (x, y) in enumerate(x_displacement_coords):
            plt.scatter(x, y, marker=x_displacement_markers[i], s=100, c='magenta')

        for i, (x, y) in enumerate(y_displacement_coords):
            plt.scatter(x, y, marker=y_displacement_markers[i], s=100, c='lime')

        plt.axis('square')
        
    def plotLoads(self, deformed=False):

        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] !=0:
                raise ValueError("No points were defined for lines!")
            if self.loads.loadsOnPoints.ids.shape[0] !=0:
                raise ValueError("No points were defined for loads on points!")
            
        if self.geometry.lines.ids.shape[0] == 0:
            if self.loads.loadsOnLines.ids.shape[0] !=0:
                raise ValueError("No points were defined for loads on lines!")
        
        
        if self.solverData.status == "unfinished":
            temp_solverData = SolverData(mesh=self.mesh)
            temp_solverData._combineLoads(geometry=self.geometry, loads=self.loads)
            loadsOnNodes = temp_solverData.nodalLoads
        else:
            loadsOnNodes = self.solverData.nodalLoads

        nodeIDs = loadsOnNodes.nodeIds
        x_force_ids = []
        y_force_ids = []
        x_force_values = []
        y_force_values = []

        for i, load in enumerate(loadsOnNodes.loads):
            if load[0] != 0:
                x_force_ids.append(nodeIDs[i])
                x_force_values.append(load[0])

            if load[1] != 0:
                y_force_ids.append(nodeIDs[i])
                y_force_values.append(load[1])

        if deformed:
            mesh = self.solution.meshDeformed
        else:
            mesh = self.mesh

        x_force_coords = mesh.nodes.findCoordinatesByNodeIds(x_force_ids)[0]
        y_force_coords = mesh.nodes.findCoordinatesByNodeIds(y_force_ids)[0]

        # Adjust markers based on force direction
        x_force_markers = ['$\\Leftarrow$' if value < 0 else '$\\Rightarrow$' for value in x_force_values]
        y_force_markers = ['$\\Downarrow$' if value < 0 else '$\\Uparrow$' for value in y_force_values]

        for i, (x, y) in enumerate(x_force_coords):
            plt.scatter(x, y, marker=x_force_markers[i], s=150, c='magenta')

        for i, (x, y) in enumerate(y_force_coords):
            plt.scatter(x, y, marker=y_force_markers[i], s=150, c='lime')

        plt.axis('square')

    def plotMesh(self,deformed=False, color_test = False, show_ids = False):
        """
        Plots the mesh

        Parameters:
        color_test (bool) -- ???
        show_ids (bool) -- True to displays node identifiers
        """
        if deformed:
            self.meshDeformed.plotMesh(color_test=color_test,show_ids=show_ids)
        else:
            self.mesh.plotMesh(color_test=color_test,show_ids=show_ids)

        """
        for elementIndex,elementNodeIds in enumerate(self.mesh.elements.nodeIds):
            elementNodeIds =np.array(elementNodeIds)
           # If elementtype is TRIA6: use defined order to get correct nodes
            if len(elementNodeIds) == 6:
                elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(elementNodeIds[[0,3,1,4,2,5]])
            # If elementtype is Quad8: use defined order to get correct nodes
            elif len(elementNodeIds) == 8:
                elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(elementNodeIds[[0,4,1,5,2,6,3,7]])
            else:
                elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(elementNodeIds)

            coords = self.mesh.nodes.coordinates[elementNodeIndex]
            
            midpoint = np.mean(coords,axis=0)
            if color_test == False:
                color = 'none'
            else:
                cmap = plt.get_cmap('jet')
                color = cmap(elementIndex/self.mesh.elements.ids.shape[0])
                
            plt.fill(coords[:,0],coords[:,1], edgecolor='cyan', facecolor=color)
            
            if show_ids == True:
                plt.text(midpoint[0],midpoint[1], self.mesh.elements.ids[elementIndex], fontsize=12,color='cyan',ha='center',va='center')

                plt.axis('square')
        """

    def plotSolutionVTK(self, deformed=True, variableName="dispTotal"):
        """
        Plot the solution using VTK.

        Parameters:
        deformed (bool) -- If True, plot the deformed shape; if False, plot the original shape.
        variableName (str) -- The name of the variable to plot (e.g., 'stressX', 'dispX', etc.)
        """
        import vtk
        # Get the mesh and coordinates
        if deformed:
            coordinates = self.solution.meshDeformed.nodes.coordinates
        else:
            coordinates = self.solution.mesh.nodes.coordinates
        
        # Create a VTK points object
        vtk_points = vtk.vtkPoints()
        for coord in coordinates:
            vtk_points.InsertNextPoint(coord[0], coord[1], 0)  # Assuming z=0 for 2D

        # Create a VTK cell array to hold the mesh elements
        vtk_cells = vtk.vtkCellArray()

        # Add elements to vtk_cells
        element_ids = self.solution.mesh.elements.ids
        for element in self.solution.mesh.elements.nodeIds:
            # Adjusting for 1-based indexing
            adjusted_element = [node_id - 1 for node_id in element]  # Convert to 0-based index
            if len(adjusted_element) == 3:  # TRIANGLE
                vtk_cells.InsertNextCell(3, adjusted_element)  # For TRIA3
            elif len(adjusted_element) == 6:  # TRIANGLE
                vtk_cells.InsertNextCell(6, adjusted_element)  # For TRIA6
            elif len(adjusted_element) == 4:  # QUAD
                vtk_cells.InsertNextCell(4, adjusted_element)  # For QUAD4
            elif len(adjusted_element) == 8:  # QUAD
                vtk_cells.InsertNextCell(8, adjusted_element)  # For QUAD8

        # Create a vtkPolyData object
        vtk_poly_data = vtk.vtkPolyData()
        vtk_poly_data.SetPoints(vtk_points)
        vtk_poly_data.SetPolys(vtk_cells)

        # Set the scalar data for the variableName
        data = getattr(self.solution, variableName)  # Retrieve stress data

        # Create a vtkArray to hold the scalar data
        vtk_data_array = vtk.vtkFloatArray()
        vtk_data_array.SetName(variableName)
        vtk_data_array.SetNumberOfComponents(1)
        vtk_data_array.SetNumberOfTuples(len(data))

        for i, value in enumerate(data):
            vtk_data_array.SetValue(i, value)

        # Add the scalar data to the polydata
        vtk_poly_data.GetPointData().AddArray(vtk_data_array)
        vtk_poly_data.GetPointData().SetScalars(vtk_data_array)

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(vtk_poly_data)

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        # Create a renderer, render window, and interactor
        renderer = vtk.vtkRenderer()
        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window_interactor = vtk.vtkRenderWindowInteractor()
        render_window_interactor.SetRenderWindow(render_window)

        # Add the actor to the scene
        renderer.AddActor(actor)
        renderer.SetBackground(1, 1, 1)  # Set background color to white

        # Render and interact
        render_window.Render()

        render_window_interactor.Start()