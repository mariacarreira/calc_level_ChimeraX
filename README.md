# calc_level_ChimeraX
ChimeraX command to predict and visualize isosurface levels for 3D density maps. This tool is based on a 3D CNN initially developed to predict the isosurface levels of 3D density maps required by [SIREn](https://www.github.com/lkinman/SIREn). More details about the 3D CNN and SIREn can be found [here](https://www.github.com/lkinman/SIREn).


## Installing  

To install the calc_level_ChimeraX code, follow the instructions below:
```
git clone https://github.com/mariacarreira/calc_level_ChimeraX.git
cd calc_level_ChimeraX
tar -xzvf weights.tar.gz
```

## Running  

To predict the isosurface level for density maps and visualize them at those levels, start by installing ChimeraX (instructions [here](https://www.cgl.ucsf.edu/chimera/download.html)).
Then open the ChimeraX GUI and execute the following commands in the ChimeraX command line:
```
xcode-select --install (for MacOS users to run on the terminal, if required)
pip install torch (if not already installed in your ChimeraX environment)
open map(s) (*mrc format) 
open calc_level_ChimeraX/calc_level.py 
volume calc_level #1 (e.g., for multiple maps, volume calc_level #1,2 or volume calc_level #1-5)
```

## Integration with other software

The predicted isosurface levels (aka binarization thresholds) can be provided to other downstream electron microscopy tools, including [SIREn](https://www.github.com/lkinman/SIREn) and [MAVEn](https://www.github.com/lkinman/MAVEn).


