from functions.GenerateClump_Ferellec_McDowell import GenerateClump_Ferellec_McDowell

inputGeom = 'ParticleGeometries/Torus.stl'
dmin = 0.1
rmin = 0.01
rstep = 0.01
pmax = 1.0
seed = 5
output = 'FM_torus.txt'
# visualise=true;

GenerateClump_Ferellec_McDowell(stlFile=inputGeom, dmin=dmin, rmin=rmin, rstep=rstep, pmax=pmax, seed=seed, output=output)
