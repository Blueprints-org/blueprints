import copy
import math
import time

import numpy as np

from blueprints.utils.femlearn.boundary_conditions import Boundaries
from blueprints.utils.femlearn.geometry import Geometry
from blueprints.utils.femlearn.loads import Loads
from blueprints.utils.femlearn.mesh import Mesh


class _ShapeFunctions:
    def __init__(self):
        """
        Contains pre defined shape function matrices
        """
        self._matrixTRIA3 = np.array([[1, 0, 0], [-1, 1, 0], [-1, 0, 1]])

        self._matrixTRIA6 = np.array(
            [[1, 0, 0, 0, 0, 0], [-3, -1, 0, 4, 0, 0], [-3, 0, -1, 0, 0, 4], [4, 0, 0, -4, 4, -4], [2, 2, 0, -4, 0, 0], [2, 0, 2, 0, 0, -4]]
        )

        self._matrixQUAD4 = np.array([[1, 1, 1, 1], [-1, 1, 1, -1], [-1, -1, 1, 1], [1, -1, 1, -1]]) / 4

        self._matrixQUAD8 = (
            np.array(
                [
                    [-1, -1, -1, -1, 2, 2, 2, 2],
                    [0, 0, 0, 0, 0, 2, 0, -2],
                    [0, 0, 0, 0, -2, 0, 2, 0],
                    [1, -1, 1, -1, 0, 0, 0, 0],
                    [1, 1, 1, 1, -2, 0, -2, 0],
                    [1, 1, 1, 1, 0, -2, 0, -2],
                    [-1, -1, 1, 1, 2, 0, -2, 0],
                    [-1, 1, 1, -1, 0, -2, 0, 2],
                ]
            )
            / 4
        )

        self._lineLoadLinear = [1 / 2, 1 / 2]
        self._lineLoadQuadtratic = [1 / 6, 1 / 6, 4 / 6]

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
            dNdXi = np.array([0, 1, 0, eta, 2 * xi, 0]) @ self._matrixTRIA6
            dNdEta = np.array([0, 0, 1, xi, 0, 2 * eta]) @ self._matrixTRIA6
        elif eType in ["QUAD4", 4]:
            dNdXi = np.array([0, 1, 0, eta]) @ self._matrixQUAD4
            dNdEta = np.array([0, 0, 1, xi]) @ self._matrixQUAD4
        elif eType in ["QUAD8", 8]:
            dNdXi = np.array([0, 1, 0, eta, 2 * xi, 0, 2 * xi * eta, eta**2]) @ self._matrixQUAD8
            dNdEta = np.array([0, 0, 1, xi, 0, 2 * eta, xi**2, xi * eta * 2]) @ self._matrixQUAD8
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


