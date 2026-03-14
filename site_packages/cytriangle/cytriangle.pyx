from cytriangle.ctriangle cimport triangulate as ctriangulate
from cytriangle.cytriangleio  cimport TriangleIO
import re

cdef class CyTriangle:
    """
    A class to represent the input, output, and voronoi output (optional) of a
    triangulation action

    Attributes
    ----------
    in_ : TriangleIO
        input object to be triangulated
    out : TriangleIO
        output object of the triangulation (null initially, and if no triangulation
        is run)
    vorout: TriangleIO
        voronoi output object of triangulation (null initially, and if no triangulation
        is run, and if -v switch is not included in triangulate options)

    Methods
    -------
    input_dict(opt=""):
        Returns a dictionary representation of the triangulation input.
    output_dict(opt=""):
        Returns a dictionary representation of the triangulation output.
    voronoi_dict(opt=""):
        Returns a dictionary representation of the triangulation voronoi output.
    validate_input_flags(opts=""):
        Checks validity of flag options to avoid obvious incompatibilities between
        flags provided.
    triangulate(triflags=""):
        Computes the triangulation  on the input object with -Qz and user input flags.
    delaunay():
        Runs the triangulate method on the input object with -Qz flags.
    convex_hull():
       Runs the triangulate method on the input object with the -Qzc flags.
    voronoi():
       Runs the triangulate method on the input object with the -Qzc flags.

    """
    cdef TriangleIO _in
    cdef TriangleIO _out
    cdef TriangleIO _vorout

    def __init__(self, input_dict=None):
        if input_dict is not None:
            self._in = TriangleIO(input_dict)
        else:
            self._in = TriangleIO()
        self._out = TriangleIO()
        self._vorout = TriangleIO()

    @property
    def in_(self):
        return self._in

    @property
    def out(self):
        return self._out

    @property
    def vorout(self):
        return self._vorout

    def input_dict(self, opt=''):
        return self._in.to_dict(opt)

    def output_dict(self, opt=''):
        return self._out.to_dict(opt)

    def voronoi_dict(self, opt=''):
        return self._vorout.to_dict(opt)

    def validate_input_flags(self, opts):
        if "r" in opts:
            if 'triangles' not in self._in.to_dict():
                raise ValueError("Triangle list must be provided when using 'r' flag")
        if "p" in opts:
            if 'segments' not in self._in.to_dict():
                raise ValueError("Segment list must be provided when using 'p' flag")
        if "a" in opts:
            if not ('triangle_max_area' in self._in.to_dict() or 'A'
                    in opts or bool(re.search(r'a[\d.*.]+\d.*', opts))):
                raise ValueError("""When using 'a' flag for area constraints, a global
                                 area flag (e.g. a0.2), 'A' flag, or local triangle area
                                 constraint list (e.g. [3.0, 1.0]) must be provided""")
        if "q" in opts:
            if not bool(re.search(r'q[\d.*.]+\d.*', opts)):
                raise ValueError("""When using 'q' flag for minimum angles, an angle
                                 must be provided""")

    # generic triangulation that accepts any switch
    cpdef triangulate(self, triflags='', verbose=False):
        """
        Runs the main triangulation method on the in_ object with any additional
        user flags input as triflags.

        The following flags are included by default:

        - Q Quiet: suppresses all output messages from Triangle library

        - z Numbers all items starting from zero (zero-indexed) rather than one.

        Adapted from Shewchuk's documentation:

        The sequence is roughly as follows.  Many of these steps can be skipped,
        depending on the command line switches.

        - Read the vertices from a file and triangulate them (no -r)
        - Insert the PSLG segments (-p), and possibly segments on the convex
          hull (-c).
        - Read the holes (-p), regional attributes (-pA), and regional area
          constraints (-pa).  Carve the holes and concavities, and spread the
          regional attributes and area constraints.
        - Enforce the constraints on minimum angle (-q) and maximum area (-a).
          Also enforce the conforming Delaunay property (-q and -a).
        - Compute the number of edges in the resulting mesh.
        - Promote the mesh's linear triangles to higher order elements (-o).
        - Write the output files.
        - Check the consistency and Delaunay property of the mesh (-C).

        """
        if triflags:
            self.validate_input_flags(triflags)
        opts = f"{'Q' if not verbose else 'V'}z{triflags}".encode('utf-8')
        if ctriangulate(opts, self._in._io, self._out._io, self._vorout._io) \
                is not None:
            raise RuntimeError('Triangulation failed')
        return self.out

    cpdef delaunay(self, verbose=False):
        """
        Run the main triangulation method on the in_ object with *only* -Qz
        flags enabled.

        - Q Quiet: suppresses all output messages from Triangle library

        - z Numbers all items starting from zero (zero-indexed) rather than one.

        """
        opts = f"{'Q' if not verbose else 'V'}z".encode('utf-8')
        if ctriangulate(opts, self._in._io, self._out._io, self._vorout._io) \
                is not None:
            raise RuntimeError('Delaunay triangulation failed')
        return self.out

    cpdef convex_hull(self, verbose=False):
        """
        Run the main triangulation method on the in_ object with -Qzc flags enabled.

        - Q Quiet: suppresses all output messages from Triangle library.

        - z Numbers all items starting from zero (zero-indexed) rather than one.

        - c Encloses the convex hull with segments

        """
        opts = f"{'Q' if not verbose else 'V'}zc".encode('utf-8')
        if ctriangulate(opts, self._in._io, self._out._io, self._vorout._io) \
                is not None:
            raise RuntimeError("""Delaunay triangulation and convex hull
                               construction failed""")
        return self.out

    cpdef voronoi(self, verbose=False):
        """
        Run the main triangulation method on the in_ object with -Qzv flags enabled.

        - Q Quiet: suppresses all output messages from Triangle library.

        - z Numbers all items starting from zero (zero-indexed) rather than one.

        - v Generates a Voronoi diagram.

        """
        opts = f"{'Q' if not verbose else 'V'}zv".encode('utf-8')
        if ctriangulate(opts, self._in._io, self._out._io, self._vorout._io) \
                is not None:
            raise RuntimeError("""Delaunay triangulation and generation of
                               voronoi diagram failed""")
        return self.out


