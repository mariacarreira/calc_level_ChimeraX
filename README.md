# calc_level_ChimeraX
ChimeraX command to predict and visualize isosurface levels for 3D density maps. This tool is based on a 3D CNN initially developed to predict the isosurface levels of 3D density maps required by [SIREn](https://www.github.com/lkinman/SIREn). More details about the 3D CNN and SIREn can be found [here](https://www.github.com/lkinman/SIREn).


## Installing  

To install the calc_level_ChimeraX code, follow the instructions below:
```
git clone https://github.com/mariacarreira/calc_level_ChimeraX.git
cd calc_level_ChimeraX
tar -xzvf weights.tar.gz
```
Then, install ChimeraX (instructions [here](https://www.cgl.ucsf.edu/chimera/download.html)). MacOS users might need to run on the terminal:
```
xcode-select --install
```
If necessary, ore details on installing ChimeraX environments can be found [here](https://www.cgl.ucsf.edu/chimerax/docs/devel/environment.html).

## Running  

To predict the isosurface level for density maps and visualize them at those levels, open the ChimeraX GUI and execute the following commands in the ChimeraX command line:
```
pip install torch (in case this error message appears ''ModuleNotFoundError: No module named 'torch''')
open map(s) (*mrc format) 
open calc_level_ChimeraX/calc_level.py 
volume calc_level #1 (e.g., for multiple maps, volume calc_level #1,2 or volume calc_level #1-5)
```

## Integration with other software

The predicted isosurface levels (aka binarization thresholds) can be provided to other downstream electron microscopy tools, including [SIREn](https://www.github.com/lkinman/SIREn) and [MAVEn](https://www.github.com/lkinman/MAVEn).