class _GaussPoints:
    def __init__(self):
        """
        Pre defined integration points and weights
        """

        # Integration wheights
        self._triaWeightsOrder1 = np.array([0.5])
        self._triaWeightsOrder3 = np.array([1 / 6, 1 / 6, 1 / 6])
        self._triaWeightsOrder4 = np.array([-9 / 32, 25 / 96, 25 / 96, 25 / 96])
        self._triaWeightsOrder7 = np.array([1 / 40, 1 / 15, 1 / 40, 1 / 15, 1 / 40, 1 / 15, 9 / 40])

        self._quadWeightsOrder1 = np.array([4])
        self._quadWeightsOrder4 = np.array([1, 1, 1, 1])
        self._quadWeightsOrder9 = np.array([25 / 81, 40 / 81, 25 / 81, 40 / 81, 64 / 81, 40 / 81, 25 / 81, 40 / 81, 25 / 81])

        # Integration point coordinates
        self._triaPointOrder1 = np.array([[1 / 3, 1 / 3]])
        self._triaPointOrder3 = np.array([[1 / 6, 1 / 6], [2 / 3, 1 / 6], [1 / 6, 2 / 3]])
        self._triaPointOrder4 = np.array([[1 / 3, 1 / 3], [3 / 5, 1 / 5], [1 / 5, 3 / 5], [1 / 5, 1 / 5]])
        self._triaPointOrder7 = np.array([[0, 0], [1 / 2, 0], [1, 0], [1 / 2, 1 / 2], [0, 1], [0, 1 / 2], [1 / 3, 1 / 3]])

        self._quadPointOrder1 = np.array([[0, 0]])
        self._quadPointOrder4 = np.array(
            [
                [-1 / math.sqrt(3), -1 / math.sqrt(3)],
                [1 / math.sqrt(3), -1 / math.sqrt(3)],
                [1 / math.sqrt(3), 1 / math.sqrt(3)],
                [-1 / math.sqrt(3), 1 / math.sqrt(3)],
            ]
        )
        self._quadPointOrder9 = np.array(
            [
                [-math.sqrt(0.6), -math.sqrt(0.6)],
                [0, -math.sqrt(0.6)],
                [math.sqrt(0.6), -math.sqrt(0.6)],
                [-math.sqrt(0.6), 0],
                [0, 0],
                [math.sqrt(0.6), 0],
                [-math.sqrt(0.6), math.sqrt(0.6)],
                [0, math.sqrt(0.6)],
                [math.sqrt(0.6), math.sqrt(0.6)],
            ]
        )

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

        self.status = "unfinished"
        self.elapsedTime = None

        self.mesh = mesh  # original mesh
        self.meshDeformed = meshDeformed  # deformed mesh

        self.numberDOF = 0  # number of DOFs (fixed DOFs are not included)
        self.fixedDOF = []  # DOFs (refers to column index in the stiffness matrix) that are fixed
        self.openDOF = []  # DOFs (refers to column index in the stiffness matrix) that are free

        self.nodalLoads = Loads().loadsOnNodes  # all loads compremised to only nodal loads object
        self.nodalDisplacements = Boundaries().displacementOnNodes  # all loads compremised to only nodal displacements objcect

        self.stiffnessMatrix = []  # global stiffness matrix
        self.displacementVector = []  # displacement vector
        self.loadVector = []  # load vector

        self.reducedStiffnessMatrix = []  # reduced  global stiffness matrix
        self.reducedDisplacementVector = []  # reduced  displacement vector
        self.reducedLoadVector = []  # reduced  load vector

    def _getIntegrationPointsCoordinates(self, nodeCoords=np.empty([1, 2]), xi=0.0, eta=0.0):
        """
        Return the global coordinates ot the integration points based on the element nodes
        """
        nodeCoords = np.array(nodeCoords)
        N = self._getShapeFunctionCoefficients(xi, eta, nodeCoords.shape[0])
        coords = N @ nodeCoords  # [x,y] coordinates

        return coords

    def _getElementDMatrix(self, E=0.0, nu=0.0, behaviour=""):
        """
        Returns the material behaviour as a matrix (D Matrix)
        """
        if behaviour.lower() in [0, "plane stress", "planestress", "stress"]:
            D = E / (1 - nu**2) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
        elif behaviour.lower() in [1, "plane strain", "planestrain", "strain"]:
            D = E / ((1 + nu) * (1 - 2 * nu)) * np.array([[1 - nu, nu, 0], [nu, 1 - nu, 0], [0, 0, 1 / 2 - nu]])
        else:
            raise Exception(f"Behaviour type {behaviour} not defined! (0 for plane stress, 1 for plane strain)")
        return D

    def _getElementBMatrixandJacobiDeterminant(self, nodeCoords=np.empty([1, 2]), xi=0.0, eta=0.0):
        """
        Returns the B Matrix and the jacobi determinant
        """
        # Use derivates to calculate jacobi matrix
        dNdXi, dNdEta = self._getShapeFunctionDerivateCoefficients(xi, eta, nodeCoords.shape[0])

        dXdXi = dNdXi @ nodeCoords[:, 0]
        dXdEta = dNdEta @ nodeCoords[:, 0]
        dYdXi = dNdXi @ nodeCoords[:, 1]
        dYdEta = dNdEta @ nodeCoords[:, 1]

        J = np.array([[dXdXi, dXdEta], [dYdXi, dYdEta]])

        J_inv = np.linalg.inv(J)

        # B1 Matrix
        B1 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 1, 0]])

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

        return B, np.linalg.det(J)

    def _getElementKMatrix(self, nodeCoords=np.empty([1, 2]), order=0, E=0.0, nu=0.0, t=0.0, behaviour=""):
        """
        Return the stiffness matrix for a single element
        """
        nodeSize = nodeCoords.shape[0]
        ke = np.zeros((2 * nodeSize, 2 * nodeSize))  # pre allocate element stiffness matrix

        D = self._getElementDMatrix(E, nu, behaviour)  # get element D matrix

        if nodeSize in [3, 6]:  # triangle
            gaussPoints = self._getTriaGaussPoint(order)
            gaussWeights = self._getTriaGaussWeights(order)
        elif nodeSize in [4, 8]:  # quad
            gaussPoints = self._getQuadGaussPoint(order)
            gaussWeights = self._getQuadGaussWeights(order)

        # iterate trough all integration points and sum up matrices
        for index, [xi, eta] in enumerate(gaussPoints):
            B, detJ = self._getElementBMatrixandJacobiDeterminant(nodeCoords, xi, eta)
            ke = ke + gaussWeights[index] * np.transpose(B) @ D @ B * detJ

        return ke * t

    def _getMatrixGuideVector(self, nodeIndex=np.empty([1, 1])):
        """
        Return a guide vector that contains the position of a DOF in the global stiffness matrix based on the node index
        """
        nodeSize = len(nodeIndex)  # Number of nodes
        g = np.zeros(2 * nodeSize, dtype=int)  # Preallocate guide vector

        for i in range(nodeSize):
            g[2 * i] = 2 * nodeIndex[i]  # x direction (even numbers)
            g[2 * i + 1] = 2 * nodeIndex[i] + 1  # y direction (odd numbers)
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

    def _findNodesBetweenTwoPoints(self, nodeCoords, pointCoords, tolerance=1e-15):
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
                if min(start[0], end[0]) <= projected_point[0] <= max(start[0], end[0]) and min(start[1], end[1]) <= projected_point[1] <= max(
                    start[1], end[1]
                ):
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
                node_load_dict[node_id] = {"load": load, "loadId": load_id}

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
        nodeCoords = self.mesh.nodes.coordinates
        nodeIds = self.mesh.nodes.ids

        # transfer boundaries on geometrical points to nodes
        if not (boundaries.displacementOnPoints.pointIds.shape[0] == 0 or len(boundaries.displacementOnPoints.displacements) == 0):
            pointIds = boundaries.displacementOnPoints.pointIds
            pointDisp = boundaries.displacementOnPoints.displacements
            pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
            nodeIndices = self._findNearestNeighbour(nodeCoords, pointCoords)
            for pointIndex, nodeIndex in enumerate(nodeIndices):
                self.nodalDisplacements.add(pointDisp[pointIndex], nodeIds[nodeIndex])

        # transfer boundaries on geometrical lines to nodes
        if not (boundaries.displacementOnLines.lineIds.shape[0] == 0 or len(boundaries.displacementOnLines.displacements) == 0):
            # iterate trough all line displacements and get nodes that lie on the current line
            for lineDispIndex, lineId in enumerate(boundaries.displacementOnLines.lineIds):
                lineDisp = boundaries.displacementOnLines.displacements[lineDispIndex]  # displacement amplitude
                lineIndex = geometry.lines._findIndexByLineIds(lineId)  # line index
                pointIds = geometry.lines.pointIds[lineIndex][0]
                pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
                nodeIndices = self._findNodesBetweenTwoPoints(nodeCoords, pointCoords)
                if nodeIndices.size != 0:
                    for nodeIndex in nodeIndices:
                        self.nodalDisplacements.add(lineDisp, nodeIds[nodeIndex])
                else:
                    print(f"No nodes were found on line {lineId}!")

        # Resolve conflicts for nodes with multiple displacements
        self._resolveDuplicateDisplacements()

    def _combineLoads(self, geometry=Geometry(), loads=Loads()):
        """
        Combine all the loads defined in the model to only nodal displacements
        """
        # make a deep copy of loads on Nodes
        self.nodalLoads = copy.deepcopy(loads.loadsOnNodes)

        # get node coordinates
        nodeCoords = self.mesh.nodes.coordinates
        nodeIds = self.mesh.nodes.ids

        # transfer loads on geometrical points to nodes
        if not (loads.loadsOnPoints.pointIds.shape[0] == 0 or loads.loadsOnPoints.loads.shape[0] == 0):
            pointIds = loads.loadsOnPoints.pointIds
            pointLoads = loads.loadsOnPoints.loads
            pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)
            nodeIndices = self._findNearestNeighbour(nodeCoords, pointCoords)
            for pointIndex, nodeIndex in enumerate(nodeIndices):
                self.nodalLoads.add(pointLoads[pointIndex], nodeIds[nodeIndex])

        # transfer loads on geometrical lines to nodes
        if not (loads.loadsOnLines.lineIds.shape[0] == 0 or loads.loadsOnLines.loads.shape[0] == 0):
            # iterate trough all line loads and get nodes that lie on the current line
            for lineLoadIndex, lineId in enumerate(loads.loadsOnLines.lineIds):
                lineLoad = loads.loadsOnLines.loads[lineLoadIndex]  # load amplitude
                lineIndex = geometry.lines._findIndexByLineIds(lineId)  # line index
                pointIds = geometry.lines.pointIds[lineIndex][0]  # vertices of line
                pointCoords, pointIndex = geometry.points.findCoordinatesByNodeIds(pointIds)  # coordinates of line vertices
                nodesOnLineIndex = self._findNodesBetweenTwoPoints(nodeCoords, pointCoords)  # nodes between vertices
                if nodesOnLineIndex.size != 0:
                    nodesOnLineIds = self.mesh.nodes.ids[nodesOnLineIndex]
                    # iterate through all elements in mesh
                    for elementIndex, elementId in enumerate(self.mesh.elements.ids):
                        # find node properties of current element
                        elementNodeIds = self.mesh.elements.nodeIds[elementIndex]
                        elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(elementNodeIds)

                        # find all nodes of the current element that are on the current line
                        elementNodeIndexOnLine = [nodeIndex for nodeIndex in elementNodeIndex if nodeIndex in nodesOnLineIndex]
                        elementNodeIdsOnLine = self.mesh.nodes.ids[elementNodeIndexOnLine]
                        elementCoordsOnLine = self.mesh.nodes.coordinates[elementNodeIndexOnLine]

                        # get element edge length (based on the numbering convention element vertices must follow each other)
                        if len(elementNodeIndexOnLine) > 1:
                            edgeLength = math.sqrt(
                                (elementCoordsOnLine[1, 0] - elementCoordsOnLine[0, 0]) ** 2
                                + (elementCoordsOnLine[1, 1] - elementCoordsOnLine[0, 1]) ** 2
                            )

                            # check if definitions are wrong
                            if len(elementNodeIds) in [3, 4]:  # linear shape function
                                if len(elementNodeIndexOnLine) != 2:
                                    raise ValueError(f"Linear element {elementId} appears to have more than two nodes on line {lineId}!")

                            elif len(elementNodeIds) in [6, 8, 9]:  # quadratic shape function
                                if len(elementNodeIndexOnLine) == 2:
                                    raise ValueError(f"Load on line {lineId} appears to not end on quadratic element {elementId} vertices!")
                                elif len(elementNodeIndexOnLine) != 3:
                                    raise ValueError(f"Quadratic element {elementId} appears to have more than three nodes on line {lineId}!")

                            # get line coefficients and add nodal force for each node
                            loadCoefficients = self._getLineLoadCoefficients(len(elementNodeIds))
                            for index, coeff in enumerate(loadCoefficients):
                                # this loop relies on the numbering convention -> vertix nodes allways come first in list
                                self.nodalLoads.add([coeff * edgeLength * lineLoad[0], coeff * edgeLength * lineLoad[1]], elementNodeIdsOnLine[index])
                else:
                    print(f"No nodes were found on line {lineId}!")

        # Resolve conflicts for nodes with multiple displacements
        self._resolveDuplicateLoads()

    def _buildStiffnessMatrix(self):
        """
        Assemble the global stiffness matrix based on the model mesh
        """

        # pre-allocation based on the DOFs
        self.stiffnessMatrix = np.zeros([2 * self.mesh.numberOfNodes, 2 * self.mesh.numberOfNodes])

        # iterate trough all elements in the mesh and insert element stiffness matrix
        for elementIndex, id in enumerate(self.mesh.elements.ids):
            nodeIds = self.mesh.elements.nodeIds[elementIndex]
            nodeCoords, nodeIndex = self.mesh.nodes.findCoordinatesByNodeIds(nodeIds)
            order = self.mesh.elements.integrationOrder[elementIndex]
            E = self.mesh.elements.youngsModulus[elementIndex]
            nu = self.mesh.elements.poissonsRatio[elementIndex]
            t = self.mesh.elements.thickness[elementIndex]
            behaviour = self.mesh.elements.planarAssumption[elementIndex]

            # element stiffness
            ke = self._getElementKMatrix(nodeCoords, order, E, nu, t, behaviour)

            # insert element stiffness using the guide vectors
            g = self._getMatrixGuideVector(nodeIndex)
            self.stiffnessMatrix[np.ix_(g, g)] = self.stiffnessMatrix[np.ix_(g, g)] + ke

    def _buildLoadVector(self):
        """
        Build load vector
        """

        # pre-allocation of load vector
        self.loadVector = np.zeros([2 * self.mesh.numberOfNodes, 1])

        # get DOF index in the global load vector for each node with a load
        index = np.array(self.mesh.nodes.findIndexByNodeIds(self.nodalLoads.nodeIds))

        # align x and y direction into a single vector
        loads = self.nodalLoads.loads.flatten()

        # insert loads at the right position of the load vector
        g = self._getMatrixGuideVector(index)
        self.loadVector[g, 0] = loads

    def _applyPrescribedDisplacements(self):
        """
        Consider prescribed nodal displacements by adjusting stiffness matrix and load vector
        """

        # Get node index for prescribed displacements other than 0
        xDisp, xDispNodeId = self.nodalDisplacements._getPrescribedNodalDispalcementX()
        xDispNodeIndex = self.mesh.nodes.findIndexByNodeIds(xDispNodeId)
        yDisp, yDispNodeId = self.nodalDisplacements._getPrescribedNodalDispalcementY()
        yDispNodeIndex = self.mesh.nodes.findIndexByNodeIds(yDispNodeId)

        # create line with all zeros for adjusting the stiffness matrix
        zeroLine = np.zeros(self.stiffnessMatrix.shape[1])

        # consider x dislacements
        for dispIndex, nodeIndex in enumerate(xDispNodeIndex):
            self.stiffnessMatrix[nodeIndex * 2, :] = zeroLine
            self.stiffnessMatrix[nodeIndex * 2, nodeIndex * 2] = 1
            self.loadVector[nodeIndex * 2] = xDisp[dispIndex]

        # consider y dislacements
        for dispIndex, nodeIndex in enumerate(yDispNodeIndex):
            self.stiffnessMatrix[nodeIndex * 2 + 1, :] = zeroLine
            self.stiffnessMatrix[nodeIndex * 2 + 1, nodeIndex * 2 + 1] = 1
            self.loadVector[nodeIndex * 2 + 1] = yDisp[dispIndex]

    def _reduceStiffnesMatrixAndLoadVector(self):
        """
        Reduces sitffness matrix and load vector based on fixated nodes
        """

        # Get index of nodes that are fixated
        xFixationNodeId = self.nodalDisplacements._getNodeIdsWithFixationX()  # fixated nodes in x
        xFixationNodeIndex = self.mesh.nodes.findIndexByNodeIds(xFixationNodeId)
        yFixationNodeId = self.nodalDisplacements._getNodeIdsWithFixationY()  # fixated nodes in y
        yFixationNodeIndex = self.mesh.nodes.findIndexByNodeIds(yFixationNodeId)

        # get number of degrees of freedom
        self.numberDOF = self.stiffnessMatrix.shape[0] - (xFixationNodeId.size + yFixationNodeId.size)

        # align reducable columns and rows in new list
        for index in xFixationNodeIndex:
            self.fixedDOF.append(index * 2)  # x-Direction
        for index in yFixationNodeIndex:
            self.fixedDOF.append(index * 2 + 1)  # y-Direction

        # Find the free DOF (those that are not fixed)
        self.openDOF = np.setdiff1d(np.arange(self.stiffnessMatrix.shape[0]), self.fixedDOF)

        # Create reduced stiffness matrix by deleting rows and columns
        self.reducedStiffnessMatrix = np.delete(self.stiffnessMatrix, self.fixedDOF, axis=0)
        self.reducedStiffnessMatrix = np.delete(self.reducedStiffnessMatrix, self.fixedDOF, axis=1)
        self.reducedLoadVector = np.delete(self.loadVector, self.fixedDOF, axis=0)

    def _solveLinearEquation(self):
        """
        Solves the linear FEM equation K*U=F by using inverse of K
        """
        start_time = time.perf_counter()

        #        if np.linalg.det(self.reducedStiffnessMatrix) <1E-300:
        #            raise ValueError("Global stiffness matrix appears to be close to singluar!\n"
        #                             "Check for faulty boundries, integration orders, unconnected nodes!")

        # solve the fem  equation
        self.reducedDisplacementVector = np.linalg.inv(self.reducedStiffnessMatrix) @ self.reducedLoadVector

        # transfer the reduced displacement vector to the comlete displacement vector
        self.displacementVector = np.zeros([self.stiffnessMatrix.shape[0], 1])
        self.displacementVector[self.openDOF, 0] = self.reducedDisplacementVector.flatten()

    def _getNodalSolution(self):
        """
        Return nodal solution and update deformed mesh
        """
        # Nodal displacements
        dispX = self.displacementVector[0::2]
        dispY = self.displacementVector[1::2]
        dispTotal = np.sqrt(dispX**2 + dispY**2)

        # Deformed mesh coordinates
        self.meshDeformed.nodes.coordinates = self.mesh.nodes.coordinates + np.hstack([dispX, dispY])

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
        self.mesh.elements.integrationpointIds = [[] for i in range(self.mesh.numberOfElements)]
        self.meshDeformed.elements.integrationpointIds = [[] for i in range(self.meshDeformed.numberOfElements)]
        self.mesh.integrationPoints.ids = np.arange(1, numberOfIntPoint + 1)
        self.meshDeformed.integrationPoints.ids = np.arange(1, numberOfIntPoint + 1)
        self.mesh.integrationPoints.coordinates = np.zeros([numberOfIntPoint, 2], np.float64)
        self.meshDeformed.integrationPoints.coordinates = np.zeros([numberOfIntPoint, 2], np.float64)

        curIntPointIndex = 0  # current integer point index (serves as a counter)

        # pre-allocation of element result arrays
        strainX = np.zeros([numberOfIntPoint, 1], np.float64)
        strainY = np.zeros([numberOfIntPoint, 1], np.float64)
        strainXY = np.zeros([numberOfIntPoint, 1], np.float64)
        stressX = np.zeros([numberOfIntPoint, 1], np.float64)
        stressY = np.zeros([numberOfIntPoint, 1], np.float64)
        stressZ = np.zeros([numberOfIntPoint, 1], np.float64)
        stressXY = np.zeros([numberOfIntPoint, 1], np.float64)
        stress11 = np.zeros([numberOfIntPoint, 1], np.float64)
        stress22 = np.zeros([numberOfIntPoint, 1], np.float64)
        stress33 = np.zeros([numberOfIntPoint, 1], np.float64)
        stressMises = np.zeros([numberOfIntPoint, 1], np.float64)

        # iterate trough each element and gather element result and integration point data
        for elementIndex, id in enumerate(self.mesh.elements.ids):
            nodeIds = self.mesh.elements.nodeIds[elementIndex]
            nodeCoords, nodeIndex = self.mesh.nodes.findCoordinatesByNodeIds(nodeIds)
            deformedCoords, nodeIndex = self.meshDeformed.nodes.findCoordinatesByNodeIds(nodeIds)
            nodeSize = nodeCoords.shape[0]
            order = self.mesh.elements.integrationOrder[elementIndex]
            E = self.mesh.elements.youngsModulus[elementIndex]
            nu = self.mesh.elements.poissonsRatio[elementIndex]
            t = self.mesh.elements.thickness[elementIndex]
            behaviour = self.mesh.elements.planarAssumption[elementIndex]

            # get guide vector to extract current DOFs
            g = self._getMatrixGuideVector(nodeIndex)

            # gauss points for which the element result is determined
            if nodeSize in [3, 6]:  # triangle
                gaussPoints = self._getTriaGaussPoint(order)
            elif nodeSize in [4, 8]:  # quad
                gaussPoints = self._getQuadGaussPoint(order)

            # element D matrix for stress results
            D = self._getElementDMatrix(E, nu, behaviour)

            # iterate trough all integration points of the elements
            for [xi, eta] in gaussPoints:
                B, detJ = self._getElementBMatrixandJacobiDeterminant(nodeCoords, xi, eta)

                # calculate strain and stress vector at current integration point
                strainVector = B @ self.displacementVector[g]
                stressVector = D @ B @ self.displacementVector[g]

                # extract scalars form strain and stress vector
                strainX[curIntPointIndex] = strainVector[0]
                strainY[curIntPointIndex] = strainVector[1]
                strainXY[curIntPointIndex] = strainVector[2]
                stressX[curIntPointIndex] = stressVector[0]
                stressY[curIntPointIndex] = stressVector[0]
                stressXY[curIntPointIndex] = stressVector[0]

                # create the full 3x3 stress tensor for principal stresses
                sigX = stressVector[0].item()
                sigY = stressVector[1].item()
                sigXY = stressVector[2].item()

                # determine stress in z direction bases on behaviour
                if behaviour.lower() in [0, "plane stress", "planestress", "stress"]:
                    sigZ = 0
                else:
                    sigZ = nu * (sigX + sigY)

                # 3x3 stress tensor
                stressTensor = np.array([[sigX, sigXY, 0], [sigXY, sigY, 0], [0, 0, sigZ]])

                stressZ[curIntPointIndex] = sigZ

                # calculate principal stresses (eigenvalues)
                eigenValues = np.linalg.eigvals(stressTensor)
                principalstresses = np.sort(eigenValues)[::-1]  # Sort in descending order
                sig1, sig2, sig3 = principalstresses

                stress11[curIntPointIndex] = sig1
                stress22[curIntPointIndex] = sig2
                stress33[curIntPointIndex] = sig3

                # calculate mises stress
                misesstress = np.sqrt(0.5 * ((sig1 - sig2) ** 2 + (sig2 - sig3) ** 2 + (sig3 - sig1) ** 2))
                stressMises[curIntPointIndex] = misesstress

                # assign integration point ids to element
                self.mesh.elements.integrationpointIds[elementIndex].append(curIntPointIndex + 1)
                self.meshDeformed.elements.integrationpointIds[elementIndex].append(curIntPointIndex + 1)

                # calculate integration point coordinates for mesh and deformed mesh
                self.mesh.integrationPoints.coordinates[curIntPointIndex, :] = self._getIntegrationPointsCoordinates(nodeCoords, xi, eta)
                self.meshDeformed.integrationPoints.coordinates[curIntPointIndex, :] = self._getIntegrationPointsCoordinates(deformedCoords, xi, eta)

                # update current integration point index
                curIntPointIndex = curIntPointIndex + 1

        # combine nodal solutions
        nodalSolution = (np.array(dispX), np.array(dispY), np.array(dispTotal))

        # combine element solutions
        elementSolution = (
            np.array(strainX),
            np.array(strainY),
            np.array(strainXY),
            np.array(stressX),
            np.array(stressY),
            np.array(stressXY),
            np.array(stress11),
            np.array(stress22),
            np.array(stress33),
            np.array(stressMises),
            np.array(stressMises),
        )

        return nodalSolution, elementSolution
