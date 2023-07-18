import numpy as np
import trimesh
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def epsi_load(file_name):
    mesh = trimesh.load_mesh("models/"+file_name+".STL")
    print("Units of the STL: ",trimesh.units.units_from_metadata(mesh))
    return mesh

def meshgen(lx,ly,lz,nx,ny,nz):
    X = np.arange(0,lx,(lx)/nx)
    Y = np.arange(0,ly,(ly)/ny)
    Z = np.arange(0,lz,lz/nz)
    Px,Py,Pz = np.meshgrid(X,Y,Z)
    P = np.stack((Px.ravel(),Py.ravel(),Pz.ravel()), axis=1)
    return P,Px.shape

def geogen(mesh,P,cex,cey,cez):
    #checking if the geometry and mesh coincide.
    p = trimesh.PointCloud(P)
    #moves the centroid of the geometry to the required center [cex,cey,lz/2]
    crrtn = mesh.centroid - [cex,cey,cez]
    mesh.apply_translation(-crrtn)
    epsilon = mesh.contains(P)
    return epsilon

def epsiPlot(epsilon,P,lx,ly,lz):
    epsilonPoints = P[np.where(epsilon==True)]
    print("plotting the points inside the mesh..")
    # Display the points inside the STL geometry
    fig = plt.figure()
    ax = fig.add_subplot(projection = '3d')
    ax.scatter(epsilonPoints[:,0], epsilonPoints[:,1], epsilonPoints[:,2], lw = 0., c = 'k')
    plt.title("Epsilon Function of the geometry")
    plt.xlim([0,lx])
    plt.ylim([0,ly])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim([0,lz])    
    plt.show()

def epsiwrite(epsilon,shape,file_name):
    epsilon=np.reshape(epsilon,shape)
    index = np.where(epsilon == True)
    with open("epsilon_"+file_name+".dat", 'w') as f:
        f.write(str(len(index[0]))+'\n')
        for x in range(len(index[0])):
            f.write(str(index[0][x])+' '+str(index[1][x])+' '+str(index[2][x])+'\n')
    print("epsilon_"+file_name+".dat"+" generated successfully.")

def epsi_gen(file_name,nx,ny,nz,lx,ly,lz,cex,cey,cez,nraf,iibm,isShow,isPlot):
    mesh = epsi_load(file_name)
    if(isShow):
        mesh.show()
    P, shape = meshgen(lx,ly,lz,nx,ny,nz)
    geo = geogen(mesh,P,cex,cey,cez)
    if(isPlot):
        epsiPlot(geo,P,lx,ly,lz)
    epsiwrite(geo,shape,file_name)
    if(mesh.is_watertight):
        if(iibm==1):
            pass
        elif(iibm==2):
            #generating xepsi with a refinement in x direction
            P, shape = meshgen(lx,ly,lz,nx*nraf,ny,nz)
            geo = geogen(mesh,P,cex,cey,cez)
            epsiwrite(geo,shape,file_name+"X")

            #generating yepsi with a refinement in y direction
            P, shape = meshgen(lx,ly,lz,nx,ny*nraf,nz)
            geo = geogen(mesh,P,cex,cey,cez)
            epsiwrite(geo,shape,file_name+"Y")

            #generating yepsi with a refinement in z direction
            P, shape = meshgen(lx,ly,lz,nx,ny,nz*nraf)
            geo = geogen(mesh,P,cex,cey,cez)
            epsiwrite(geo,shape,file_name+"Z")
        else:
            raise ValueError("Incorrect type of IBM Method entered.")
    else:
        raise ValueError("The STL geometry should be watertight.")