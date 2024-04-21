# cython: language_level=3
cimport cython

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef bytes get_long(bytes FILE_DATA, int start):
    return FILE_DATA[start:start + 4]

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list get_wave_info(int start, bytes FILE_DATA):
    cdef bytes AREA_NAME = b""
    cdef int AREA_SIZE = 0
    cdef int FILE_SIZE = len(FILE_DATA)
    cdef int MSIZE = 0
    cdef str MNAME = ""

    cdef int OFFSET = start
    OFFSET += 4
    while OFFSET <= FILE_SIZE:
        AREA_NAME = get_long(FILE_DATA, OFFSET)
        OFFSET += 4
        AREA_SIZE = int.from_bytes(get_long(FILE_DATA, OFFSET), byteorder='little')
        if AREA_NAME == b"data":
            break
        else:
            if AREA_NAME == b"LIST":
                MNAME = get_mark_name(FILE_DATA, OFFSET)
            OFFSET += AREA_SIZE + 4

    FILE_START = start - 8
    SIZE = OFFSET - FILE_START + AREA_SIZE + 4
    SIZE = min(SIZE, FILE_SIZE - FILE_START)
    return [FILE_START, SIZE, MNAME]

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef str get_mark_name(bytes FILE_DATA, int OFFSET):
    cdef int MOFFSET = OFFSET + 12
    cdef int MSIZE = int.from_bytes(get_long(FILE_DATA, MOFFSET), byteorder='little')
    MSIZE -= 4
    MOFFSET += 8
    cdef bytes MNAME = FILE_DATA[MOFFSET:MOFFSET - 1 + MSIZE]
    return MNAME.decode('utf-8')

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef list parse_waves(bytes FILE_DATA):
    cdef bytes WAVE_IDENT = b"WAVEfmt"
    cdef int FILE_SIZE = len(FILE_DATA)
    cdef list matches = []
    cdef tuple IDENT_HEAD = (b"RIFX", b"RIFF")
    cdef int OFFSET = 0

    cdef list DATA = []
    cdef int index = 0

    while True:
        index = FILE_DATA.find(WAVE_IDENT, OFFSET)
        if index == -1 or index is None:
            break
        if get_long(FILE_DATA, index - 8) in IDENT_HEAD:
            DATA = get_wave_info(index, FILE_DATA)
            matches.append(DATA)

        OFFSET = index + 20

    return matches
