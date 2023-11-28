from functions.GenerateClump_Euclidean_3D import GenerateClump_Euclidean_3D
import sys
sys.path.append('../')

inputGeom = 'ParticleGeometries/Hexahedron_Coarse_Mesh.stl'
N = 21
rMin = 0
div = 102
overlap = 0.6
output = 'EU_hexaCoarse.txt'
visualise = True

GenerateClump_Euclidean_3D(inputGeom=inputGeom, N=N, rMin=rMin, div=div, overlap=overlap, output=output, visualise=True, VTK=True)