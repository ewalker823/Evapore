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
5. Select your data (excel files only .xslx)
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
11. Click "Confirm Bounds" and the average evaporation rate will be displayed as a
    dotted line. Where this line intersects the graph is the beginning of pore draining for your membrane.
12. The time point equal to the intersection will auto-populate. Otherwise click or enter the time point.
14. The program will plot the final distribution and will prompt the user to save
    the results.
NOTE: THE DATA WILL SAVE IN THE SAME DIRECTORY HOME UNDER /Evapore/. EACH SAVED
FILE WILL APPEND THE DATA TYPE TO THE ORIGINAL FILE NAME.
15. To start another session, simply navigate to file->New Session
16. To exit close the window or navigate to file->Exit
17. Additional information is stored under the about tab
