import numpy as np
import trimesh
from scipy.ndimage import distance_transform_edt
from functions.utils.ClumpPlotter import clump_plotter


"""
Clump generator using the Euclidean map for voxelated, 3D particles 
2020 © V. Angelidakis, S. Nadimi, M. Otsubo, S. Utili.

The main concept of this methodology:
1. We import the surface mesh of a particle.
2. We transform the mesh into a voxelated representation, i.e. a binary
   3D image, where each voxel belonging to the particle is equal to zero.
3. The Euclidean distance transform of the 3D image is computed and
   the radius of the largest inscribed sphere is found as the maximum
   value of the Euclidean transform of the voxelated image.
4. The voxels corresponding to the inscribed sphere are then set equal to
   one. This methodology can also generate overlapping spheres, if only a
   percentage of the voxels of each new sphere are set equal to one,
   instead of all of them.
5. This process is repeated until a user-defined number of spheres 'N' is
   found or until the user-defined minimum radius criterion has been met,
   as the spheres are generated in decreasing sizes.
"""


class Clump:
    def __init__(self):
        self.positions = np.empty((0, 3))
        self.radii = np.empty((0, 1))
        self.minRadius = None
        self.maxRadius = None
        self.numSpheres = None


def GenerateClump_Euclidean_3D(inputGeom, N, rMin, div, overlap, **kwargs):
    """
    :param inputGeom: Directory of stl file, used to generate spheres
    :param N: Number of spheres to be generated.
    :param rMin: Minimum allowed radius: When this radius is met, the generation procedure stops even before N spheres are generated.
    :param div: Division number along the shortest edge of the AABB during voxelisation (resolution). If not given, div=50 (default value in iso2mesh).
    :param overlap: Overlap percentage: [0,1): 0 for non-overlapping spheres, 0.4 for 40% overlap of radii, etc.
    :param kwargs: Can contain either of the optional variables "output".
                - File name for output of the clump in .txt form. If not assigned, a .txt output file is not created.
    :return: mesh: structure containing all relevant parameters of polyhedron
                    mesh.vertices
                    mesh.faces
                    mesh.centroid
                    mesh.volume
                    mesh.inertia
                    mesh.inertiaPrincipal
                    mesh.orientationsPrincipal

            clump:	structure containing all relevant clump parameters
                    clump.positions		:	M-by-3 matrix containing the position of each generated sphere.
                    clump.radii			:	M-by-1 vector containing the radius of each generated sphere
                    clump.minRadius		:	Minimum generated sphere (might differ from rmin)
                    clump.maxRadius		:	Maximum generated sphere
                    clump.numSpheres	:	Total number of spheres

            output: txt file with centroids and radii, with format: [x,y,z,r]
    """

    ################################################################################################
    #                                   Main Body of the Function                                  #
    ################################################################################################

    clump = Clump()  # instentiate Clump object for later use

    # F, P = STLReader.read_stl(stlFile)  # read the STL file and get faces and vertices
    # Build "mesh" structure
    # mesh = RigidBodyParameters.RBP(F, P)  # calculate the rigid body parameters based on F and P.

    mesh = trimesh.load_mesh(inputGeom)  # this will be used for voxalization
    F = mesh.faces
    P = mesh.vertices

    # Calculate extreme coordinates & centroid of the AABB of the particle
    minX, minY, minZ = np.min(P[:, 0]), np.min(P[:, 1]), np.min(P[:, 2])
    maxX, maxY, maxZ = np.max(P[:, 0]), np.max(P[:, 1]), np.max(P[:, 2])
    aveX, aveY, aveZ = np.mean((minX, maxX)), np.mean((minY, maxY)), np.mean((minZ, maxZ))

    # Center the particle to the centroid of its AABB
    P[:, 0] -= aveX
    P[:, 1] -= aveY
    P[:, 2] -= aveZ

    # Voxalization
    min_AABB = np.min(
        (np.abs(maxX - minX), np.abs(maxY - minY), np.abs(maxZ - minZ)))  # find the shortest length of axes
    voxel_size = min_AABB / div  # determine the voxel size

    img_temp = mesh.voxelized(pitch=voxel_size, method="subdivide").fill()  # voxalize

    intersection = np.pad(np.array(img_temp.matrix), ((2, 2), (2, 2), (2, 2)), mode='constant')  # pad the array with 2 voxels

    # I skipped the part "Ensure the voxel size is the same in all 3 directions -> Might be an overkill, but still".
    # Maybe add it later - Utku

    # Dimensions of the new image
    halfSize = np.array(intersection.shape) / 2
    dx, dy, dz = np.meshgrid(np.arange(1, intersection.shape[1] + 1), np.arange(1, intersection.shape[0] + 1),
                             np.arange(1, intersection.shape[2] + 1))  # be careful about the order

    # Calculate centroid of the voxelated image
    centroid = mesh.centroid  # centroid of the initial particle

    for k in range(N):
        edtImage = distance_transform_edt(intersection, return_distances=True)
        radius = np.max(edtImage)

        if radius < rMin:
            print(f"The mimimum radius rMin={rMin} has been met using {k - 1} spheres")

        xyzCenter = np.argwhere(edtImage == radius)

        dists = np.sqrt(np.sum(np.power(centroid - xyzCenter, 2), axis=1))
        i = np.argmax(dists)

        sph = np.sqrt(
            (dx - xyzCenter[i, 1]) ** 2 + (dy - xyzCenter[i, 0]) ** 2 + (dz - xyzCenter[i, 2]) ** 2) > (
                      1 - overlap) * radius

        intersection = np.logical_and(intersection, sph)

        xyzC = xyzCenter[i] - halfSize + 1

        clump.positions = np.vstack((clump.positions, xyzC * voxel_size))
        clump.radii = np.vstack((clump.radii, radius * voxel_size))

    clump.minRadius = np.min(clump.radii)
    clump.maxRadius = np.max(clump.radii)
    clump.numSpheres = len(clump.radii)

    output = kwargs.get('output')
    if output is not None:
        np.savetxt(output, np.asarray(np.hstack((clump.positions, clump.radii))),
                   delimiter=",")  # In PyCharm this line seems to have an error but it does not. Known issue.

    visualise = kwargs.get('visualise')
    if visualise is not None:
        clump_plotter(P, F, clump)

    return mesh, clump
