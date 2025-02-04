# calc_level_ChimeraX
ChimeraX plugin to predict and visualize isosurface levels for 3D density maps. This tool is based on a 3D CNN initially developed to predict the isosurface levels of 3D density maps, as required by [SIREn](https://www.github.com/lkinman/SIREn). More details about the 3D CNN and SIREn can be found [here](https://www.github.com/lkinman/SIREn).


## Installation (Part 1)

To install the calc_level_ChimeraX code, run the commands below in the terminal:
```
git clone https://github.com/mariacarreira/calc_level_ChimeraX.git
cd calc_level_ChimeraX
tar -xzvf weights.tar.gz
```
If applicable, you will also need to install ChimeraX (instructions [here](https://www.cgl.ucsf.edu/chimera/download.html)). MacOS users might need to run on the terminal:
```
xcode-select --install
```

If necessary, details on installing ChimeraX environments can be found [here](https://www.cgl.ucsf.edu/chimerax/docs/devel/environment.html).

## Installation (Part 2)  

Open the ChimeraX GUI and, in case this error message appears "ModuleNotFoundError: No module named 'torch'", run:
```
pip install torch 
```
Windows users might need to run the command below inside this directory C:\Program Files\ChimeraX<version>\bin)
```  
pip install torch==2.2.1
```
Select the UCSF ChimeraX Preferences/Settings dropdown (on Mac, see UCSF ChimeraX>Settings; on Linux/Windows, see Favorites>Settings), go to **Startup tab**, and add the line below to **'Execute these commands at startup'**:

```
open calc_level_ChimeraX/calc_level.py 
```
Click 'Save' 

## Running (Part 3)
To predict the isosurface level for density maps and visualize them at the predicted levels, re-open ChimeraX and run:

```
open map(s) (*.mrc format) 
volume calc_level #1 (for multiple maps, volume calc_level #1,2 or volume calc_level #1-5)
```

## Integration with other software

The predicted isosurface levels (a.k.a. binarization thresholds) can be provided to other downstream electron microscopy tools, including [SIREn](https://www.github.com/lkinman/SIREn) and [MAVEn](https://www.github.com/lkinman/MAVEn).


## Citing

If the 3D-CNN predictions are useful to your work, you can cite the paper below:
```bibtex
@article {2024.10.08.617123,
	author = {Kinman LF*, Carreira MV*, Powell BM, Davis JH},
	title = {Automated model-free analysis of cryo-EM volume ensembles with SIREn},
	year = {2024},
	doi = {10.1101/2024.10.08.617123},
	journal = {bioRxiv}
}
```

