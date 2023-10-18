import numpy as np
from stl.mesh import Mesh


def read_stl(stl_dir, is_duplicated=False):
    # read stl files into mesh. mesh contains all the required information
    mesh = Mesh.from_file(stl_dir)

    # extract the vectors of vertices
    P = mesh.points.reshape(-1, 3)

    # face enumeration
    F = np.arange(0, P.shape[0], dtype=np.int64).reshape(mesh.points.shape[0], 3)

    if is_duplicated:
        return F, P
    else:
        # now take unique values to do stl.SlimVerts.m's job
        # it discards the common vertices to avoid duplication.
        P_unique, indices = np.unique(P, return_inverse=True, axis=0)

        F_unique = indices.reshape(-1, 3)

        return F_unique, P_unique


"""def read_stl(stl_dir, isDublicated=False):
    # read stl files into mesh. mesh contains all the required information
    mesh = Mesh.from_file(stl_dir)

    # extract the vectors of vertices
    # note: below can be vectorized. it is good for now.
    P = np.zeros((mesh.points.shape[0] * 3, 3))
    k = 0
    for row in mesh.points:
        P[k, :] = row[0:3]
        P[k + 1, :] = row[3:6]
        P[k + 2, :] = row[6:9]
        k += 3

    # face enumeration
    F = np.arange(0, P.shape[0]).reshape(mesh.points.shape[0], 3)  # BE CAREFUL INDEXING. IT STARTS FROM 0 NOT 1

    # now take unique values to do stl.SlimVerts.m's job
    # it discards the common vertices to avoid dublication. This can be controlled by isDublicated flag.
    F_redefine = np.arange(0, P.shape[0])  # BE CAREFUL INDEXING. IT STARTS FROM 0 NOT 1
    P_unique, indices = np.unique(P, return_inverse=True, axis=0)

    F_unique = F_redefine[indices]
    F_unique = F_unique.reshape(F_unique.shape[0] // 3, 3)

    if isDublicated:
        return F, P
    else:
        return F_unique, P_unique"""
