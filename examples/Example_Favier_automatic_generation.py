from functions.GenerateClump_Favier import GenerateClump_Favier

inputGeom = 'ParticleGeometries/Ellipsoid_R_2.0_1.0_1.0.stl'
N = 10
chooseDistance = 'min'
output = 'FA_Ellipsoid_2.0_1.0_1.0.txt'
# visualise=true

GenerateClump_Favier(inputGeom=inputGeom, N=N, chooseDistance=chooseDistance, output=output)