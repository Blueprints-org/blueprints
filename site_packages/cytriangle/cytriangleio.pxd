from cytriangle.ctriangle cimport triangulateio

cdef class TriangleIO:
    cdef triangulateio* _io
