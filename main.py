# STL to epsilon function generator for xcompact3d

import numpy as np
import trimesh
import matplotlib.pyplot as plt

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

    nx,ny,nz = 101,101,10
    lx,ly,lz = 30,30,6
    cex,cey = 15,15
    r=0.5
    print("generating domain mesh..")
    X = np.arange(0-cex+r,(lx-cex+r)+((lx-cex+r)/nx),(lx-cex+r)/nx)
    Y = np.arange(0-cey+r,(ly-cey+r)+((ly-cey+r)/ny),(ly-cey+r)/ny)
    Z = np.arange(0,lz+(lz/nz),lz/nz)
    Px,Py,Pz = np.meshgrid(X,Y,Z)
    P = np.stack((Px.ravel(),Py.ravel(),Pz.ravel()), axis=1)
    print("Domain mesh generation completed !")

    #checking if the geometry and mesh coincide.
    p = trimesh.PointCloud(P)
    print("Centroid of Geometry: ",mesh.centroid)
    print("Centroid of Mesh: ",p.centroid)

    print("generating the epsilon function")
    epsilon = mesh.contains(P)
    print("epsilon function generated. Saving into epsilon.txt")

    with open("epsilon.txt", 'w') as f:
        for x in epsilon:
            f.write(str(x)+'\n')

    print("Epsilon file generated successfully.")

else:
    raise GeometryNotWatertightException
