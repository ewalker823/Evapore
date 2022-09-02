# Evapore
An executable file to process raw mass measurements of liquid evaporation from a porous material to determine pore size percentage and pore surface area.

This text document provides a simple set of instructions that will hopefully 
instruct users on how to run the software.

1. Firstly, to create a shortcut on the desktop, right click on your 
   windows desktop and navigate to new->shortcut
2. Click browse and navigate to your folder containing the software. The .exe
   file should be under Evapore/dist
3. Click next and change the application to give it a suitable name and hit finish


To run the application:
1. Either click on your shortcut or navigate to Evapore/dist and double click
   on the .exe file
2. The application may take a short while to initialize!
3. The GUI should now be initialized
4. First, open your data under the top menubar: file->open
5. Select your data (excel files only .xslx, formatted as a single mass column with no header)
6. Example data provided for reference
7. Select your solvent in the solvent dropdown box to the right of the listed
   default temperature. This will fill the solvent box with your selected 
   solvent.
7. Fill in your temperature, density, surface tension, vapor pressure, molecular weight (if different from default) and your data acquisition
   interval. Note that these spaces cannot be negative or contain non-numeric 
   characters.
8. Click "Analyze Data" and the program will start
9. The program will now display a graph with the intermediary evaporation rate
    data, click or enter the lower and upper bounds of the free-standing layer evaporation. (This is the constant evaporation of your solvent)
10. Click "Confirm Bounds" and the average evaporation rate will be displayed as a
    dotted line. Where this line intersects the graph is the beginning of pore draining for your membrane.
11. The time point equal to the intersection will auto-populate. Otherwise click or enter the time point.
12. The program will plot the final distribution and will prompt the user to save
    the results.
NOTE: THE DATA WILL SAVE IN THE SAME DIRECTORY HOME UNDER /Evapore/. EACH SAVED
FILE WILL APPEND THE DATA TYPE TO THE ORIGINAL FILE NAME.
13. To start another session, simply navigate to file->New Session
14. To exit close the window or navigate to file->Exit
15. Additional information is stored under the about tab


Interpretation of Results:
This program calculates results of your pores over the time range of the pore draining input to when the calculated diameter falls below 4 nm.

The results file gives the following data:

1. Average Pore Diameter (nm) - An average of all determined diameters over the range. 
2. Average Surface Area (M^2) - An average of all determined pore surface area measurments over the range.
3. Average Specific surface Area (M^2/g) - Average surface area divided by the total mass lost over the range.
4. Latent Slope (mol/s^2) - Slope of the free standing layer evaporation over the input free standing layer range.
5. Latent Standard Deviation - Standard deviation of evaporation values over the input free standing layer range.
6. Pore Draining (mol/s) - evaporation rate at which pore drainng starts, equal to the average evaporation rate of the standing layer minus three standard deviations.
7. Start of Pore Draining (s) - Time point where Pore Draining intersects with the evaporation curve.
8. Total Mass loss (g) - The total mass evaporated over the range.
9. Total Void Volume (M^3) - Volume that was evaporated over the range.
10. INST Filtered Diameters (nm) - Instant diameter calculated at each time point using the evaporation rate over the range. (cut off below 4nm)
11. Average Evaporation rate (mol/s) - All Evaporation rate data averaged with a n = 11
12. Pore Percentage (%) - The Percentage of each pore in the sample. Each value corresponds to the Diameter (nm) results line.
13. Mass loss (g) - The total mass evaporated at each Diameter (nm).
14. Diameter (nm) - Diameters from 5nm to 300nm. Each recorded diameter in the program is grouped to these bins with a 2.5nm tolereance. Ex: 4nm = 5nm , 7.3 nm = 5nm.
15. Variables - Values you input into the program.
