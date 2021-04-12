# MREAbaqusEditor
**MRE Abaqus Editor**
You think editing Inp File in abaqus is painful ? 
Here you can find a python script to edit abaqus job file (.inp) to add magnetic loads 

**Procedure**
First you need to create a job in abaqus. To do that follow this procedure :  
Create the part as you want it  
Create a  dummy material (for example elastical with E = 1 and nu = 0.3, please be careful your material has to be coherent, i.e. nu can be greater than 0.5 for example), a section and assign the section to the previous part  
Create an instance  
Create a step (Please set NLGEOM to yes)  
Mesh the part and set element type to C3D8RH (Hex with reduced intregration and hybrid formulation)  
Create the job file (Click on writing input)  
