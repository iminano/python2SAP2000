# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 12:39:27 2021

@author: iminano
"""


import comtypes.client
import streamlit as st
import numpy as np
import pandas as pd
import math
import os
import sys
import comtypes.client


st.write("""

# SAP 2000: Tunnel ring modeller

""")

st.sidebar.header('User Input Values')




def user_input_features():

    Diameter = st.sidebar.text_input('Tunnel mean diameter, D [m]',10)

    	##st.sidebar.add_rows

    nel = st.sidebar.slider('Number of elements, nel', min_value=1, max_value = 1000, step = 1)

    	##st.sidebar.add_rows

    # No_Of_Years = st.sidebar.selectbox('Select No Of Years',Year_List, 2)



    data = {'Diameter': Diameter,'Number of elements': nel}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

def nelLength(df):
    l=(2*np.pi*(0.5*float(df["Diameter"][0]))**2)/(int(df["Number of elements"][0]))
    return l

st.subheader('User Entered parameters : ')

st.write(df)

st.subheader('The calculated element length is:')


st.write(np.round(nelLength(df),2), 'm')
df_1=nelLength(df)

R=float(df["Diameter"][0])/2
nno=(int(df["Number of elements"][0]))+1


r=np.linspace(0,math.radians(360),nno)

loc=[]    # (x,y,z)
for i in r:
    loc.append(("GLOBAL","Cartesian",R*math.cos(i),0.0,R*math.sin(i),0.0,0.0,0.0))
    
loc=np.asarray(loc)

def runSAP2000(loc):
    

    
    #set the following flag to True to attach to an existing instance of the program
    
    #otherwise a new instance of the program will be started
    
    AttachToInstance = False
    
     
    
    #set the following flag to True to manually specify the path to SAP2000.exe
    
    #this allows for a connection to a version of SAP2000 other than the latest installation
    
    #otherwise the latest installed version of SAP2000 will be launched
    
    SpecifyPath = False
    
     
    
    #if the above flag is set to True, specify the path to SAP2000 below
    
    # ProgramPath = 'C:\Program Files\Computers and Structures\SAP2000 23\SAP2000.exe'
    # ProgramPath = 'C:\Program Files\Computers and Structures\SAP2000 23>sap2000.exe /L PLUS'
    
    # ProgramPath = "C:\Program Files\Computers and Structures\SAP2000 23\plus.bat"
    
    #full path to the model
    
    #set it to the desired path of your model
    
    APIPath = 'C:\SAP2000'
    
    if not os.path.exists(APIPath):
    
            try:
    
                os.makedirs(APIPath)
    
            except OSError:
    
                pass
    
    ModelPath = APIPath + os.sep + 'API_1-001.sdb'
    
     
    
    #create API helper object
    
    helper = comtypes.client.CreateObject('SAP2000v1.Helper')
    
    helper = helper.QueryInterface(comtypes.gen.SAP2000v1.cHelper)
    
     
    
    if AttachToInstance:
    
        #attach to a running instance of SAP2000
    
        try:
    
            #get the active SapObject
    
                mySapObject = helper.GetObject("CSI.SAP2000.API.SapObject") 
    
        except (OSError, comtypes.COMError):
    
            print("No running instance of the program found or failed to attach.")
    
            sys.exit(-1)
    
    else:
    
     
    
        if SpecifyPath:
    
            try:
    
                #'create an instance of the SAPObject from the specified path
    
                mySapObject = helper.CreateObject(ProgramPath)
    
            except (OSError, comtypes.COMError):
    
                print("Cannot start a new instance of the program from " + ProgramPath)
    
                sys.exit(-1)
    
        else:
    
            try:
    
                #create an instance of the SAPObject from the latest installed SAP2000
    
                mySapObject = helper.CreateObjectProgID("CSI.SAP2000.API.SapObject")
    
            except (OSError, comtypes.COMError):
    
                print("Cannot start a new instance of the program.")
    
                sys.exit(-1)
    
     
    
        #start SAP2000 application
    
        mySapObject.ApplicationStart()
    
        
    
    #create SapModel object
    
    SapModel = mySapObject.SapModel
    
     
    
    #initialize model
    
    SapModel.InitializeNewModel()
    
     
    
    #create new blank model
    
    ret = SapModel.File.NewBlank()
    
     
    
    #define material property
    
    # """
    # eMatType_Steel = 1
    
    # eMatType_Concrete = 2
    
    # eMatType_NoDesign = 3
    
    # eMatType_Aluminum = 4
    
    # eMatType_ColdFormed = 5
    
    # eMatType_Rebar = 6
    
    # eMatType_Tendon = 7
    
    # """
    
    eMatType=2
    
    
    
    ret = SapModel.PropMaterial.SetMaterial('Concrete', eMatType)
    
    #assign other properties
    
    ret = SapModel.PropMaterial.SetOConcrete_1("Concrete", 5, False, 0, 1, 2, 0.0022, 0.0052, -0.1) 
    
    #assign isotropic mechanical properties to material
    
    ret = SapModel.PropMaterial.SetMPIsotropic('Concrete', 3600, 0.2, 0.0000055)
    
     
    #define rectangular frame section property
    
    ret = SapModel.PropFrame.SetRectangle('R1', 'Concrete', 0.4, 1)
    
     
    
    #define frame section property modifiers
    
    # ModValue = [1, 1, 1, 1, 1, 1, 1, 1]
    
    # ret = SapModel.PropFrame.SetModifiers('R1', ModValue)
    
     
    
    #switch to k-ft units
    
    kN_m_C = 6
    
    ret = SapModel.SetPresentUnits(kN_m_C)
        
    for i in range(nno-1):
        FrameName=str(i)
    
        [FrameName, ret] = SapModel.FrameObj.AddByCoord(float(loc[i][2]), float(loc[i][3]), float(loc[i][4]), 
                                                        float(loc[i+1][2]), float(loc[i+1][3]), float(loc[i+1][4]), 
                                                        FrameName, "R1", '1', 'Global')
       
    return  

if st.button('Run SAP2000'):
    runSAP2000(loc)
    
    
