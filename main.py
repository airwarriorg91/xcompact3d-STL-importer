# STL to epsilon function generator for xcompact3d
from epsi import epsi_gen

#parameters
file_name = "flat-plate"
nx,ny,nz = 321,320,20
lx,ly,lz = 55,15.25,15.25
cex,cey,cez = lx/2,ly/2, lz/2
iibm = 2
nraf = 10
BC = [2,2,0,0,0,0]
nobjmax = 2
isShow = 0
isPlot = 0

epsi_gen(file_name,nx,ny,nz,lx,ly,lz,cex,cey,cez,nraf,iibm,BC,nobjmax,isShow,isPlot)