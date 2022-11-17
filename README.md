# ECH2O_calibration
This repository contains code to calibrate the ECH2O using the DDS algorithm.
This code is for calibrating the ECH2O hydrologic model using the DDS algorithm. The code runs the ECH2O model and calculates the objective function KGE or NSE. The objective function value is transfered back to the DDS script where it is compared to the previous objective function value. New parameter values are generated and these are transfered back to the calibration script. The calibration file then  changes ascii files and table files,converts these files to binary files for the model and restarts the model run. 

Resources required to run the code can be found at:
- model: https://ech2o.readthedocs.io/projects/ECH2O-SPAC/en/latest/Setup.html
- DDS: https://github.com/bsu-wrudisill/WRF-HYDRO_CALIB
- input data: https://www.hydroshare.org/resource/20d6db6ff9064928803528dcb317dfad/
