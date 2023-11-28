import numpy as np
import matplotlib.pyplot as plt
import pyvista as pv

def clump_plotter(P, F, clump):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create patch
    ax.plot_trisurf(P[:, 0], P[:, 1], P[:, 2], triangles=F, color=[0, 1, 0, 0.2], edgecolor='none')

    # Set properties
    ax.set_box_aspect([np.ptp(a) for a in [P[:, 0], P[:, 1], P[:, 2]]])  # axis equal
    ax.grid(True)  # grid on

    # Plot spheres
    u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]  # sphere mesh
    for i in range(len(clump.radii)):
        x, y, z, r = clump.positions[i, 0], clump.positions[i, 1], clump.positions[i, 2], clump.radii[i]
        X = r * np.cos(u) * np.sin(v) + x
        Y = r * np.sin(u) * np.sin(v) + y
        Z = r * np.cos(v) + z
        ax.plot_surface(X, Y, Z, color=np.random.rand(3), edgecolor='none')

    plt.show()


def clump_plotter_pyvista(clump, opacity=1.0, phi_res=50, theta_res=50):
    """
    Plots 3D spheres using PyVista with increased opacity, a white background, and a finer mesh.
    Each sphere is defined by its center (x, y, z) and radius r.

    :param spheres_data: Array of sphere data [[x1, y1, z1, r1], ..., [xn, yn, zn, rn]]
    :param opacity: Opacity of the spheres, default is 1.0
    :param phi_res: Resolution of the mesh in the azimuthal direction
    :param theta_res: Resolution of the mesh in the polar direction
    """

    spheres_data = np.hstack((clump.positions, clump.radii))

    plotter = pv.Plotter()

    # Precompute colors for all spheres
    colors = [plt.cm.jet(i / len(spheres_data)) for i in range(len(spheres_data))]

    # Batch process the spheres
    for (x, y, z, r), color in zip(spheres_data, colors):
        sphere = pv.Sphere(radius=r, center=(x, y, z), phi_resolution=phi_res, theta_resolution=theta_res)
        plotter.add_mesh(sphere, color=color, opacity=opacity)

    plotter.show()