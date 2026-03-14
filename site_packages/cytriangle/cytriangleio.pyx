from libc.stdlib cimport free, malloc
import numpy as np
from cytriangle.ctriangle cimport triangulateio


def validate_input_attributes(attributes):
    num_attr = list(set([len(sublist) for sublist in attributes]))
    if len(num_attr) > 1:
        raise ValueError(
            "Attribute lists must have the same number of attributes for each element"
        )
    return num_attr[0]


def validate_attribute_number(attributes, base_quantity):
    if len(attributes) != base_quantity:
        raise ValueError(
            """Attribute list must have the same number of elements as the
            input it decorates"""
        )


cdef class TriangleIO:

    def __cinit__(self):
        # Initialize the triangulateio struct with NULL pointers
        self._io = <triangulateio*> NULL

    def __dealloc__(self):
        # Free allocated memory when the instance is deallocated
        if self._io is not NULL:
            # add all the allocation releases
            if self._io.pointlist is not NULL:
                free(self._io.pointlist)
            if self._io.pointattributelist is not NULL:
                free(self._io.pointattributelist)
            if self._io.pointmarkerlist is not NULL:
                free(self._io.pointmarkerlist)
            if self._io.trianglelist is not NULL:
                free(self._io.trianglelist)
            if self._io.triangleattributelist is not NULL:
                free(self._io.triangleattributelist)
            if self._io.trianglearealist is not NULL:
                free(self._io.trianglearealist)
            if self._io.neighborlist is not NULL:
                free(self._io.neighborlist)
            if self._io.segmentlist is not NULL:
                free(self._io.segmentlist)
            if self._io.segmentmarkerlist is not NULL:
                free(self._io.segmentmarkerlist)
            if self._io.holelist is not NULL:
                free(self._io.holelist)
            if self._io.regionlist is not NULL:
                free(self._io.regionlist)
            if self._io.edgelist is not NULL:
                free(self._io.edgelist)
            if self._io.edgemarkerlist is not NULL:
                free(self._io.edgemarkerlist)
            if self._io.normlist is not NULL:
                free(self._io.normlist)
            free(self._io)

    def __init__(self, input_dict=None):
        # Assemble the triangulateio struct from a Python dictionary (default)
        self._io = <triangulateio*> malloc(sizeof(triangulateio))

        # Allocate null fields
        self._io.pointlist = <double*> NULL
        self._io.numberofpoints = 0

        self._io.pointattributelist = <double*> NULL
        self._io.numberofpointattributes = 0
        self._io.pointmarkerlist = <int*> NULL

        self._io.trianglelist = <int*> NULL
        self._io.numberoftriangles = 0
        self._io.numberofcorners = 0
        self._io.numberoftriangleattributes = 0
        self._io.triangleattributelist = <double*> NULL
        self._io.trianglearealist = <double*> NULL
        self._io.neighborlist = <int*> NULL

        # input - p switch
        self._io.segmentlist = <int*> NULL
        self._io.segmentmarkerlist = <int*> NULL
        self._io.numberofsegments = 0

        # input - p switch without r
        self._io.holelist = <double*> NULL
        self._io.numberofholes = 0
        self._io.regionlist = <double*> NULL
        self._io.numberofregions = 0

        # input - always ignored
        self._io.edgelist = <int*> NULL
        self._io.edgemarkerlist = <int*> NULL
        self._io.normlist = <double*> NULL
        self._io.numberofedges = 0

        # Populate based on input_dict
        if input_dict is not None:
            if 'vertices' in input_dict:
                self.set_vertices(input_dict['vertices'])
                # set other vertex related optional fields
                if 'vertex_attributes' in input_dict:
                    self.set_vertex_attributes(input_dict['vertex_attributes'])
                if 'vertex_markers' in input_dict:
                    self.set_vertex_markers(input_dict['vertex_markers'])
            if 'triangles' in input_dict:
                # fetch number of corners from triangle input
                self._io.numberofcorners = len(input_dict['triangles'][0])
                self.set_triangles(input_dict['triangles'])
                if 'triangle_attributes' in input_dict:
                    self.set_triangle_attributes(input_dict['triangle_attributes'])
                if 'triangle_max_area' in input_dict:
                    self.set_triangle_areas(input_dict['triangle_max_area'])
            if 'segments' in input_dict:
                self.set_segments(input_dict['segments'])
                if 'segment_markers' in input_dict:
                    self.set_segment_markers(input_dict['segment_markers'])
            if 'holes' in input_dict:
                self.set_holes(input_dict['holes'])
            if 'regions' in input_dict:
                self.set_regions(input_dict['regions'])

    def to_dict(self, opt=''):
        """
        Converts the internal C TriangleIO data structure into a dictionary format.

        Parameters:
        - opt: A string that indicates the format of the output. If 'np',
          numpy arrays are used.

        Returns:
        - A dictionary containing the triangulation data.
        """
        output_dict = {}

        if opt == 'np':
            if self.vertices:
                output_dict['vertices'] = np.asarray(self.vertices)
            if self.vertex_attributes:
                output_dict['vertex_attributes'] = np.asarray(self.vertex_attributes)
            if self.vertex_markers:
                output_dict['vertex_markers'] = np.asarray(self.vertex_markers)
            if self.triangles:
                output_dict['triangles'] = np.asarray(self.triangles)
            if self.triangle_attributes:
                output_dict['triangle_attributes'] = np.asarray(
                    self.triangle_attributes)
        else:
            if self.vertices:
                output_dict['vertices'] = self.vertices
            if self.vertex_attributes:
                output_dict['vertex_attributes'] = self.vertex_attributes
            if self.vertex_markers:
                output_dict['vertex_markers'] = self.vertex_markers
            if self.triangles:
                output_dict['triangles'] = self.triangles
            if self.triangle_attributes:
                output_dict['triangle_attributes'] = self.triangle_attributes
        if self.triangle_max_area:
            output_dict['triangle_max_area'] = self.triangle_max_area
        if self.neighbors:
            output_dict['neighbors'] = self.neighbors
        if self.segments:
            output_dict['segments'] = self.segments
        if self.segment_markers:
            output_dict['segment_markers'] = self.segment_markers
        if self.holes:
            output_dict['holes'] = self.holes
        if self.regions:
            output_dict['regions'] = self.regions
        if self.edges:
            output_dict['edges'] = self.edges
        if self.edge_markers:
            output_dict['edge_markers'] = self.edge_markers
        if self.norms:
            output_dict['norms'] = self.norms

        return output_dict

    @property
    def vertices(self):
        """
        `vertices`:  A list of pairs [x, y] that are vertex coordinates.

        Returns:
        - A list of pairs [x, y] that are vertex coordinates.
        """
        if self._io.pointlist is not NULL:
            return [[self._io.pointlist[2*i], self._io.pointlist[2*i + 1]]
                    for i in range(self._io.numberofpoints)]

    @vertices.setter
    def vertices(self, vertices):
        self.set_vertices(vertices)

    @property
    def vertex_attributes(self):
        """
        `vertex_attributes`: An list of lists of vertex attributes (floats).
        Each vertex must have the same number of attributes, and
        len(vertex_attributes) must match the number of points.

        Returns:
        - A list of lists, where each inner list contains attributes for a vertex.
        """
        if self._io.pointattributelist is not NULL:
            vertex_attributes = []
            for i in range(self._io.numberofpoints):
                vertex_attr = []
                for j in range(self._io.numberofpointattributes):
                    vertex_attr.append(
                        self._io.pointattributelist[
                            i*self._io.numberofpointattributes + j
                        ]
                    )
                vertex_attributes.append(vertex_attr)
            return vertex_attributes

    @vertex_attributes.setter
    def vertex_attributes(self, vertex_attributes):
        self.set_vertex_attributes(vertex_attributes)

    @property
    def vertex_markers(self):
        """
        `vertex_markers`: A list of vertex markers; one int per point.

        Returns:
        - A list of integers representing markers for each vertex.
        """
        if self._io.pointmarkerlist is not NULL:
            return [self._io.pointmarkerlist[i] for i in range(self._io.numberofpoints)]

    @vertex_markers.setter
    def vertex_markers(self, vertex_markers):
        self.set_vertex_markers(vertex_markers)

    @property
    def triangles(self):
        """
        `triangles`: A list of triangle corners (not necessarily 3).
        Corners are designated in a counterclockwise order,
        followed by any other nodes if the triangle represents a
        nonlinear element (e.g. num_corners > 3).

        Returns:
        - A list of lists, where each inner list contains vertex indices for a triangle.
        """
        if self._io.trianglelist is not NULL:
            triangles = []
            for i in range(self._io.numberoftriangles):
                tri_order = []
                for j in range(self._io.numberofcorners):
                    tri_order.append(self._io.trianglelist[
                        i * self._io.numberofcorners + j
                    ])
                triangles.append(tri_order)
            return triangles

    @triangles.setter
    def triangles(self, triangles):
        self.set_triangles(triangles)

    @property
    def triangle_attributes(self):
        """
        `triangle_attributes`: A list of triangle attributes. Each triangle must have
        the same number of attributes.

         Returns:
        - A list of lists, where each inner list contains attributes for a triangle.
        """
        if self._io.triangleattributelist is not NULL:
            triangle_attributes = []
            for i in range(self._io.numberoftriangles):
                triangle_attr = []
                for j in range(self._io.numberoftriangleattributes):
                    triangle_attr.append(
                        self._io.triangleattributelist[
                            i*self._io.numberoftriangleattributes + j
                        ]
                    )
                triangle_attributes.append(triangle_attr)
            return triangle_attributes

    @triangle_attributes.setter
    def triangle_attributes(self, triangle_attributes):
        self.set_triangle_attributes(triangle_attributes)

    @property
    def triangle_max_area(self):
        """
        `triangle_max_area`: A list of triangle area constraints;
        one per triangle, 0 if not set.
        Input only.

        Returns:
        - A list of floats representing the maximum area for each triangle.
        """
        if self._io.trianglearealist is not NULL:
            return [self._io.trianglearealist[i]
                    for i in range(self._io.numberoftriangles)]

    @triangle_max_area.setter
    def triangle_max_area(self, triangle_areas):
        self.set_triangle_areas(triangle_areas)

    @property
    def neighbors(self):
        """
        `neighbors`: A list of triangle neighbors; three ints per triangle. Output only.

        Returns:
        - A list of lists, where each inner list contains indices of neighboring
          triangles.
        """
        max_neighbors = 3
        if self._io.neighborlist is not NULL:
            neighbor_list = []
            for i in range(self._io.numberoftriangles):
                neighbors = [self._io.neighborlist[i*max_neighbors + j]
                             for j in range(max_neighbors)]
                # remove sentinel values (-1)
                neighbors = [neighbor for neighbor in neighbors if neighbor != -1]
                neighbor_list.append(neighbors)
            return neighbor_list

    @property
    def segments(self):
        """
        `segments`: A list of segment endpoints.

        Returns:
        - A list of lists, where each inner list contains vertex indices for
        a segment.
        """
        if self._io.segmentlist is not NULL:
            segments = []
            for i in range(self._io.numberofsegments):
                start_pt_index = self._io.segmentlist[2 * i]
                end_pt_index = self._io.segmentlist[2 * i + 1]
                segments.append([start_pt_index, end_pt_index])
            return segments

    @segments.setter
    def segments(self, segments):
        self.set_segments(segments)

    @property
    def holes(self):
        """
        `holes`: A list of hole coordinates.

        Returns:
        - A list of pairs [x, y] representing coordinates of holes.
        """
        if self._io.holelist is not NULL:
            return [[self._io.holelist[2*i], self._io.holelist[2*i + 1]]
                    for i in range(self._io.numberofholes)]

    @holes.setter
    def holes(self, holes):
        self.set_holes(holes)

    # unmarked segments have a value of 0
    @property
    def segment_markers(self):
        """
        `segment_markers`:  An array of segment markers; one int per segment.

        Returns:
        - A list of integers representing markers for each segment.
        """
        if self._io.segmentmarkerlist is not NULL:
            segment_markers = []
            for i in range(self._io.numberofsegments):
                segment_markers.append(self._io.segmentmarkerlist[i])
            return segment_markers

    @segment_markers.setter
    def segment_markers(self, segment_markers):
        self.set_segment_markers(segment_markers)

    @property
    def regions(self):
        """
        `regions`: An array of regional attributes and area constraints. Note that
        each regional attribute is used only if you select the `A` switch, and each area
        constraint is used only if you select the `a` switch (with no number following).

        Returns:
        - A list of dictionaries, each containing 'vertex' (coordinates of the region's
        vertex), 'marker' (integer marker for the region), and 'max_area' (maximum area
        constraint for the region).
        """
        if self._io.regionlist is not NULL:
            regions = []
            for i in range(self._io.numberofregions):
                region = {}
                region['vertex'] = [self._io.regionlist[4*i],
                                    self._io.regionlist[4*i + 1]]
                region['marker'] = int(self._io.regionlist[4*i + 2])
                region['max_area'] = self._io.regionlist[4*i + 3]
                regions.append(region)
            return regions

    @regions.setter
    def regions(self, regions):
        self.set_regions(regions)

    @property
    def edges(self):
        """
        `edges`: An array of edge endpoints. The first edge's endpoints are at
        indices [0] and [1], followed by the remaining edges. Two ints per
        edge. Output only.

        Returns:
        - A list of lists, where each inner list contains vertex indices for an edge.
        """
        if self._io.edgelist is not NULL:
            edges = []
            for i in range(self._io.numberofedges):
                edges.append([self._io.edgelist[i * 2], self._io.edgelist[i * 2 + 1]])
            return edges

    @property
    def edge_markers(self):
        """
        `edge_markers`: An array of edge markers; one int per edge. Output only.

        Returns:
        - A list of integers representing markers for each edge.
        """
        if self._io.edgemarkerlist is not NULL:
            return [self._io.edgemarkerlist[i] for i in range(self._io.numberofedges)]

    @property
    def norms(self):
        """
        `norms`: An array of normal vectors, used for infinite rays in Voronoi
        diagrams. For each finite edge in a Voronoi diagram, the normal vector written
        is the zero vector. Output only.

        Returns:
        - A list of dictionaries, each containing 'ray_origin' (start
        point of the ray) and 'ray_direction' (direction of the ray),
        represented as [x, y] pairs.
        """
        if self._io.normlist is not NULL:
            norm_list = []
            for i in range(self._io.numberofedges):
                norm_list.append({'ray_origin': [self._io.normlist[i * 4],
                                                 self._io.normlist[i * 4 + 1]],
                                  'ray_direction': [self._io.normlist[i * 4 + 2],
                                                    self._io.normlist[i * 4 + 3]]})
            return norm_list

    def set_vertices(self, vertices):
        num_vertices = len(vertices)
        self._io.numberofpoints = num_vertices
        if num_vertices < 3:
            raise ValueError('Valid input requires three or more vertices')
        vertices = np.ascontiguousarray(vertices)
        self._io.pointlist = <double*>malloc(2 * num_vertices * sizeof(double))
        for i in range(num_vertices):
            self._io.pointlist[2 * i] = vertices[i, 0]
            self._io.pointlist[2 * i + 1] = vertices[i, 1]

    def set_vertex_attributes(self, vertex_attributes):
        num_attr = validate_input_attributes(vertex_attributes)
        num_vertices = self._io.numberofpoints
        validate_attribute_number(vertex_attributes, num_vertices)
        vertex_attributes = np.ascontiguousarray(vertex_attributes)
        self._io.pointattributelist = <double*>malloc(
            num_attr * num_vertices * sizeof(double))
        self._io.numberofpointattributes = num_attr
        for i in range(num_vertices):
            for j in range(num_attr):
                self._io.pointattributelist[i * num_attr + j] = vertex_attributes[i, j]

    def set_vertex_markers(self, vertex_markers):
        vertex_markers = np.ascontiguousarray(vertex_markers, dtype=int)
        self._io.pointmarkerlist = <int*>malloc(len(vertex_markers) * sizeof(int))
        for i in range(len(vertex_markers)):
            self._io.pointmarkerlist[i] = vertex_markers[i]

    def set_triangles(self, triangles):
        num_triangles = len(triangles)
        num_corners = self._io.numberofcorners
        triangles = np.ascontiguousarray(triangles, dtype=int)
        self._io.trianglelist = <int*>malloc(num_triangles * num_corners * sizeof(int))
        self._io.numberoftriangles = num_triangles
        for i in range(num_triangles):
            for j in range(num_corners):
                self._io.trianglelist[i*num_corners + j] = triangles[i, j]

    def set_triangle_attributes(self, triangle_attributes):
        num_attr = validate_input_attributes(triangle_attributes)
        num_triangles = self._io.numberoftriangles
        validate_attribute_number(triangle_attributes, num_triangles)
        triangle_attributes = np.ascontiguousarray(triangle_attributes)
        self._io.triangleattributelist = <double*>malloc(
            num_attr * num_triangles * sizeof(double))
        self._io.numberoftriangleattributes = num_attr
        for i in range(num_triangles):
            for j in range(num_attr):
                self._io.triangleattributelist[
                    i * num_attr + j] = triangle_attributes[i, j]

    def set_triangle_areas(self, triangle_areas):
        num_triangles = self._io.numberoftriangles
        validate_attribute_number(triangle_areas, num_triangles)
        triangle_max_area = np.ascontiguousarray(triangle_areas)
        self._io.trianglearealist = <double*>malloc(num_triangles * sizeof(double))
        for i in range(num_triangles):
            self._io.trianglearealist[i] = triangle_max_area[i]

    def set_segments(self, segments):
        num_segments = len(segments)
        self._io.numberofsegments = num_segments
        segments = np.ascontiguousarray(segments, dtype=int)
        self._io.segmentlist = <int*>malloc(num_segments * 2 * sizeof(int))
        for i in range(num_segments):
            self._io.segmentlist[i * 2] = segments[i, 0]
            self._io.segmentlist[i * 2 + 1] = segments[i, 1]

    def set_segment_markers(self, segment_markers):
        segment_markers = np.ascontiguousarray(segment_markers, dtype=int)
        validate_attribute_number(segment_markers, self._io.numberofsegments)
        self._io.segmentmarkerlist = <int*>malloc(
            self._io.numberofsegments * sizeof(int))
        for i in range(self._io.numberofsegments):
            self._io.segmentmarkerlist[i] = segment_markers[i]

    def set_holes(self, holes):
        num_holes = len(holes)
        self._io.numberofholes = num_holes
        holes = np.ascontiguousarray(holes)
        self._io.holelist = <double*>malloc(num_holes * 2 * sizeof(double))
        for i in range(num_holes):
            self._io.holelist[2 * i] = holes[i, 0]
            self._io.holelist[2 * i + 1] = holes[i, 1]

    def set_regions(self, regions):
        num_regions = len(regions)
        self._io.numberofregions = num_regions
        # unpack region dict
        region_array = [[region['vertex'][0],
                         region['vertex'][1],
                         region['marker'],
                         region['max_area']]
                        for region in regions]
        regions = np.ascontiguousarray(region_array)
        self._io.regionlist = <double*>malloc(num_regions * 4 * sizeof(double))
        for i in range(num_regions):
            for j in range(4):
                self._io.regionlist[i * 4 + j] = regions[i, j]
