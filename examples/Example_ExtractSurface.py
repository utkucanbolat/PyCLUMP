import numpy as np
from functions.ExtractSurface import ExtractSurface


N_sphere = 200
N_circle = 100

clump = np.array([[1, 0, 0, 1.1],
                  [2, 1, 0, 1.1],
                  [3, 0, 0, 1.2]])

visualise = True

faces, vertices = ExtractSurface(clump, N_sphere, N_circle, visualise)

