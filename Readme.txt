This program simulates a solar powered platform, given havested power, battery capacity and power consumed. There are two controller available in the simulator: receding horizon controller and a naive controller. The simulation serves as a case study of our runtime micro-architectural adaption project. To use the code, please cite:
	 J. Chen and B. Carrion Schafer, "Low Power Design through Frequency-Optimized Runtime Micro-architectural Adaptation", International Conference on Computer Design (ICCD), 2019

For more information about the receding horizon controller, please see:
	Moser, C., Thiele, L., Brunelli, D., Benini, L. "Adaptive power management for environmentally powered systems", IEEE Transactions on Computers, 59(4), 478-491, 2009.

To generate parameters of the controller, MPT MATLAB toolbox can be used:
	https://www.mpt3.org/

Solar radiation data is from the National Solar Radiation Data Base:
	https://rredc.nrel.gov/solar/old_data/nsrdb/1991-2010/hourly/siteonthefly.cgi?id=722590

Please read the code (controller_run.py) if you want to know how the simulator works.