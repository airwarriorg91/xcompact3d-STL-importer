# STL to epsilon function generator for xcompact3d

import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# define Python user-defined exceptions
class GeometryNotWatertightException(Exception):
    "Epsilon function generation failed. The geometry is not watertight. Please check!"
    pass


#loading the stl file
mesh = trimesh.load_mesh('models/cylinder.STL')
print(trimesh.units.units_from_metadata(mesh))

#the stl geometry should be watertight otherwise
#generation of epsilon function fails.

if (mesh.is_watertight) : 
    #mesh.show() 
    # uncomment to verify the mesh. Press q on the 
    # keyboard to quit to proceed forward.

    #generating the domain with required parameters

    nx,ny,nz = 261,260,20
    lx,ly,lz = 30,30,6
    cex,cey,cez = 15,15, lz/2
    r=0.5
    print("generating domain mesh..")
    X = np.arange(0,(lx)+((lx)/nx),(lx)/nx)
    Y = np.arange(0,(ly)+((ly)/ny),(ly)/ny)
    Z = np.arange(0,lz+(lz/nz),lz/nz)
    Px,Py,Pz = np.meshgrid(X,Y,Z)
    P = np.stack((Px.ravel(),Py.ravel(),Pz.ravel()), axis=1)
    print("Domain mesh generation completed !")

    #checking if the geometry and mesh coincide.
    p = trimesh.PointCloud(P)
    print("Centroid of Geometry: ",mesh.centroid)
    print("Centroid of Mesh: ",p.centroid)
    
    #moves the centroid of the geometry to the required center [cex,cey,lz/2]
    crrtn = mesh.centroid - [cex,cey,cez]
    mesh.apply_translation(-crrtn)

    print("After coinciding the geometry and mesh centroids")
    print("Centroid of Geometry: ",mesh.centroid)
    print("Centroid of Mesh: ",p.centroid)

    print("generating the epsilon function")
    epsilon = mesh.contains(P)

    epsilonPoints = np.zeros(shape = (0,3))
    n=0
    for i in epsilon:
        if i:
            epsilonPoints = np.append(epsilonPoints,[P[n]],axis=0)
        n+=1
    epsilonPoints = np.array(epsilonPoints)
    
    print("plotting the points inside the mesh..")
    # Display the points in/out the mesh
    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')
    ax.scatter(epsilonPoints[:,0], epsilonPoints[:,1], epsilonPoints[:,2], lw = 0., c = 'k')
    plt.title("Epsilon Function of the geometry")
    plt.xlim([0,lx])
    plt.ylim([0,ly])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim([0,lx])
    plt.show()
    
    '''print("epsilon function generated. Saving into epsilon.txt")
    with open("epsilon.txt", 'w') as f:
        for x in epsilon:
            f.write(str(x)+'\n')

    print("Epsilon file generated successfully.")'''

else:
    raise GeometryNotWatertightException
