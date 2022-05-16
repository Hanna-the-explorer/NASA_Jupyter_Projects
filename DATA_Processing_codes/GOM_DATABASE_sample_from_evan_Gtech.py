#The pandastable module has a built in graphing ability which appears best for quick and dirty graphs
#See https://www.youtube.com/watch?v=Ss0QIFywt74 for video on functionality
#Note default option after hitting plot is to use index (check box in graph window) as x-axis. User may set a column as the index and select a single column for the y-axis before hitting plot
#Using the index as the x-axis and selecting two column will allow the second selected column to be set as error bars (check box in graph window)
#Note refresh button on graph window must be pressed to update changes
#
#The tkinter module controls the gui windows and setup
#The sqlite3 module controls the databse creation and queries

#################################################
#IMPORT MODULES
import sqlite3 as sql
import pandas as pd
import openpyxl
from sqlalchemy import create_engine
from tkinter import *
from pandastable import Table, TableModel, config
#################################################

#CREATE GUI WINDOW (root)
root = Tk()
#Window background color
root['background'] = 'floral white'
#Window title. Default is Tk if not changed or set to blank
root.title('')

#GUI WINDOW SIZE
#############################################
##UPDATE IF TOO SMALL AFTER NEW OPTIONS ADDED
#############################################
root.geometry('520x240')

#GUI SCREEN TITLE LABEL
Title_label = Label(root, text = 'Gulf of Mexico OA project database', bg = 'floral white')
Title_label.grid(column = 1, row = 0, columnspan = 2)

##CREATE SELECTION WINDOWS
####################################################
##ADD AND PLACE NEW LABEL IF NEW SEARCH OPTION ADDED
####################################################
#Create selection window labels
#<bg = > option is for background color
Cruise_label = Label(root, text = 'Select Cruise(s)', bg = 'floral white')
Station_label = Label(root, text = 'Select Station(s)', bg = 'floral white')
Analysis_label = Label(root, text = 'Select Analysis or Analyses', bg = 'floral white')
Type_Label = Label(root, text = 'Select Sample Type(s)', bg = 'floral white')

#Place selection window labels
Cruise_label.grid(column = 0, row = 1)
Station_label.grid(column = 1, row = 1)
Analysis_label.grid(column = 2, row = 1)
Type_Label.grid(column = 3, row = 1)

#Create lists of selection window labels. Note <'*'> option input below does not do anything is searched in query and results in an error
###########################################################################################
##ADD NEW SELECTION OPTIONS HERE, IF NEW OPTION TYPE IS ADDED, UPDATE OTHER INDICATED LINES
###########################################################################################
Cruise_options = ['*', '102020_GOM', '072021_GOM', '102021_GOM', '042021_GOM', '072021_GOM']
Station_options = ['*', '5B', 4, 'MK', 7, 2, 16, 9, 14, 13, 11, 15, 12, '7 PW Thin', '2 PW Thin', '5B PW Thin', 'DICKSON']
Analysis_options = ['*', 'Ammonium_Spec', 'Benthic Flux', 'Carbon Isotope', 'DIC Flow Injection', 'Diffusive Flux']
Type_options = ['*', 'BC', 'PW', 'Standard']

#Create selection windows. Note these have a scolling functionality but no scrollbar shown by default
############################################
##ADD NEW LISBOX HERE IF NEW OPTION IS ADDED
############################################
clicked = StringVar()
clicked.set('*')

Cruise_select = Listbox(root, selectmode = 'multiple', exportselection = FALSE)
Cruise_select.grid(column = 0, row = 2)
for each in range(len(Cruise_options)):
    Cruise_select.insert(END, Cruise_options[each])

Station_select = Listbox(root, selectmode = 'multiple', exportselection = FALSE)
Station_select.grid(column = 1, row = 2)
for each in range(len(Station_options)):
    Station_select.insert(END, Station_options[each])

Analysis_select = Listbox(root, selectmode = 'multiple', exportselection = FALSE)
Analysis_select.grid(column = 2, row = 2)
for each in range(len(Analysis_options)):
    Analysis_select.insert(END, Analysis_options[each])

