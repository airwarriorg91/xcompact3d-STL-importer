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
    plt.ylim([0,lx])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim([0,lz])    
    plt.show()

def epsiwrite(array1,array2=None,dim=None, ftype=None):
    if (not os.path.exists(os.getcwd()+"\geometry")):
        os.makedirs(os.getcwd()+"\geometry")
    array1t = array1.flatten('F')
    if ftype == 'epsilon':
        array1t = np.int_(array1t)
        np.savetxt("geometry/epsilon.bin",array1t,fmt='%12d')
        print("epsilon.bin generated successfully.")
    elif ftype == 'obj':
        np.savetxt("geometry/nobj"+dim+".dat",array1t,fmt='%12d')
        print("nobj"+dim+".dat generated successfully.")
    elif ftype == 'xixf':
        array2t = array2.flatten("F")
        temp = list(zip(array1t, array2t))
        np.savetxt("geometry/"+dim+"i"+dim+"f"+".dat",temp,fmt=['%24.16E','%24.16E'])
        print(dim+"i"+dim+"f"+".dat generated successfully.")
    elif ftype == 'nxifpif':
        array2t = array2.flatten("F")
        temp = list(zip(array1t, array2t))
        np.savetxt("geometry/n"+dim+"if"+"pif.dat",temp,fmt=['%12d','%12d'])
        print("n"+dim+"if"+"pif.dat generated successfully.") 
    else:
        pass
    


def epsi_gen(file_name,nx,ny,nz,lx,ly,lz,cex,cey,cez,nraf,iibm,BC,nobjmax,npif,izap,isShow,isPlot):
    mesh = epsi_load(file_name)
    if(isShow):
        mesh.show()

    if(mesh.is_watertight):
        P, epshape = meshgen(lx,ly,lz,nx,ny,nz)
        ep0 = geogen(mesh,P,cex,cey,cez)
        ep = np.reshape(ep0,epshape)
        ep = np.transpose(ep, (1,0,2))
        epshape = (epshape[1], epshape[0], epshape[2])
        dd, nrafL = meshRef(lx,ly,lz,nx,ny,nz,BC,nraf)
        
        if(isPlot):
            epsiPlot(ep0,P,lx,ly,lz)
        epsiwrite(ep,ftype="epsilon")

        if(iibm==1):
            pass
        elif(iibm==2):
            #counting the number of objects in the x, y and z directions
            nobjx = obj_count(ep,'x',epshape)
            epsiwrite(nobjx,dim='x',ftype='obj')
            nobjy = obj_count(ep,'y',epshape)
            epsiwrite(nobjy,dim='y',ftype='obj')
            nobjz = obj_count(ep,'z',epshape)
            epsiwrite(nobjz,dim='z',ftype='obj')

            #generating xepsi with a refinement in x direction and counting 
            #the number of objects in x direction after refinement 
            P, shape = meshgen(lx,ly,lz,nrafL[0],ny,nz)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjxraf = obj_count(geo,'x',shape)
            

            #getting the boundaries in the x direction
            xi, xf = get_boundaries(geo,'x',shape, lx, ly, lz, nobjmax, dd)

            #if the number of objects in x direction doesn't match before and after refinement
            if(nobjx.all()!=nobjxraf.all()):
                xi, xf = fixBugs(ep, geo,'x',epshape, nobjx,nobjxraf, nraf, nobjmax, xi, xf) 
            epsiwrite(xi,xf,'x','xixf')

            #generating yepsi with a refinement in y direction and counting
            #the number of objects in y direction after refinement
            P, shape = meshgen(lx,ly,lz,nx,nrafL[1],nz)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjyraf = obj_count(geo,'y',shape)

            #getting boundaries in the y direction
            yi, yf = get_boundaries(geo,'y',shape, lx, ly, lz,nobjmax, dd)

            #if the number of objects in y direction doesn't match before and after refinement
            if(nobjy.all()!=nobjyraf.all()):
                yi, yf = fixBugs(ep, geo,'y',epshape, nobjy,nobjyraf, nraf, nobjmax, yi, yf)
            epsiwrite(yi,yf,'y','xixf')

            #generating zepsi with a refinement in z direction and counting
            #the number of objects in z direction after refinement
            P, shape = meshgen(lx,ly,lz,nx,ny,nrafL[2])
            geo = geogen(mesh,P,cex,cey,cez)
            geo = geogen(mesh,P,cex,cey,cez)
            geo = np.reshape(geo,shape)
            geo = np.transpose(geo, (1,0,2))
            shape = (shape[1], shape[0], shape[2])
            nobjzraf = obj_count(geo,'z',shape)

            #getting boundaries in the z direction
            zi, zf = get_boundaries(geo,'z',shape, lx, ly, lz,nobjmax, dd)

            #if the number of objects in z direction doesn't match before and after refinement
            if(nobjz.all()!=nobjzraf.all()):
                zi, zf = fixBugs(ep, geo,'z',epshape, nobjz,nobjzraf, nraf, nobjmax, zi, zf)
            print("zi, zf generated successfully")
            epsiwrite(zi,zf,'z','xixf')

            #generating nxifpif, nyifpif, nzifpif 

            nxipif, nxfpif = verify(ep, 'x', epshape, nobjmax, npif, izap)
            epsiwrite(nxipif,nxfpif,'x','nxifpif')
            nyipif, nyfpif = verify(ep, 'y', epshape, nobjmax, npif, izap)
            epsiwrite(nyipif,nyfpif,'y','nxifpif')
            nzipif, nzfpif = verify(ep, 'z', epshape, nobjmax, npif, izap)
            epsiwrite(nzipif,nzfpif,'z','nxifpif')

        else:
            raise ValueError("Incorrect type of IBM Method entered.")
    else:
        raise ValueError("The STL geometry should be watertight.")