def ComputeCtAB(A, B, C, CtAB):
    import _pylibROM.linalg as libROM
    import mfem.ser as mfem
    from ctypes import c_double

    # spatial basis is always distributed regardless of actual MPI initialization.
    assert((B.distributed()) and (C.distributed()) and (not CtAB.distributed()))

    num_rows = B.numRows()
    num_cols = B.numColumns()
    num_rows_A = A.NumRows()

    assert(C.numRows() == num_rows_A)

    Bvec = libROM.Vector(num_rows, False)
    BvecData = Bvec.getData()
    ABvec = mfem.Vector(num_rows_A)

    AB = libROM.Matrix(num_rows_A, num_cols, True)
    ABdata = AB.getData()

    for i in range(num_cols):
        B.getColumn(i, Bvec)
        A.Mult(mfem.Vector(BvecData, num_rows), ABvec)
        ABdata[:, i] = (c_double * ABvec.Size()).from_address(int(ABvec.GetData()))
        # for j in range(num_rows_A):
        #     AB[j, i] = ABvec[j]

    C.transposeMult(AB, CtAB)
    return