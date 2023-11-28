from functions.GenerateClump_Ferellec_McDowell import GenerateClump_Ferellec_McDowell
import sys
sys.path.append('../')

inputGeom = 'ParticleGeometries/Ellipsoid_R_2.0_1.0_0.5.stl'
dmin = 0.1
rmin = 0.01
rstep = 0.01
pmax = 1.0
seed = 5
output = 'FM_ellipsoid.txt'
visualise = True

GenerateClump_Ferellec_McDowell(inputGeom=inputGeom, dmin=dmin, rmin=rmin, rstep=rstep, pmax=pmax, seed=seed, output=output, visualise=visualise, VTK=True)
