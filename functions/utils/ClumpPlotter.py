import numpy as np
import matplotlib.pyplot as plt

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
