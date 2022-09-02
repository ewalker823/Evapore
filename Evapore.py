from asyncore import write
import csv
import ctypes
from decimal import Decimal
from distutils.command.install_scripts import install_scripts
import enum
import math
from operator import indexOf, itemgetter
import os
import sys
import tkinter
from cProfile import label
from enum import Enum
from logging import addLevelName
from pathlib import Path
from select import select
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.filedialog import asksaveasfilename

import matplotlib.cbook as cbook  # external dependency (matplotlib)
import matplotlib.mlab as mlab  # external dependency (matplotlib)
import matplotlib.pyplot as plt  # external dependency (matplotlib) #install 1st
import numpy as np  # external dependency (numpy) 
import openpyxl  # external dependency (openpyxl) #install 2nd
import pandas as pd
import xlrd  # external dependency, install 5th
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from mpldatacursor import datacursor  # external dependency (mpldatacursor) #install 3rd
from pyparsing import col  # external dependency, install 4th

"""
Development by: Andres Ortiz - > andresmortiz1@gmail.com
Copyright: University of Arkansas, 2022
"""

class App(object):
    """ The main class that holds the attributes of the gui"""
    gasconstant = 8.314

    class Results:
        """   
        Subclass that contains the results of the program.
        """
        waverage = -1
        latentslope = -1
        latentwa = -1
        latentstd = -1
        poreDraining = -1
        instdiameter = -1
        totalmassloss = -1
        averageporediameter = -1

    #Constructor: Builds GUI visualization
    def __init__(self) -> None:
        #Initializes main application
        self.mainspace = Tk()
        self.mainspace.geometry('1000x650') 
        self.mainspace.title('Evapoporometry')
        #Initializes menubar, labels, entries, dropdown and widget panel
        #IMPORTANT:
        #    A grid positioning system is used to align the objects properly.
        #    Previously, the components were placed manually which tends to be 
        #    a bad practice in user interface development.
        #
        self.create_menubar()
        self.add_labels()
        self.create_solvent_list()
        self.add_buttons()
        self.add_entries()
        self.create_panel()
        #Define undefined results
        self.results = self.Results()

    #Function that creates menubar
    def create_menubar(self) -> None:
        # Creates menu toolbar
        menubar = Menu(self.mainspace)
        filemenu = Menu(menubar, tearoff = 0)
        # Creates first menu dropdown
        filemenu.add_command(label = "New Session", command = self.clear)
        filemenu.add_command(label = "Open", command = self.open_file)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self.quit_app)
        menubar.add_cascade(label = "File", menu = filemenu)
        # Creates Second menu dropdown
        helpmenu = Menu(menubar, tearoff = 0)
        helpmenu.add_command(label = "About", command = self.show_about)
        helpmenu.add_command(label = "References", command = self.show_references)
        helpmenu.add_command(label = "Contact Developer", command = self.contact_dev)
        menubar.add_cascade(label = "About", menu = helpmenu)
        self.mainspace.config(menu = menubar)

    #Quits application
    def quit_app(self) -> None:
        self.mainspace.destroy()
        quit()
    #Function that creates labels on GUI
    def add_labels(self) -> None:
        Label(self.mainspace, text = "Select Solvent").grid(row = 0, column = 3)
        Label(self.mainspace, text = 'Solvent').grid(row = 0, column = 1, sticky = "W")
        Label(self.mainspace, text = 'Absolute temperature (K)').grid(row = 1, column = 1, sticky = "W")
        Label(self.mainspace, text = 'Data acquisition interval (s)').grid(row = 2, column = 1, sticky = "W")
        #fourthlabel = Label(text = 'Supporting layer pore size (nm)').place(x = 10, y = 220)
        #fifthlabel = Label(text = 'Reported % porosity').place(x = 20, y = 245)     
        #sixthlabel = Label(text = 'X-section area supp. layer pore').place(x = 5, y = 275)

    #Function that creates button to start analysis
    def add_buttons(self) -> None:
        Button(self.mainspace, text = "Analyze Data", command = self.execute).grid(row = 4, column = 1, sticky = "W")

    #Fills the box that lists the solvents
    def create_solvent_list(self) -> None:
        #List of used solvents
        self.solventList = [ "2-propanol", "1-butanol", "ethanol", "acetone", "ethylene glycol", "water"]
        #This variable holds the intermediate solvent that is selected
        self.solventIndexStr = StringVar()
        #Creates dropdown on GUI
        OptionMenu(self.mainspace, self.solventIndexStr, *self.solventList, command = self.select_solvent).grid(row = 1,
            column = 3)
        
    #Changes solvent in entry when user changes the value in the dropdown
    def select_solvent(self, selectedString) -> None:
        #The entry txt has to be deleted first before a new one can be inserted
        self.solventbox.delete(0, END)
        self.solventbox.insert(0, selectedString)
        #This is a safety measure, it should work all of the time. However, if a user somehow manages to change the sel-
        #ected string, it will display an error.
        try:
            self.solventindex = self.solventList.index(selectedString)
        except:
            messagebox.showerror('Error', 'You should not be seeing this message. Please contact the developer.')
        
    #Populates the GUI with entry boxes
    def add_entries(self) -> None:
        self.solventbox = Entry(self.mainspace, bd = 5)    
        self.solventbox.grid(row = 0, column = 2)
        self.temperaturebox = Entry(self.mainspace, bd = 5)
        self.temperaturebox.grid(row = 1, column = 2)
        self.temperaturebox.insert(0, str(297.3))
        self.timeintervalbox = Entry(self.mainspace, bd = 5)
        self.timeintervalbox.grid(row = 2, column = 2)
        #self.supportporebox = Entry(mainspace, bd = 5)
        #self.supportporebox.pack()
        #downstream code for this not implemented yet
        #self.estimatedporositybox = Entry(mainspace, bd = 5)
        #self.estimatedporositybox.pack()
        # downstream code for this not implemented yet
        #self.crosssectionareabox = Entry(mainspace, bd = 5)
        #self.crosssectionareabox.pack()
        # downstream code for this not implemented yet

    #Creates Widget panel that will display graphs and results
    def create_panel(self) -> None:
        #This is the title of the widget that will change throughout the use of the application
        self.widgetPaneltext = Label(self.mainspace, text = "Widget", bg = '#fff')
        self.widgetPaneltext.grid(row = 0, column = 4)
        #This paned window is the object type that is easiest to allow creation of new applications inside of it
        #It is colored black to give an "OFF" feel
        self.widgetPanel = PanedWindow(orient = VERTICAL, bg = '#000000', width = 600, height = 600)
        self.widgetPanel.grid(row = 1, column = 4, rowspan = 20)
        
    #Shows maintanence information
    def show_about(self) -> None:
        #A top level creates a new window that does not interfere with the application
        about_popup = Toplevel(self.mainspace)
        about_popup.title("About")
        Label(about_popup, text = 'Evapore V. 1.0.0 \n Developed and maintained by the Hestekin lab at the University o'
            'f Arkansas').pack(pady = 5, padx = 5)

    #Shows references to scientific journal papeprs
    def show_references(self) -> None:
        #A top level creates a new window that does not interfere with the application
        ref_popup = Toplevel(self.mainspace)
        ref_popup.title("References")
        Label(ref_popup, text = '1: doi.org/10.1016/j.memsci.2013.03.045').grid(row = 1, column = 1, sticky = "W")
        Label(ref_popup, text = '2: doi.org/10.1016/j.memsci.2015.09.013').grid(row = 2, column = 1, sticky = "W")
        Label(ref_popup, text = '3: doi.org/10.1016/j.memsci.2016.11.082').grid(row = 3, column = 1, sticky = "W")

    #Clears all loaded and entered data. Should restore defaults and close any open widgets
    def clear(self) -> None:
        #Clears entries
        self.solventbox.delete(0, END)
        self.temperaturebox.delete(0, END)
        self.timeintervalbox.delete(0, END)
        #Restores Default temperature
        self.temperaturebox.insert(0, 297.3)
        #Removes everything related to solvent attributes
        self.solventindex = -1
        self.solventIndexStr = None
        #Deletes saved excel filepath
        self.exceldirectory = None
        #Tries to reset widget name
        try:
            self.widgetPaneltext.config(text = "Widget")
        except:
            None
        #Tries to destroy any open widgets
        try:
            self.latentspace.destroy()
        except:
            None
        try: 
            self.beginspace.destroy()
        except:
            None
        try:
            self.savespaceWidget.destroy()
        except:
            None

    #Displays contact information for developer
    def contact_dev(self) -> None:
        dev_popup = Toplevel(self.mainspace)
        dev_popup.title("Contact Developer")
        Label(dev_popup, text = "Andres Ortiz: andresmortiz1@gmail.com").pack()

    #Opens excel file
    def open_file(self) -> None:
        #Should propmt user to ONLY select excel file
        self.exceldirectory = tkinter.filedialog.askopenfilename(filetypes = [("Excel", "*.xlsx")])
        #In the event a user manages to not select a file or opens a non .xlsx file, program throws error
        if not (str(self.exceldirectory).endswith(".xlsx")):
            self.open_error(1)
            return
        #Function to read excel file
        self.read_file()

    #Function that displays error popup depending on error type
    def open_error(self, type) -> None:
        match type:
            #User picks invalid/no file 
            case 1:
                messagebox.showerror('File Error', 'Selected file is not supported. Use file with extension .xlsx')
                return
            #User does not enter all information in the GUI
            case 2:
                messagebox.showerror('File Error', 'Unable to analyze data. One or more parameters in the GUI are missi'
                    'ng or invalid.')
                return
            #User selects invalid bounds on the first widget
            case 3:
                messagebox.showerror('Execution Error', 'One or more bounds was not chosen or is incorrect. Terminating'
                    'analysis.')
            #User selects invalid starting point on second widget
            case 4:
                messagebox.showerror('Execution Error', 'Starting Point not chosen or out of bounds. Terminating analys'
                    'is.')
            #Data is invalid and tries to divide things by zero
            case 5:
                messagebox.showerror('Arithmetic Error', 'Divide by zero error, save not completed. Data invalid!')
            
    #Function defines solvent parameters for program depending on selected solvent    
    def load_solvent_data(self, solventindex) -> None:
        #Creates solvent class
        defaultsolvent = self.default_solvents()
        #selects solvent dictionary based on index selected in dropdown
        selectedSolvent = defaultsolvent.select_solvent(self.solventindex)
        #parses dictionary and fills important values
        self.surfaceTension = selectedSolvent["surface_tension"]
        self.vapormolarvolume = selectedSolvent["vapor_molar_volume"]
        self.molarmass = selectedSolvent["molar_mass"]

    #Reads in excel file and parses data into arrays
    def read_file(self) -> None:
        #Reads excel file columns and puts data into PANDAS dataframe
        #Don't know why these columns are flipped
        massDataFrame = pd.read_excel(self.exceldirectory, header = None)
        #Parses PANDAS dataframe into an array
        self.massData = np.concatenate(massDataFrame.values)
           
    #Defines a function enabling the user to save evaporation rate data before further processing
    def save_evap_rate_data(self) -> None:
        answer = messagebox.askyesno(title = 'Save Data', message = 'Do you want to save the intermediate evaporation r'
            'ate data?')
        if not answer:
            return
        #Appends data type to original array
        newFileName = Path(self.exceldirectory).stem +"_Evaporation_rateData.csv"
        #Appends new filename to original directory location
        newSaveFile = os.path.dirname(self.exceldirectory) + "/" + newFileName
        #Tries to save all values in waverage to new file
        with open (newSaveFile, "w") as output:
            writer = csv.writer(output, lineterminator = '\n')
            for val in self.waverage:
                writer.writerow([val])
        
    #First part of execution. Initializes first widget for user to input selections
    def execute(self) -> None:
        #If clear is not selected when running new data
        try:
            self.savespaceWidget.destroy()
        except:
            None
        #Exception for no file selected
        try:
            if not self.exceldirectory:
                self.open_error(1)
                return
        except:
            self.open_error(1)
            return
        #Exception handling for blank solvent
        try:
            if (self.solventindex < 0):
                self.open_error(2)
                return
        except:
            self.open_error(2)
            return
        #Exception handling for time interval box
        try:
            self.time = np.double(self.timeintervalbox.get())
            if self.time <= 0:
                self.open_error(2)
                return
        except:
            self.open_error(2)
            return
        #Exception handling for empty temperature box
        try:
            self.temperature = np.double(self.temperaturebox.get())
            if self.temperature < 0:
                self.open_error(2)
                return
        except:
            self.open_error(2)
            return
         

        #supportpore = int(supportporebox.get())
        self.load_solvent_data(self.solventindex)
        self.newmass = self.movingaverage(self.massData, 7)
        #fills the massaverage list with values derived from a moving average of rawmass with an interval of 7
        #sampledmass = massaverage[::7]
        #"samples every 7th value from the massaverage list"
        #slope = abs(np.gradient(rawmass, 6)) / (float(time))
        #slope = np.array([x - newmass[i - 1] for i, x in enumerate(newmass)][1:])
        self.newmass = np.longdouble(self.newmass)
        diff = -(np.diff(self.newmass))
        self.slope = np.array(diff/np.longdouble(self.time))
        #Yields the instantaneous slope....takes the difference between the sampled mass points.
        self.waverage = (self.slope[::])/self.molarmass
        self.waverage = self.movingaverage(self.waverage,11)
        self.results.waverage = self.waverage
        #Yields the instantaneous evaporation rate
        self.save_evap_rate_data()

        #Create formatter to be used to for plot
        formatter = ScalarFormatter(useMathText = True, useOffset = False) 
        formatter.set_scientific(True) 
        formatter.set_powerlimits((-12, 12)) 
        #Creates range to plot waverage against
        x = range(len(self.waverage))
        y = self.waverage
        #Calculates more variables to be used in plot
        datarange = max(y)-min(y)
        border = abs(datarange+0.0000000000001)
        uppery = max(y)+border
        lowery = min(y)-border

        #Creation of point selection widget 
        self.latentspace = PanedWindow(width = 600, height = 600, bg = '#fff')
        self.widgetPanel.add(self.latentspace)
        self.widgetPaneltext.config(text = "Select bounds of free-standing layer evaporation")
        #Creates components to be displayed on first widget
        firstXLabel = Label(self.latentspace, text = 'Lower X bound').grid(row = 0, column = 0)
        self.firstPSX = StringVar()
        firstXEntry = Entry(self.latentspace, textvariable = self.firstPSX, bd = 5).grid(row = 0, column = 1)
        secondXLabel = Label(self.latentspace, text = 'Upper X bound').grid(row = 1, column = 0)
        self.secondPSX = StringVar()
        secondXEntry = Entry(self.latentspace, textvariable = self.secondPSX, bd = 5).grid(row = 1, column = 1)
        confirmButton = Button(self.latentspace, text = "Confirm bounds", command = self.continue_execute).grid(
            row = 2, column = 0)
        #Creates figure that will house plot
        fig = Figure()
        #Adds plot to figure
        ax = fig.add_subplot(1, 1, 1)
        customCursor = self.CustomCursor(fig, ax, self, 0)
        fig.canvas.mpl_connect('button_press_event',customCursor.onClick)
        #Sets plot attributes
        ax.set_xlabel("Time(s)")
        ax.set_ylabel("Evaporation rate (mol/s)")
        #Creates scatter point of data
        scat = ax.scatter(x*self.time, y, s = 0.1)
        #Sets more plot attributes
        ax.yaxis.set_major_formatter(formatter)
        datacursor(scat)
        ax.set_ylim(lowery, uppery)
        ax.grid(linestyle='--')
        #Draws plot in widget plane to prevent opnening of another new window
        canvas = FigureCanvasTkAgg(fig, master = self.latentspace)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 20)

    #Second part of execution. Initializes second widget for user to input selections
    def continue_execute(self) -> None:
        #Exception handling for not putting filling out requested information
        try: 
            #Case for flip-flopped point selection
            if np.double(self.firstPSX.get()) > np.double(self.secondPSX.get()):
                self.open_error(3)
                self.latentspace.destroy()
                return
            #Case for negative point selection
            if np.double(self.firstPSX.get()) < 0 or np.double(self.secondPSX.get()) < 0:
                self.open_error(3)
                self.latentspace.destroy()
                return
        except:
            self.open_error(3)
            #Kills widget
            self.latentspace.destroy()
            return
        #Grab second points from entry box's StringVars()
        first_point = int(np.double(self.firstPSX.get())/self.time)
        second_point = int(np.double(self.secondPSX.get())/self.time)
        self.secondpoint = second_point
        #Kills widget
        self.latentspace.destroy()
        #Calculates average slope (evaporation rate) across a range of points likely to represent the evaporation of the
        #surface solvent layer and stores in results class
        latentslope = np.mean(self.slope[first_point:second_point])
        self.results.latentslope = latentslope
        self.latentwa = np.mean(self.waverage[first_point:second_point])
        self.results.latentwa = self.latentwa
        #Calculates the standard deviation of the evaporation rate across the same range of points and stores results in
        #the same class
        latentstd = np.std(self.waverage[first_point:second_point])
        self.results.latentstd = latentstd
        #Calculates the results for the pore draining
        self.results.poreDraining = (self.latentwa - (3*latentstd))

        #Initializes formatter for Y axis
        formatter = ScalarFormatter(useMathText = True, useOffset = False) 
        formatter.set_scientific(True) 
        formatter.set_powerlimits((-12, 12)) 
        #Create range to plot against waverage
        x = range(len(self.waverage))
        y = self.waverage
        datarange2 = max(y)-min(y)
        border2 = abs(datarange2+0.0000000000001)
        uppery = max(y)+border2
        lowery = min(y)-border2

        #Creates paned window to add to widget panel
        self.beginspace = PanedWindow(width = 600, height = 600, bg = '#fff')
        self.widgetPanel.add(self.beginspace)
        #Changes widget title text
        self.widgetPaneltext.config(text = "Select bounds of pore draining")
        #Adds components to widget to allow user interaction
        thirdXLabel = Label(self.beginspace, text = 'Indicate beginning of pore draining').grid(row = 0, column = 0)
        self.thirdPSX = StringVar()
        thirdXEntry = Entry(self.beginspace, textvariable = self.thirdPSX, bd = 5).grid(row = 0, column = 1)
        continuebutton = Button(self.beginspace, text = "Confirm Beginning", command = self.finish_execution).grid(
            row = 1, column = 0)        

        #Creates figure that will house plot
        fig = Figure()
        #Adds plot to figure
        axis = fig.add_subplot(1, 1, 1)
        customCursor = self.CustomCursor(fig, axis, self, 1)
        fig.canvas.mpl_connect('button_press_event', customCursor.onClick)
        #Sets plot attributes
        axis.set_xlabel("Time(s)")
        axis.set_ylabel("Evaporation rate (mol/s)")
        #Creates scatter plot based on data previously calculated
        scat = axis.scatter(x*self.time, y, s = 0.1)
        #Uses formatter to set y axis labels
        axis.yaxis.set_major_formatter(formatter)
        #Sets limits on y axis
        axis.set_ylim(lowery, uppery)
        axis.grid(linestyle='--')
        #Canvas allows figure to be placed inside paned window without opening new window
        canvas = FigureCanvasTkAgg(fig, master = self.beginspace)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 20)
        #Adds horizontal line to plot
        horizontalLine_val = y = (self.latentwa - (3*latentstd))
        axis.axhline(y = horizontalLine_val, linestyle = '--')
        

    
    def finish_execution(self) -> None:
        #Exception handling for not putting filling out requested information
        try: 
            #Handles negative values for pore selection
            if np.double(self.thirdPSX.get()) < 0:
                self.open_error(4)
                #Kills widget on error
                self.beginspace.destroy()
                return
        except:
            self.open_error(4)
            #Kills widget on error
            self.beginspace.destroy()
            return
        #Kills widget
        self.beginspace.destroy()
        #Gets value user input on second widget
        startpoint = int(np.double(self.thirdPSX.get())/self.time)
        #Calculates diameter
        instdiameter = ((-4 * self.surfaceTension * self.vapormolarvolume)/(app.gasconstant * (self.temperature) 
            * np.log((self.waverage[startpoint:]/self.latentwa)))) * math.pow(10, 9)
        self.results.instdiameter = instdiameter
        #yields average diameters for each consecutive group of two measured diameters
        avgdiameters = self.movingaverage(instdiameter,2)
        #yields the difference between each consecutive group of two measured diameters
        massdiff= np.array(-np.diff(self.newmass[startpoint:]))
        avgmassdiff = self.movingaverage(massdiff,2)
        #TODO: don't know what this is
        filtereddiameters = [i for i in avgdiameters if i >= 4]
        
        #Creates new widget window 
        self.savespaceWidget = PanedWindow(width = 600, height = 600, bg = '#fff')
        self.widgetPanel.add(self.savespaceWidget)

        #Creates widget with other attributes
        savespace = self.saveSpace()
        savespace.create_datatable(filtereddiameters, avgmassdiff)
        #Prompts users to save pore data
        savespace.save_pore_diam_dist()
        savespace.save_pore_size_dist()
        
        #Creates figure to store subplot
        fig = Figure()
        axis = fig.add_subplot(1, 1, 1)
        #Creates bar graph based on calculated pore mass percentages
        bar = axis.bar(savespace.labels, savespace.poremasspercent.values)
        #Sets plot attributes
        tick_labels = list(map(str, savespace.labels))
        for i in range(len(tick_labels)):
            if i%4:
                tick_labels[i] = ""
        axis.set_xticks(savespace.labels)
        axis.set_xticklabels(tick_labels)
        axis.set_xlabel("Pore diameter (nm)")
        axis.set_ylabel("Fraction of total pores (%)")
        #Creates Canvas to allow figure to be placed inside of widget space
        canvas = FigureCanvasTkAgg(fig, master = self.savespaceWidget)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 3, column = 0, columnspan = 20)
        #Propmts users to save final results from resutls class
        answer = messagebox.askyesno(title = 'Save Data', message = 'Do you want to save the results?')
        if not answer:
            return
        else:
            self.save_results()


    #Writes entries of result class to file
    def save_results(self) -> None:
        #Appends _Results.csv to filename stem
        newFileName =  Path(app.exceldirectory).stem +"_Results.csv"
        #Adds directory to file name
        newSaveFile = os.path.dirname(app.exceldirectory) + "/" + newFileName
        with open (newSaveFile, "w") as output:
            writer = csv.writer(output, lineterminator = '\n')
            #Tries to write results stored in class to file. If value is undefined, it will write -infinity in its place
            try:
                writer.writerow(["Average Pore Diameter", self.results.averageporediameter])
            except: 
                writer.writerow(["Average Pore Diameter",-np.Inf])
            try:
                writer.writerow(["INST Diameter"])
                writer.writerow(self.results.instdiameter)
            except: 
                writer.writerow(["INST Diameter",-np.Inf])
            try:
                writer.writerow(["Latent Slope",self.results.latentslope])
            except: 
                writer.writerow(["Latent Slope",-np.Inf])
            try:
                writer.writerow(["Latent Standard Deviation",self.results.latentstd])
            except: 
                writer.writerow(["Latent Standard Deviation",-np.Inf])
            try:
                writer.writerow(["Latent Evaportaion Rate",self.results.latentwa])
            except: 
                writer.writerow(["Latent Evaportaion Rate",-np.Inf])
            try:
                writer.writerow(["Pore Draining",self.results.poreDraining])
            except: 
                writer.writerow(["Pore Draining",-np.Inf])
            try:
                writer.writerow(["Total Mass Loss",self.results.totalmassloss])
            except: 
                writer.writerow(["Total Mass Loss",-np.Inf])
            try:
                writer.writerow(["Average Evaporation Rate"])
                writer.writerow(self.results.waverage)
            except: 
                writer.writerow(["Average Evaporation Rate",-np.Inf])
        
        
    #Defines a moving average function using NumpyConvolve"
    def movingaverage (self, values, window):
        weights = np.repeat(1.0, window)/window
        sma = np.convolve(values, weights, 'valid')
        return sma    
        
    #This class contains the data for a given solvent     
    class default_solvents:
        # Units of Dictionary: newtons per meter, cubic meters per mole, grams per mole
        class solvent(Enum):
            PROPANOL2 = 1
            BUTANOL1 = 2
            ETHANOL = 3
            ACETONE = 4
            ETHYLENE_GLYCOL = 5
            WATER = 6

        #Dictionaries that correlate attribute strings to actual values
        propanol2 = { "surface_tension" : 0.022, "vapor_molar_volume" : 0.0000766, "molar_mass" : 60.1 }
        butanol1 = {  "surface_tension" : 0.0246, "vapor_molar_volume" : 0.0000915, "molar_mass" : 74.1 }
        ethanol = { "surface_tension" : 0.024, "vapor_molar_volume" : 0.0000584, "molar_mass" : 46.7 }
        acetone = {  "surface_tension" :  0.0237, "vapor_molar_volume" : 0.0000733, "molar_mass" : 58.08 }
        ethylene_glycol = {  "surface_tension" : 0.0477, "vapor_molar_volume" : 0.0000559, "molar_mass" : 62.07 }
        water =  { "surface_tension" : 0.07275, "vapor_molar_volume" : 0.0000180, "molar_mass" : 18.02 }

        #Default constructor
        def __init__(self) -> None:
            pass

        #Selects dictionary based on user's selection on drop down and returns said dictionary
        def select_solvent(self, input):
            _solvent = self.solvent(input+1)
            match _solvent:
                case self.solvent.PROPANOL2:
                    selectedSolvent = self.propanol2
                case self.solvent.BUTANOL1:
                    selectedSolvent = self.butanol1
                case self.solvent.ETHANOL:
                    selectedSolvent = self.ethanol
                case self.solvent.ACETONE:
                    selectedSolvent = self.acetone
                case self.solvent.ETHYLENE_GLYCOL:
                    selectedSolvent = self.ethylene_glycol
                case self.solvent.WATER:
                    selectedSolvent = self.water
            return selectedSolvent

    #Organizational class that confines file saving aspects to singular class
    class saveSpace:
        #Default constructor that creates array with bar plot labels for x axis
        def __init__(self) -> None:
            self.labels = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 
                55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 
                115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 
                165, 170, 175, 180, 185, 190, 195, 200, 205, 210, 
                215, 220, 225, 230, 235, 240, 245, 250, 255, 260, 265, 
                270, 275, 280, 285, 290, 295, 300])
            
        #Defines a function enabling the user to save pore diameter data before further processing
        def save_pore_diam_dist(self) -> None:
            #Checks to see if calculation fails on a divide by zero error. Poremass percent may all be zeros
            try:
                pp = type(self.binnedmasses)
                self.poremasspercent = (self.binnedmasses/self.totalmassloss)*100
                #Calculates the average pore diameter"            
                averageporediameter = sum(self.poremasspercent*self.labels)/sum(self.poremasspercent)
                app.results.averageporediameter = averageporediameter
            except:
                self.poremasspercent = [0] * self.binnedmasses.size
                app.open_error(5)
                return
            #Asks users if they want to save
            answer = messagebox.askyesno(title = 'Save Data', message = 'Do you want to save the pore diameter distribu'
                'tion data?')
            if not answer:
                return
            #Creates new file name and path name to save the file to.
            newFileName = Path(app.exceldirectory).stem +"_PoreDiameter_DistData.csv"
            newSaveFile = os.path.dirname(app.exceldirectory) + "/" + newFileName
            with open (newSaveFile, "w") as output:
                writer = csv.writer(output, lineterminator = '\n')
                writer.writerow(self.binnedmasses)
            
        #Defines a function enabling the user to save pore size data before further processing
        def save_pore_size_dist(self) -> None:
            #Prompts user if they want to save
            answer = messagebox.askyesno(title = 'Save Data', message = 'Do you want to save the pore size distribution'
                ' data?')
            if not answer:
                return
            #Creates new file name and path name to save the file to
            newFileName = Path(app.exceldirectory).stem +"_PoreSize_DistData.csv"
            newSaveFile = os.path.dirname(app.exceldirectory) + "/" + newFileName
            with open (newSaveFile, "w") as output:
                writer = csv.writer(output, lineterminator = ',')
                writer.writerow(self.poremasspercent.values)

        #Creates a dataframe and bins to allow bar plot to be created
        def create_datatable(self, filtereddiameters, avgmassdiff) -> None:
            pandastest = pd.DataFrame(list(zip(filtereddiameters, avgmassdiff)), columns = ['Diameter', 'MassLoss'])
            self.totalmassloss = pandastest['MassLoss'].sum()
            app.results.totalmassloss = self.totalmassloss
            bins = pd.cut(pandastest['Diameter'], 
                [2.5, 7.5, 12.5, 17.5, 22.5, 27.5, 32.5, 37.5, 
                42.5, 47.5, 52.5, 57.5, 62.5, 67.5, 72.5, 77.5, 
                82.5, 87.5, 92.5, 97.5, 102.5, 107.5, 112.5, 
                117.5, 122.5, 127.5, 132.5, 137.5, 142.5, 147.5, 
                152.5, 157.5, 162.5, 167.5, 172.5, 177.5, 182.5, 
                187.5, 192.5, 197.5, 202.5, 207.5, 212.5, 217.5, 
                222.5, 227.5, 232.5, 237.5, 242.5, 247.5, 252.5, 
                257.5, 262.5, 267.5, 272.5, 277.5, 282.5, 287.5, 
                292.5, 297.5, 302.5
            ])
            self.binnedmasses = pandastest.groupby(bins)['MassLoss'].agg('sum')
            #asymmetrycorrectionratiolist = (3.14*(np.array(labels**2)))/(3.14*(supportpore**2))
            #correctedmassloss = binnedmasses * asymmetrycorrectionratiolist
            #poremasspercent = (correctedmassloss/totalmassloss)*100

    class CustomCursor(object):

        def __init__(self, figure, axes, app, type):
            self.focus = 0
            self.axis = axes
            self.app = app
            self.type = type
            self.first = True

        def onClick(self,event):
            if event.inaxes:
                position = (event.x, event.y) 
                match self.type:
                    case 0:
                        if (self.first):
                            self.app.firstPSX.set(event.xdata)
                            self.first = False
                        else:
                            self.app.secondPSX.set(event.xdata)
                            self.first = True
                    case 1:
                        self.app.thirdPSX.set(event.xdata)


            





if __name__ == '__main__':
    print("Starting Application. Please wait!")
    app = App()
    app.mainspace.mainloop()