Type_select = Listbox(root, selectmode = 'multiple', exportselection = FALSE)
Type_select.grid(column = 3, row = 2)
for each in range(len(Type_options)):
    Type_select.insert(END, Type_options[each])

#CREATE DATABASE ENGINE    
#Creates/calls to sqlite database with given name
#Databse name given after <:///>
#Database should save in the folder that this code is ran from
engine = create_engine('sqlite:///GOM_Database', echo=False)

#######################
##IMPORT MS EXCEL FILES
#######################
##ADD NEW FILES HERE
#######################
#<engine = 'openpyxl'> is used because <.read_excel.()> does not support .xlsx files by default
AM_102020_PW = pd.read_excel(r'H:\PhD_Data\Ammonium_Spec\102020_GOM\102020_GOM_PW_Ammonium_Spec.xlsx', sheet_name = 'Database', engine = 'openpyxl')
AM_072021_BC = pd.read_excel(r'H:\PhD_Data\Ammonium_Spec\072021_GOM\BC\072021_GOM_BC_Ammonium_Spec.xlsx', sheet_name = 'Database', engine = 'openpyxl')
AM_072021_PW = pd.read_excel(r'H:\PhD_Data\Ammonium_Spec\072021_GOM\PW\072021_GOM_PW_Ammonium_Spec.xlsx', sheet_name = 'Database', engine = 'openpyxl')

Benthic_Fluxes = pd.read_excel(r'H:\PhD_Data\Benthic_Fluxes\GOM_Benthic_Fluxes.xlsx', sheet_name = 'Database', engine = 'openpyxl')

Carbon_Isotopes_072021 = pd.read_excel(r'H:\PhD_Data\Carbon_Isotopes\072021_GOM\072021_GOM_Carbon_Isotopes.xlsx', sheet_name = 'Database', engine = 'openpyxl')                              
Carbon_Isotopes_102020 = pd.read_excel(r'H:\PhD_Data\Carbon_Isotopes\102020_GOM\102020_GOM_Carbon_Isotopes.xlsx', sheet_name = 'Database', engine = 'openpyxl')                              
Carbon_Isotopes_102021 = pd.read_excel(r'H:\PhD_Data\Carbon_Isotopes\102021_GOM\102021_GOM_Carbon_Isotopes.xlsx', sheet_name = 'Database', engine = 'openpyxl')

DIC_FI_072021_BC = pd.read_excel(r'H:\PhD_Data\DIC_FlowInjection\072021_GOM\072021_GOM_BC_DIC.xlsx', sheet_name = 'Database', engine = 'openpyxl') 
DIC_FI_072021_PW = pd.read_excel(r'H:\PhD_Data\DIC_FlowInjection\072021_GOM\072021_GOM_PW_DIC.xlsx', sheet_name = 'Database', engine = 'openpyxl') 
DIC_FI_102020 = pd.read_excel(r'H:\PhD_Data\DIC_FlowInjection\102020_GOM\102020_GOM_DIC.xlsx', sheet_name = 'Database', engine = 'openpyxl') 
DIC_FI_102021 = pd.read_excel(r'H:\PhD_Data\DIC_FlowInjection\102021_GOM\102021_GOM_PW_DIC.xlsx', sheet_name = 'Database', engine = 'openpyxl')

Diffusive_Fluxes = pd.read_excel(r'H:\PhD_Data\Diffusive_Fluxes\GOM_Diffusive_fluxes.xlsx', sheet_name = 'Database', engine = 'openpyxl')

#################################
##CONCATENATE IMPORTED DATAFRAMES
#################################
##ADD IMPORTED DATAFRAMES HERE
#################################
Dataframes = [
    AM_102020_PW,
    AM_072021_BC,
    AM_072021_PW,
    Benthic_Fluxes,
    Carbon_Isotopes_072021,
    Carbon_Isotopes_102020,
    Carbon_Isotopes_102021,
    DIC_FI_072021_BC,
    DIC_FI_072021_PW,
    DIC_FI_102020,
    DIC_FI_102021,
    Diffusive_Fluxes
    ]

Bulk_Data = pd.concat(Dataframes)

