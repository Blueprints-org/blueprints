from matplotlib import pyplot as plt

from blueprints.utils.femlearn.boundary_conditions import Boundaries, DisplacementOnPoints
from blueprints.utils.femlearn.geometry import Geometry
from blueprints.utils.femlearn.loads import Loads, LoadsOnPoints
from blueprints.utils.femlearn.mesh import Mesh
from blueprints.utils.femlearn.solution import Solution
from blueprints.utils.femlearn.solver_data import SolverData


class Model2d:
    """
    Model class that holds all data for a 2D FEM model.
    """

    def __init__(self, geometry=Geometry(), mesh=Mesh(), boundaries=Boundaries(), loads=Loads(), solverData=SolverData(), solution=Solution()):
        self.geometry = geometry
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
        # print("Check model parameters:")

        if not (
            self.mesh.elements.ids.shape[0]
            == len(self.mesh.elements.nodeIds)
            == self.mesh.elements.youngsModulus.shape[0]
            == self.mesh.elements.poissonsRatio.shape[0]
            == self.mesh.elements.thickness.shape[0]
            == self.mesh.elements.integrationOrder.shape[0]
        ):
            raise ValueError("Elements not correctly defined!")
        if not (self.mesh.nodes.ids.shape[0] == self.mesh.nodes.coordinates.shape[0]):
            raise ValueError("Nodes not correctly defined!")
        if self.mesh.numberOfElements == 0 or self.mesh.numberOfNodes == 0:
            raise ValueError("Empty mesh!")

        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] != 0:
                raise ValueError("No points were defined for lines!")
            if self.boundaries.displacementOnPoints.ids.shape[0] != 0:
                raise ValueError("No points were defined for displacement on points!")

        if self.geometry.lines.ids.shape[0] == 0:
            if self.boundaries.displacementOnLines.ids.shape[0] != 0:
                raise ValueError("No points were defined for displacement on lines!")

    def generateQuadMesh(
        self, nx=1, ny=1, type=4, specified_nodes=None, integrationOrder=4, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]
    ):
        """Generates a Quad mesh for a rectangle

        Args:
            nx (int): Number of nodes in x direction
            ny (int): Number of nodes in y direction
            type (str, optional): "Quad4" or "Quad8". Defaults to 'Quad4'.
            specified_nodes (array, optional): Specify coordinates where aditional nodes should be placed . Defaults to None.
        """
        if type in ["Quad4", 4]:
            xmin = np.min(self.geometry.points.x)
            xmax = np.max(self.geometry.points.x)
            ymin = np.min(self.geometry.points.y)
            ymax = np.max(self.geometry.points.y)
            x = np.linspace(xmin, xmax, nx)
            y = np.linspace(ymin, ymax, ny)
            # Füge spezifische nodes hinzu die in specified_nodes angegeben sind
            # Wird vor allem für die mesh_polygon funktion gebraucht
            if specified_nodes is not None:
                x = np.union1d(x, specified_nodes[:, 0])
                nx = x.size
                y = np.union1d(y, specified_nodes[:, 1])
                ny = y.size
            xx, yy = np.meshgrid(x, y)
            self.mesh.nodes = Nodes(np.vstack([xx.ravel(), yy.ravel()]).T)
            # self.mesh.nodes.setIds(self.mesh.nodes.ids)

            connectivity = []

            # Schleife über alle elemente, bei jedem element alle vier knoten die dazugehören berechnen
            for i in range(ny - 1):  # durch zeilen iterieren; n knoten in x richting => n-1 elemente in x richtung
                for j in range(nx - 1):  # durch spalten iterieren
                    n0 = i * (nx) + j + 1
                    # erklärung für n0: i * (nx) => Erster knoten in der Zeile + j => die jeweilige spalte
                    n1 = n0 + 1  # 1 nach rechts von n0
                    n3 = n0 + nx  # zuers n3 alos oben links berechen
                    n2 = n3 + 1  # 1 nach rechts von n3
                    connectivity.append([n0, n1, n2, n3])
            connectivity = np.array(connectivity)
            self.mesh.elements = Elements(
                nodeIds=connectivity, thickness=thickness, youngsModulus=youngsModulus, poissonsRatio=poissonRation, planarAssumption=planarAssumption
            )
        elif type in ["Quad8", 8]:
            raise ("Quad8 not supportet yet")

        self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])

    def generateTriangleMesh(self, size, type=3, integrationOrder=1, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]):
        """Creates a triangle mesh using the pygmsh library

        Args:
            size (float): element size
            type (int, optional): type of the element 3=>tria3; 6 => tria6. Defaults to 3.
            integrationOrder (int,optional): number of integration points per element. Deaults to 4
        """
        import pygmsh  # externe meshing bibliothek

        vertices = self.geometry.points.coordinates
        with blueprints.utils.femlearn.geometry.Geometry() as pygeom:
            pygeom.add_polygon(
                vertices,
                mesh_size=size,
            )

            if type == 3:
                keyType = 1
            elif type == 6:
                keyType = 2
            else:
                raise ValueError(f"Type TRIA-{type} not implemented!")

            gmsh = pygeom.generate_mesh(order=keyType)
            keys = ["triangle", "triangle6", "triangle10"]
            connectivity = np.array(gmsh.cells_dict[keys[keyType - 1]]) + 1
            points = np.array(gmsh.points)
            self.mesh.nodes = Nodes(coordinates=points[:, [0, 1]])
            self.mesh.nodes.setIds(self.mesh.nodes.ids)

            self.mesh.elements = Elements(
                nodeIds=connectivity, thickness=thickness, youngsModulus=youngsModulus, poissonsRatio=poissonRation, planarAssumption=planarAssumption
            )
            self.mesh.elements.setIds(self.mesh.elements.ids)
            self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])
            pass

    def importNasFile(self, filename, integrationOrder=1, thickness=[], poissonRation=[], youngsModulus=[], planarAssumption=[]):
        from pyNastran.bdf.bdf import BDF

        model = BDF()

        model.read_bdf(filename, xref=False)

        coords = model.get_xyz_in_coord()[:, [0, 2]]
        all_node_ids = list(model.node_ids)
        number_of_node = model.nnodes

        # nodeIDs = np.array([model.get_node_ids_with_elements([i],return_array=True) for i in model.element_ids])
        nodeIDs = np.array([model.elements[i].node_ids for i in model.element_ids])

        if nodeIDs.shape[1] not in [3, 4, 6, 8]:
            # If elements have Three nodes, the colummns are already in the correct order
            raise ("Import is only implemented for elements of type: {Tria3;Tria3; Quad4; Quad8}")

        self.mesh.nodes = Nodes(coordinates=coords, ids=all_node_ids)
        self.mesh.elements = Elements(
            nodeIds=nodeIDs, thickness=thickness, youngsModulus=youngsModulus, poissonsRatio=poissonRation, planarAssumption=planarAssumption
        )
        self.mesh.elements.integrationOrder = np.array([integrationOrder for _ in range(self.mesh.numberOfElements)])

    def solve(self):
        """
        Assemble the equation matrices from mesh, boundaries and load definitions and solve them
        """
        self._checkParameters()
        start_time = time.perf_counter()
        self.meshDeformed = copy.deepcopy(self.mesh)
        self.solverData = SolverData(self.mesh, self.meshDeformed)
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
        self.solution = Solution(
            self.mesh,
            self.meshDeformed,
            nodalSolution[0],
            nodalSolution[1],
            nodalSolution[2],
            elementSolution[0],
            elementSolution[1],
            elementSolution[2],
            elementSolution[3],
            elementSolution[4],
            elementSolution[5],
            elementSolution[6],
            elementSolution[7],
            elementSolution[8],
            elementSolution[9],
            elementSolution[10],
        )
        pass

    def plotSolution(self, variableName, averaged=False, deformed=True):
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
            if variableName[:4] != "disp":
                averagedResult = self.solution._getAveragedResult(variableName)

            # Iterate through all elements by iterating through the nodeIDs vector
            for index, nodeIds in enumerate(self.mesh.elements.nodeIds):
                # Get the the deformed coordinates of the nodes belonging to the current element
                # If elementtype is TRIA6: use only first three coordinates for plotting
                if len(nodeIds) == 6:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds[[0, 3, 1, 4, 2, 5]])
                # If elementtype is Quad8: use only first four coordinates for plotting
                elif len(nodeIds) == 8:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds[[0, 4, 1, 5, 2, 6, 3, 7]])
                else:
                    elementNodeIndex = self.mesh.nodes.findIndexByNodeIds(nodeIds)
                element_coords = coords[elementNodeIndex]

                # If the variable is a deformation, the average is calculated inside the loop.
                # This way the "nodeIDs" that were calculated via "findIndexByNodeIds()" can be reused
                if variableName[:4] == "disp":
                    # Get the average deformation of the nodes belonging to the urrent element
                    average_variable = variable[
                        elementNodeIndex
                    ].mean()  # nodeIds can be used since deformations are stored in the same order as the nodes
                else:
                    average_variable = averagedResult[index]

                # map deformation to colormap
                cmap = plt.get_cmap("jet")
                color = cmap((average_variable - var_min) / (var_max - var_min))

                ax.fill(element_coords[:, 0], element_coords[:, 1], edgecolor="cyan", facecolor=color)
                ax.set_aspect("equal", adjustable="box")

        # If averaged = false
        else:
            if variableName[:4] != "disp":
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
            cmap = plt.get_cmap("jet")
            color = cmap((variable - var_min) / (var_max - var_min))

            plt.scatter(coords[:, 0], coords[:, 1], c=color, s=150)
            mesh.plotMesh()
            ax.set_aspect("equal", adjustable="box")

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=var_min, vmax=var_max))
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax)
        cbar.set_label(variableName)
        return fig

    def plotBoundaries(self, deformed=False):
        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] != 0:
                raise ValueError("No points were defined for lines!")
            if self.boundaries.displacementOnPoints.ids.shape[0] != 0:
                raise ValueError("No points were defined for displacement on points!")
            if self.loads.loadsOnPoints.ids.shape[0] != 0:
                raise ValueError("No points were defined for loads on points!")

        if self.geometry.lines.ids.shape[0] == 0:
            if self.boundaries.displacementOnLines.ids.shape[0] != 0:
                raise ValueError("No points were defined for displacement on lines!")
            if self.loads.loadsOnLines.ids.shape[0] != 0:
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

        plt.scatter(x_fixed_coords[:, 0], x_fixed_coords[:, 1], marker=5, s=100, c="magenta", label="x fixed")
        plt.scatter(y_fixed_coords[:, 0], y_fixed_coords[:, 1], marker=6, s=100, c="lime", label="y fixed")

        # Adjust markers based on displacement direction
        x_displacement_markers = []
        for value in x_displacement_values:
            if isinstance(value, (int, float)):
                if value < 0:
                    x_displacement_markers.append("$\\leftarrow$")
                elif value > 0:
                    x_displacement_markers.append("$\\rightarrow$")
                else:
                    x_displacement_markers.append("")  # For zero
            else:
                x_displacement_markers.append("")  # For None string values

        y_displacement_markers = []
        for value in y_displacement_values:
            if isinstance(value, (int, float)):
                if value < 0:
                    y_displacement_markers.append("$\\downarrow$")
                elif value > 0:
                    y_displacement_markers.append("$\\uparrow$")
                else:
                    y_displacement_markers.append("")  # For zero
            else:
                y_displacement_markers.append("")  # For None or string values

        for i, (x, y) in enumerate(x_displacement_coords):
            plt.scatter(x, y, marker=x_displacement_markers[i], s=100, c="magenta")

        for i, (x, y) in enumerate(y_displacement_coords):
            plt.scatter(x, y, marker=y_displacement_markers[i], s=100, c="lime")

        plt.axis("square")

    def plotLoads(self, deformed=False):
        if self.geometry.points.ids.shape[0] == 0:
            if self.geometry.lines.ids.shape[0] != 0:
                raise ValueError("No points were defined for lines!")
            if self.loads.loadsOnPoints.ids.shape[0] != 0:
                raise ValueError("No points were defined for loads on points!")

        if self.geometry.lines.ids.shape[0] == 0:
            if self.loads.loadsOnLines.ids.shape[0] != 0:
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
        x_force_markers = ["$\\Leftarrow$" if value < 0 else "$\\Rightarrow$" for value in x_force_values]
        y_force_markers = ["$\\Downarrow$" if value < 0 else "$\\Uparrow$" for value in y_force_values]

        for i, (x, y) in enumerate(x_force_coords):
            plt.scatter(x, y, marker=x_force_markers[i], s=150, c="magenta")

        for i, (x, y) in enumerate(y_force_coords):
            plt.scatter(x, y, marker=y_force_markers[i], s=150, c="lime")

        plt.axis("square")

    def plotMesh(self, deformed=False, color_test=False, show_ids=False):
        """
        Plots the mesh

        Parameters:
        color_test (bool) -- ???
        show_ids (bool) -- True to displays node identifiers
        """
        if deformed:
            self.meshDeformed.plotMesh(color_test=color_test, show_ids=show_ids)
        else:
            self.mesh.plotMesh(color_test=color_test, show_ids=show_ids)

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


if __name__ == "__main__":
    model = Model2d()

    # Create geometry
    model.geometry.makePolygon(coordinates=[[0, 0], [20, 0], [20, 4], [0, 10]])

    model.geometry.plot()
    plt.show()

    # Meshing
    model.generateTRIAngleMesh(size=2, type=6, integrationOrder=3, thickness=1, poissonRation=0.3, youngsModulus=100, planarAssumption="plane stress")

    # Boundary conditions
    disp = DisplacementOnPoints(displacements=[[0, 0], [0, "free"]], pointIds=[1, 4])
    model.boundaries.setDisplacementOnPoints(disp)

    # Loads
    loads = LoadsOnPoints(loads=[[0, -10]], pointIds=[2])
    model.loads.setLoadsOnPoints(loads)

    model.solve()

    # Y-displacement in deformed mesh with loads and BCs
    model.plotSolution("dispY", averaged=True, deformed=True)
    model.plotBoundaries(deformed=True)
    model.plotLoads(deformed=True)
    plt.show()

    # Mises stress in undeformed mesh
    model.plotSolution("stressMises", averaged=False, deformed=False)
    model.plotMesh(deformed=False)
    model.plotBoundaries(deformed=False)
    model.plotLoads(deformed=False)
    plt.show()
