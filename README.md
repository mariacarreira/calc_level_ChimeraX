# calc_level_ChimeraX
ChimeraX plugin to predict and visualize isosurface levels for 3D density maps. This tool is based on a 3D CNN initially developed to predict the isosurface levels of 3D density maps required by [SIREn](https://www.github.com/lkinman/SIREn). More details about the 3D CNN and SIREn can be found [here](https://www.github.com/lkinman/SIREn).


## Installation (Part 1)

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

If necessary, more details on installing ChimeraX environments can be found [here](https://www.cgl.ucsf.edu/chimerax/docs/devel/environment.html).

## Installation (Part 2)  

When running calc_level for the first time, open the ChimeraX GUI and execute the following commands in the ChimeraX command line:

```
pip install torch (in case this error message appears "ModuleNotFoundError: No module named 'torch'")
  Note: Windows users might need to run instead (cd C:\Program Files\ChimeraX <version>\bin)
  pip install torch==2.2.1
```

Select ChimeraX Preferences dropdown (on Mac, see UCSF ChimeraX>Settings; on Linux, see Favorites>Settings; on Windows, see TODO), go to Startup tab, and add the line below to 'Execute these commands at startup':

```
open calc_level_ChimeraX/calc_level.py 
```

## Running
To predict the isosurface level for density maps and visualize them at the predicted levels, run:

```
open map(s) (*.mrc format) 
volume calc_level #1 (e.g., for multiple maps, volume calc_level #1,2 or volume calc_level #1-5)

```

## Integration with other software

The predicted isosurface levels (a.k.a. binarization thresholds) can be provided to other downstream electron microscopy tools, including [SIREn](https://www.github.com/lkinman/SIREn) and [MAVEn](https://www.github.com/lkinman/MAVEn).