#CONVERT CONCATENATED DATAFRAME TO SQL
Bulk_Data.to_sql('data', engine, if_exists = 'replace', index = False)

#CREATE BUTTON TO SEARCH FOR DATA IN DATABASE BASED ON SELECTED VALUES
#Function that runs on button click
def Data_button_click():

    #Create lists of selection from GUI
    ####################################
    ##ADD NEW LINES HERE FOR NEW OPTIONS
    ####################################
    Cruise_selections = []
    Station_selections = []
    Analysis_selections = []
    Type_selections = []
    
    for item in Cruise_select.curselection():
        Cruise_selections.append(Cruise_select.get(item))
    for item in Station_select.curselection():
        Station_selections.append(Station_select.get(item))
    for item in Analysis_select.curselection():
        Analysis_selections.append(Analysis_select.get(item))
    for item in Type_select.curselection():
        Type_selections.append(Type_select.get(item))

    #Formats ? usage for each <WHERE...IN({})> option in query search
    #In sqlite3 query search input ? is replaced with supplied text similar to using <.format()>
    ######################################################
    ##ADD NEW Option_join BLOCK HERE FOR NEW ADDED OPTIONS
    ######################################################
    Cruise_join = '?'
    if len(Cruise_selections) > 1:
        Cruise_join = ['?']
        Cruise_join.append((' , ?')*(len(Cruise_selections)-1))
        Cruise_join = ''.join(Cruise_join)
     
    Station_join = '?'
    if len(Station_selections) > 1:
        Station_join = ['?']
        
        Station_join.append((' , ?')*(len(Station_selections)-1))
        Station_join = ''.join(Station_join)
        
    Analysis_join = '?'
    if len(Analysis_selections) > 1:
        Analysis_join = ['?']
        Analysis_join.append((' , ?')*(len(Analysis_selections)-1))
        Analysis_join = ''.join(Analysis_join)
        
    Type_join = '?'
    if len(Type_selections) > 1:
        Type_join = ['?']
        Type_join.append((' , ?')*(len(Type_selections)-1))
        Type_join = ''.join(Type_join)

    #Query search, text containint ? symbols is input into {} by <.format()>. Question marks, specific to sqlite3, are replaced by lists given after the <.format(),> line: <(""".format(), (*list1, *list2,...))>
    ############################################
    ##UPDATE "WHERE" LINE IF NEW OPTION ADDED IN
    ###############################################################################################################################
    #To update, add in the following to the end of the <"SELECT.....WHERE ....."> line that is in quotations : <AND option IN ({})>
    #Additionally, add in to the end of <.format()>: <Option_join>
    #Additionally, add in to the end of final set of (), which contains asterisks: <(*Option_selections)>
    ###############################################################################################################################
    results = engine.execute(
        "SELECT * from data \
        WHERE TRIP_ID IN ({}) AND Station IN ({}) AND Analysis IN ({}) AND Sample_Type IN ({}) \
        ".format(Cruise_join, Station_join, Analysis_join, Type_join),
        (*Cruise_selections, *Station_selections, *Analysis_selections, *Type_selections)
                             )

    #Convert query results to pandas dataframe and drop completely empty columns
    Final = pd.DataFrame(results, columns = Bulk_Data.columns)
    Final.dropna(how = 'all', axis = 1, inplace = True)
    Final = Final.round(3)

    #Create secondary GUI window
    #Toplevel() is used to create secondary windows while Tk() creates a primary window
    Table_window = Toplevel(root)
    Table_window.geometry('1000x1000')
    Table_window.title('')
    frame = Frame(Table_window)
    frame.pack(expand = True, fill = 'both')

    #Create table with gathered data and show
    GUI_table = Table(frame, dataframe = Final, showtoolbar = True, showstatusbar = True)
    GUI_table.show()

    #Loops secondary window GUI
    Table_window.mainloop()   

#CREATE AND PLACE GET DATA BUTTON
Data_button = Button(root, text = 'Get Data', command = Data_button_click)
Data_button.grid(column = 0, row = 3, columnspan = 4)

#LOOPS TKINTER GUI
root.mainloop()                       