def triangulate(input_dict, flags):
    """
    Triangulates an input dict with the following properties:

    Required entries:
    - vertices: A list of pairs [x, y] that are vertex coordinates.

    Optional entries:
    - vertex_attributes: An list of lists of vertex attributes (floats).
      Each vertex must have the same number of attributes, and
      len(vertex_attributes) must match the number of points.

    - vertex_markers: A list of vertex markers; one int per point.

    - triangles: A list of lists of triangle corners (not necessarily 3).
      Corners are designated in a counterclockwise order, followed by any
      other nodes if the triangle represents a nonlinear element (e.g. num_corners > 3).

    - triangle_attributes: A list of triangle attributes. Each triangle must have
      the same number of attributes.

    - triangle_max_area: A list of triangle area constraints; one per triangle,
      0 if not set.

    - segments: A list of segment endpoints, where each list contains vertex
      indices.

    - segment_markers: A list of segment markers; one int per segment.

    - holes: A list of [x, y] hole coordinates.

    - regions: A list of regional attributes and area constraints. Note that
      each regional attribute is used only if you select the `A` switch, and each area
      constraint is used only if you select the `a` switch (with no number following).

    Returns:
    - A dictionary containing the successful triangulation data.

    """
    # parse regions
    if "regions" in input_dict:
        raw_regions = input_dict["regions"]
        parsed_regions = []
        for region in raw_regions:
            parsed_regions.append(
                {
                    "vertex": [region[0], region[1]],
                    "marker": int(region[2]),
                    "max_area": region[3],
                }
            )
        input_dict["regions"] = parsed_regions
    triangle_obj = CyTriangle(input_dict)
    triangle_obj.triangulate(flags)
    return triangle_obj.out.to_dict(opt="np")
