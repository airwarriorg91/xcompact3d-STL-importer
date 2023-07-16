# STL to epsilon function generator for xcompact3d

import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


# define Python user-defined exceptions
class GeometryNotWatertightException(Exception):
    "Epsilon function generation failed. The geometry is not watertight. Please check!"
    pass
   
#loading the stl file
file_name = "flat-plate"
mesh = trimesh.load_mesh("models/"+file_name+".STL")
print(trimesh.units.units_from_metadata(mesh))

#the stl geometry should be watertight otherwise
#generation of epsilon function fails.

if (mesh.is_watertight) : 
    #mesh.show() 
    # uncomment to verify the mesh. Press q on the 
    # keyboard to quit to proceed forward.

    #generating the domain with required parameters

    nx,ny,nz = 641,640,20
    lx,ly,lz = 275,76.25,76.25
    cex,cey,cez = lx/2,ly/2, lz/2
    #r=0.5
    print("generating domain mesh..")
    X = np.arange(0,lx,(lx)/nx)
    Y = np.arange(0,ly,(ly)/ny)
    Z = np.arange(0,lz,lz/nz)
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
    index = np.where(epsilon == True)
    epsilonPoints = P[index]
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
    plt.show() #uncomment to visualize the epsilon function
    
    print("epsilon function generated. Saving into epsilon.txt")

    epsilon=np.reshape(epsilon,(len(X),len(Y),len(Z)))
    index = np.where(epsilon == True)
    with open("epsilon_"+file_name+"_"+str(nx)+".dat", 'w') as f:
        f.write(str(len(index[0]))+'\n')
        for x in range(len(index[0])):
            f.write(str(index[0][x])+' '+str(index[1][x])+' '+str(index[2][x])+'\n')

    print("Epsilon file generated successfully.")

else:
    raise GeometryNotWatertightException
