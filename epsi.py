import numpy as np
import trimesh
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from epsiIBM import obj_count, get_boundaries, fixBugs, verify

def meshRef(lx,ly,lz,nx,ny,nz,BC, nraf):
    nrafL = [0,0,0]
    if BC[0]==0 and BC[1]==0:  
        nrafL[0] = nx*nraf
    else:
        nrafL[0] = (nx-1)*nraf+1

    if BC[2]==0 and BC[3]==0:
        nrafL[1] = ny*nraf
    else:
        nrafL[1] = (ny-1)*nraf+1

    if BC[4]==0 and BC[5]==0:
        nrafL[2] = nz*nraf
    else:
        nrafL[2] = (nz-1)*nraf+1

    dd = [lx/nx, lx/nrafL[0], ly/ny, ly/nrafL[1], lz/nz, lz/nrafL[2]]

    return dd, nrafL

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

def epsiwrite(epsilon,shape,file_name,nz,ny):
    if (not os.path.exists(os.getcwd()+"\geometry")):
        os.makedirs(os.getcwd()+"\geometry")
    epsilon=np.reshape(epsilon,shape)
    index = np.where(epsilon == True)

    with open("geometry/epsilon_"+file_name+".dat", 'w') as f:
        f.write(str(len(index[0]))+'\n')
        for x in range(len(index[0])):
            f.write(str(index[0][x])+' '+str(index[1][x])+' '+str(index[2][x])+'\n')
    print("epsilon_"+file_name+".dat"+" generated successfully.")


def epsi_gen(file_name,nx,ny,nz,lx,ly,lz,cex,cey,cez,nraf,iibm,BC,nobjmax,npif,izap,isShow,isPlot):
    mesh = epsi_load(file_name)
    if(isShow):
        mesh.show()

    if(mesh.is_watertight):
        P, epshape = meshgen(lx,ly,lz,nx,ny,nz)
        ep = geogen(mesh,P,cex,cey,cez)
        ep = np.reshape(ep,epshape)
        ep = np.transpose(ep, (1,0,2))
        epshape = (epshape[1], epshape[0], epshape[2])
        dd, nrafL = meshRef(lx,ly,lz,nx,ny,nz,BC,nraf)
        
        if(isPlot):
            epsiPlot(ep,P,lx,ly,lz)
        epsiwrite(ep,epshape,file_name,nz,ny)

        if(iibm==1):
            pass
        elif(iibm==2):

            #counting the number of objects in the x, y and z directions
            nobjx = obj_count(ep,'x',epshape)
            nobjy = obj_count(ep,'y',epshape)
            nobjz = obj_count(ep,'z',epshape)

            #generating xepsi with a refinement in x direction and counting 
            #the number of objects in x direction after refinement 
            P, shape = meshgen(lx,ly,lz,nrafL[0],ny,nz)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjxraf = obj_count(geo,'x',shape)
            print("nobjxraf generated successfully")

            #getting the boundaries in the x direction
            xi, xf = get_boundaries(geo,'x',shape, lx, ly, lz, nobjmax, dd)

            #if the number of objects in x direction doesn't match before and after refinement
            if(nobjx.all()!=nobjxraf.all()):
                xi, xf = fixBugs(ep, geo,'x',epshape, nobjx,nobjxraf, nraf, nobjmax, xi, xf) 
            print("xi, xf generated successfully")

            #generating yepsi with a refinement in y direction and counting
            #the number of objects in y direction after refinement
            P, shape = meshgen(lx,ly,lz,nx,nrafL[1],nz)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjyraf = obj_count(geo,'y',shape)
            print("nobjyraf generated successfully")

            #getting boundaries in the y direction
            yi, yf = get_boundaries(geo,'y',shape, lx, ly, lz,nobjmax, dd)

            #if the number of objects in y direction doesn't match before and after refinement
            if(nobjy.all()!=nobjyraf.all()):
                yi, yf = fixBugs(ep, geo,'y',epshape, nobjy,nobjyraf, nraf, nobjmax, yi, yf)
            print("yi, yf generated successfully")

            #generating zepsi with a refinement in z direction and counting
            #the number of objects in z direction after refinement
            P, shape = meshgen(lx,ly,lz,nx,ny,nrafL[2])
            geo = geogen(mesh,P,cex,cey,cez)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjzraf = obj_count(geo,'z',shape)
            print("nobjzraf generated successfully")

            #getting boundaries in the z direction
            zi, zf = get_boundaries(geo,'z',shape, lx, ly, lz,nobjmax, dd)

            #if the number of objects in z direction doesn't match before and after refinement
            if(nobjz.all()!=nobjzraf.all()):
                zi, zf = fixBugs(ep, geo,'z',epshape, nobjz,nobjzraf, nraf, nobjmax, zi, zf)
            print("zi, zf generated successfully")

            #generating nxifpif, nyifpif, nzifpif 

            nxipif, nxfpif = verify(ep, 'x', epshape, nobjmax, npif, izap)
            print("nxipif, nxfpif generated successfully")
            nyipif, nyfpif = verify(ep, 'y', epshape, nobjmax, npif, izap)
            print("nyipif, nyfpif generated successfully")
            nzipif, nzfpif = verify(ep, 'z', epshape, nobjmax, npif, izap)
            print("nzipif, nzfpif generated successfully")

        else:
            raise ValueError("Incorrect type of IBM Method entered.")
    else:
        raise ValueError("The STL geometry should be watertight.")