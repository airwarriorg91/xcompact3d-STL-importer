# xcompact3d-STL-importer
A python code to generate epsilon function from an STL geometry. Epsilon function is a method to define a geometry in the DNS simulations using the [Xcompact3d](https://github.com/xcompact3d/Incompact3d) code. The code takes input the STL file of the geometry, domain size, mesh size and the position of geometry in the domain and outputs the epsilon function for the simulation case. 

The code is based on the trimesh python library for the import and manipulation of the STL geometry. A big shout out to [trimesh](https://github.com/mikedh/trimesh) library for making it possible. 

## Motivation
I wanted to use complex geometry in xcompact3d code and one of the sister python library [xcompact3d-toolbox](https://github.com/fschuch/xcompact3d_toolbox/) provides the option to input geometry from an STL file in the sandbox mode of xcompact3d. I planned to generate epsilon function for the geomtry and then modify the fortran code of xcompact3d to read the generated epsilon function. But due to compatibility issues in the dependencies of the library, I wasn't able to install the library. So, I built this code to accomplish the problem.

## Dependencies
+ Pandas
+ Numpy
+ Trimesh
+ Matplotlib
+ PyQt5
+ Pyglet
+ Scipy
+ Pillow

## How to install and use the library ?
### Steps to intall the library:
+ Clone this repositry using the command `git clone https://github.com/airwarriorg91/xcompact3d-stl_2_epsilon_generator`
+ Open the repositry folder
+ Install all the dependencies using `pip install -r requirements.txt`

### Xcompact3d Simulation Parameters:
+ `lx`, `ly` and `lz` (Length of domain in x, y and z directions)
+ `nx`, `ny` and `nz` (Mesh size in x, y and z directions)
+ `cex` and `cey` (X and Y coordinates of centre of the geometry)

  _Note: By default the `cez` is set as the midpoint of the length in z-direction i.e. `lz/2`. If you wish to change it, you can modify the line 
  `cex,cey,cez = 15,15, lz/2` to accomodate for the cez._

### Dimensions of geometry in the STL file?
Epsilon Function is a matrix of points scoped from a 3D domain of points based on the geometry. In the program, the parameters are adimnesionalised just like xcompact3d.

For example, if the geomtry is a 3D cylinder with diameter 1 Unit and height is 6 Units, you want a domain 30 x 30 x 6 times the diameter of the cylinder, then the parameters `[lx, ly, lz]` is equal to `[30,30,6]`.

So, parameters `[lx, ly, lz]` should be multipled by the length you have adimensionalized the domain. 

### Running the python code
+ Open the cloned folder and copy your STL file to the models folder.
+ Modify the `main.py` to import the STL and other simulation parameters.
+ To import the STL file, modify the line `mesh = trimesh.load_mesh('models/your_model_name.STL')`.
+ Run the python code using the command in terminal `python path/to/xcompact3d-stl_2_epsilon_generator/main.py`

The python code generates a .txt file which will be read by the fortran code of xcompact3d to create the geometry from the generated epsilon function.


## Results
The code was used to generate epslion function for the following STL geometries.

* Cylinder (Diameter: 1, Height: 6, Domain: (30, 30, 6) and Mesh Size: (261, 260, 20))

  ![Cylinder STL Geometry visualized and converted into Epsilon function using the code](/images/cylinder.png)

* Statue (Height: 10.15, Domain: (30,30, 15) and Mesh Size: (301,300,50))
  
  Model Credit: [Alex Petuhov](https://grabcad.com/library/abstraction-2)

  ![Statue STL Geometry visualized and converted into Epsilon function using the code](/images/statue.png)

* Flat Plate with a bevel (Height: 0.08, Length: 0.4, Domain: (11,3.05,3.05))
  
  Reference Paper: Chen, Jerry M., and Yuan-Cheng Fang. "Strouhal numbers of inclined flat plates." Journal of wind engineering and industrial aerodynamics 61.2-3 (1996): 99-112. 

   ![Flat Plate STL Geometry visualized and converted into Epsilon function using the code](/images/flat-plate.png)

***NOTE: The code is in development phase. If you want to contribute you can create a pull request and discuss it with me through mail. Reach me out [here](mailto:gauravxpgupta@gmail.com)***
