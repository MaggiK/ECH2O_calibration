# -*- coding: utf-8 -*-
"""


@author: Maggi
"""
import os
import pandas as pd
import numpy as np
import hydroeval as he
import time
import math
#from shutil import copyfile

#%%
calibtable=pdf.reset_index()[['Parameter', "Init"]]
calibtable.rename(columns={'Parameter':"op", "Init":"value"}, inplace=True)

#%%
#this function takes values from dds

def calib(x0):
    parameter_names = pdf.index
    calibtable = pd.DataFrame({'op': parameter_names, 'value': x0}) #bring in the parameter names and values from the dds script
    
    if calibtable['op'].str.contains('max_can_storage').any():
        #spc_calib= calibtable.loc[calibtable['op']=='max_can_storage_var1'].reset_index()
        spc_calib = calibtable.loc[calibtable['op'].str.contains('max_can_storage') | calibtable['op'].str.contains('kbeers') | calibtable['op'].str.contains('gsmax') | calibtable['op'].str.contains('gspsihigh') | calibtable['op'].str.contains('gspsilow') | calibtable['op'].str.contains('topt') | calibtable['op'].str.contains('tmin') | calibtable['op'].str.contains('tmax')| calibtable['op'].str.contains('gsvpd')| calibtable['op'].str.contains('gslight')].reset_index()
        change_table(spc_calib)
        bring_in_change_ascii(calibtable.loc[calibtable['op']!='max_can_storage'].reset_index())
    else:
        bring_in_change_ascii(calibtable) #change the map files to the new values
       
    kge_score = modrun() #run the model and output the objecive function
    return(kge_score)


#%%  
    #####################################3
    #####read in the ascii
def bring_in_change_ascii(calibtable):
    #calibtable is the table of calibration parameters with their factors
    #p_index is the location/index of a parameter in the table 
    #use the value in the table to read in the ascii
   
    #split table with uniform and varying parameters
    calibtable2= calibtable[calibtable['op'].str.contains('keff')]
    calibtable2= calibtable2.reset_index()
    calibtable_poros= calibtable[calibtable['op'].str.contains('poros')]
    calibtable_poros= calibtable_poros.reset_index()
    calibtable_psi= calibtable[calibtable['op'].str.contains('psiae')]
    calibtable_psi= calibtable_psi.reset_index()
    calibtable_unif = calibtable.loc[(calibtable['op'].str.contains('leakance')) ] 
    calibtable_unif=calibtable_unif.reset_index()
    calibtable_bc= calibtable[calibtable['op'].str.contains('bc')]
    calibtable_bc= calibtable_bc.reset_index()
    calibtable_kvkh= calibtable[calibtable['op'].str.contains('kvkh')]
    calibtable_kvkh= calibtable_kvkh.reset_index()
    calibtable_snowmelt= calibtable[calibtable['op'].str.contains('snowmelt')]
    calibtable_snowmelt= calibtable_snowmelt.reset_index()
    calibtable_dsoil1= calibtable[calibtable['op'].str.contains('dsoil1')]
    calibtable_dsoil1= calibtable_dsoil1.reset_index()
    calibtable_dsoil2= calibtable[calibtable['op'].str.contains('dsoil2')]
    calibtable_dsoil2= calibtable_dsoil2.reset_index()
    calibtable_soildepth= calibtable[calibtable['op'].str.contains('soildepth')]
    calibtable_soildepth= calibtable_soildepth.reset_index()
    #p_index= 1
    
    
    ###if bc is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('bc').any():
        
        bc_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/bclambda_temp.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(bc_temp_op, "r") as a:
            bc=a.read()
        
        for i in range(len(calibtable_bc)):
            list_of_params_txt.append(calibtable_bc['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_bc['value'][i])
            if calibtable_bc['op'].str.contains('var1')[i]:
                v= round(float(calibtable_bc['value'][i]),4)
                d_replaced= bc.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_bc['op'].str.contains('var2')[i]:
                v= round(float(calibtable_bc['value'][i]), 4)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_bc['op'].str.contains('var3')[i]:
                v= round(float(calibtable_bc['value'][i]),4)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_bc['op'].str.contains('var4')[i]:
                v= round(float(calibtable_bc['value'][i]),4)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v      
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "bclambda.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        list_of_clonefiles.append(t)
        #os.system(str(t))
        os.system("asc2map --clone C:\ech2o\Documentation\dry_data\Spatial\\base.map -a -S C:\ech2o\Documentation\dry_data\Spatial\\bclambda.asc C:\ech2o\Documentation\dry_data\Spatial\\bclambda.map")
         
    ###if dsoil1 is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('dsoil1').any():
        
        dsoil1_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/depth_soil1_temp.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(dsoil1_temp_op, "r") as a:
            dsoil1=a.read()
        
        for i in range(len(calibtable_dsoil1)):
            list_of_params_txt.append(calibtable_dsoil1['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_dsoil1['value'][i])
            if calibtable_dsoil1['op'].str.contains('var1')[i]:
                v= round(float(calibtable_dsoil1['value'][i]),6)
                d_replaced= dsoil1.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil1['op'].str.contains('var2')[i]:
                v= round(float(calibtable_dsoil1['value'][i]), 6)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil1['op'].str.contains('var3')[i]:
                v= round(float(calibtable_dsoil1['value'][i]),6)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil1['op'].str.contains('var4')[i]:
                v= round(float(calibtable_dsoil1['value'][i]),6)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v      
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/depth_soil1.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "depth_soil1.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        list_of_clonefiles.append(t)
        #os.system(str(t))
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -a -S C:/ech2o/Documentation/dry_data/Spatial/depth_soil1.asc C:/ech2o/Documentation/dry_data/Spatial/depth_soil1.map")
    
    ###if dsoil2 is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('dsoil2').any():
        
        dsoil2_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/depth_soil2_temp.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(dsoil2_temp_op, "r") as a:
            dsoil2=a.read()
        
        for i in range(len(calibtable_dsoil2)):
            list_of_params_txt.append(calibtable_dsoil2['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_dsoil2['value'][i])
            if calibtable_dsoil2['op'].str.contains('var1')[i]:
                v= round(float(calibtable_dsoil2['value'][i]),6)
                d_replaced= dsoil2.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil2['op'].str.contains('var2')[i]:
                v= round(float(calibtable_dsoil2['value'][i]), 6)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil2['op'].str.contains('var3')[i]:
                v= round(float(calibtable_dsoil2['value'][i]),6)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_dsoil2['op'].str.contains('var4')[i]:
                v= round(float(calibtable_dsoil2['value'][i]),6)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v      
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/depth_soil2.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "depth_soil2.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        list_of_clonefiles.append(t)
        #os.system(str(t))
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -a -S C:/ech2o/Documentation/dry_data/Spatial/depth_soil2.asc C:/ech2o/Documentation/dry_data/Spatial/depth_soil2.map")
         
    ###if soildepth is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('soildepth').any():
        
        soildepth_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/soildepth_temp.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(soildepth_temp_op, "r") as a:
            soildepth=a.read()
        
        for i in range(len(calibtable_soildepth)):
            list_of_params_txt.append(calibtable_soildepth['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_soildepth['value'][i])
            if calibtable_soildepth['op'].str.contains('var1')[i]:
                v= round(float(calibtable_soildepth['value'][i]),6)
                d_replaced= soildepth.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_soildepth['op'].str.contains('var2')[i]:
                v= round(float(calibtable_soildepth['value'][i]), 6)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_soildepth['op'].str.contains('var3')[i]:
                v= round(float(calibtable_soildepth['value'][i]),6)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_soildepth['op'].str.contains('var4')[i]:
                v= round(float(calibtable_soildepth['value'][i]),6)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v      
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/soildepth2.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "soildepth2.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        list_of_clonefiles.append(t)
        #os.system(str(t))
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -a -S C:/ech2o/Documentation/dry_data/Spatial/soildepth2.asc C:/ech2o/Documentation/dry_data/Spatial/soildepth2.map")
        
        
    ###if kvkh is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('kvkh').any():
        
        kvkh_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/kvkh_temp.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(kvkh_temp_op, "r") as a:
            kvkh=a.read()
        
        for i in range(len(calibtable_kvkh)):
            list_of_params_txt.append(calibtable_kvkh['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_kvkh['value'][i])
            if calibtable_kvkh['op'].str.contains('var1')[i]:
                v= round(float(calibtable_kvkh['value'][i]),7)
                d_replaced= kvkh.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_kvkh['op'].str.contains('var2')[i]:
                v= round(float(calibtable_kvkh['value'][i]), 7)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_kvkh['op'].str.contains('var3')[i]:
                v= round(float(calibtable_kvkh['value'][i]),7)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_kvkh['op'].str.contains('var4')[i]:
                v= round(float(calibtable_kvkh['value'][i]),7)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v      
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/kvkh.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "KvKh.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        list_of_clonefiles.append(t)
        #os.system(str(t))
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -a -S C:/ech2o/Documentation/dry_data/Spatial/kvkh.asc C:/ech2o/Documentation/dry_data/Spatial/KvKh.map")
    
    
    ###if snowmeltcoeff is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('snowmelt').any():
        
        snowmelt_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/snowmeltcoeff_var_temp2.asc" #open the template
        #bc_temp_op="".join(bc_temp_op)
        with open(snowmelt_temp_op, "r") as a:
            snowmelt=a.read()
        
        for i in range(len(calibtable_snowmelt)):
            list_of_params_txt.append(calibtable_snowmelt['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_snowmelt['value'][i])
            if calibtable_snowmelt['op'].str.contains('var1')[i]:
                v= round(float(calibtable_snowmelt['value'][i]),10)
                d_replaced= snowmelt.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_snowmelt['op'].str.contains('var2')[i]:
                v= round(float(calibtable_snowmelt['value'][i]),10)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_snowmelt['op'].str.contains('var3')[i]:
                v= round(float(calibtable_snowmelt['value'][i]),10)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v   
            
                
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/snowmeltcoeff_varies.asc"
            
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
         
        #change the ascii file to a map file 
        #mpfile = "C:/ech2o/Documentation/dry_data/Spatial/bclambda.map"
        mpfile = "snowmeltcoeff.map"
        #mpfile="".join(mpfile)
        t=[] #reset t        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a -S --clone base.map", cal_open2, mpfile]
        t=" ".join(t)
        #os.system(str(t))
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -a -S C:/ech2o/Documentation/dry_data/Spatial/snowmeltcoeff_varies.asc C:/ech2o/Documentation/dry_data/Spatial/snowmeltcoeff.map")
        
    
    ###if poros is in the dataframe then open and do stuff to the ascii##      
    if calibtable['op'].str.contains('poros').any(): 
         
        #poros_temp_op = ["C:\ech2o\Documentation\dry_data\Spatial", r'\\', "poros" ,"_temp", ".asc"] #open the template
        #poros_temp_op="".join(poros_temp_op)
        poros_temp_op ="C:/ech2o/Documentation/dry_data/Spatial/poros_temp.asc" 
        with open(poros_temp_op, "r") as a:
            porosity=a.read()
        
        for i in range(len(calibtable_poros)):
            list_of_params_txt.append(calibtable_poros['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_poros['value'][i])
            if calibtable_poros['op'].str.contains('var1')[i]:
                v= round(float(calibtable_poros['value'][i]),6) 
                d_replaced= porosity.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_poros['op'].str.contains('var2')[i]:
                v= round(float(calibtable_poros['value'][i]), 6)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_poros['op'].str.contains('var3')[i]:
                v= round(float(calibtable_poros['value'][i]),6)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_poros['op'].str.contains('var4')[i]:
                v= round(float(calibtable_poros['value'][i]),6)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v
            
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/poros.asc" 
    
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
            
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -S -a C:/ech2o/Documentation/dry_data/Spatial/poros.asc C:/ech2o/Documentation/dry_data/Spatial/poros.map")
       
        #moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
        #dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/poros", moment, ".map"]
        #dtosave="_".join(dtosave)   
       # with open(dtosave, "w") as i:
        #    i.write(d_replaced)   
        
        #os.system('cls') 

          
     
    ###if keff is in the dataframe then open and do stuff to the ascii##
    if calibtable['op'].str.contains('keff').any():
        
        keff_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/keff_temp.asc" #open the template
       
        with open(keff_temp_op, "r") as a:
            kff=a.read()
        
        for i in range(len(calibtable2)):
            list_of_params_txt.append(calibtable2['op'][i]) #record what we are looking at
            list_of_params.append(calibtable2['value'][i])
            if calibtable2['op'].str.contains('var1')[i]:
                v= round(calibtable2['value'][i],8)
                d_replaced= kff.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable2['op'].str.contains('var2')[i]:
                v= round(calibtable2['value'][i], 8)
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable2['op'].str.contains('var3')[i]:
                v= round(calibtable2['value'][i] ,8)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable2['op'].str.contains('var4')[i]:
                v= round(calibtable2['value'][i], 8)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v
       
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/keff.asc" 
    
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
            
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -S -a C:/ech2o/Documentation/dry_data/Spatial/keff.asc C:/ech2o/Documentation/dry_data/Spatial/keff.map")
       
        
    ###if psiae is in the dataframe then open and do stuff to the ascii##    
    if calibtable['op'].str.contains('psiae').any():
        
        psiae_temp_op = "C:/ech2o/Documentation/dry_data/Spatial/psiae_temp.asc"#open the template
        
        with open(psiae_temp_op, "r") as a:
            psi=a.read()
            
        for i in range(len(calibtable_psi)):
            list_of_params_txt.append(calibtable_psi['op'][i]) #record what we are looking at
            list_of_params.append(calibtable_psi['value'][i])
            if calibtable_psi['op'].str.contains('var1')[i]:
                v= round(calibtable_psi['value'][i], 6)
                d_replaced= psi.replace("var1", str(v)) #replace the place holder with the new value v
            if calibtable_psi['op'].str.contains('var2')[i]:
                v= round(calibtable_psi['value'][i], 6) 
                d_replaced= d_replaced.replace("var2", str(v)) #replace the place holder with the new value v
            if calibtable_psi['op'].str.contains('var3')[i]:
                v= round(calibtable_psi['value'][i], 6)
                d_replaced= d_replaced.replace("var3", str(v)) #replace the place holder with the new value v
            if calibtable_psi['op'].str.contains('var4')[i]:
                v= round(calibtable_psi['value'][i], 6)
                d_replaced= d_replaced.replace("var4", str(v)) #replace the place holder with the new value v
           
        cal_open2 = "C:/ech2o/Documentation/dry_data/Spatial/psi_ae.asc" 
    
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
            
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        os.system("asc2map --clone C:/ech2o/Documentation/dry_data/Spatial/base.map -S -a C:/ech2o/Documentation/dry_data/Spatial/psi_ae.asc C:/ech2o/Documentation/dry_data/Spatial/psi_ae.map")
       
            
    # for everything else revert back to uniform file
    for p_index in range(len(calibtable_unif)):
        #p_index= 1
        #from the table of parameters to calibrate, open and change
        cal_open= calibtable_unif['op'][p_index] #pick on value from the table
        list_of_params_txt.append(calibtable_unif['op'][p_index]) #record what we are looking at
        cal_open2 = ["C:\ech2o\Documentation\dry_data\Spatial", r'\\', cal_open,"_temp", ".asc"] #open the template
        cal_open2="".join(cal_open2)
        with open(cal_open2, "r") as a:
            d=a.read()
        
        #v2= 'var1'
        
        #define v-> this is from the dds model output. the new value to replace
        v= calibtable_unif['value'][p_index]  
        d_replaced= d.replace("var1", str(v)) #replace the place holder with the new value v
        
        list_of_params.append(v) #save the current and replaced values
    
    #save file- saving as text as well
    #with open("C:/ech2o/Documentation/dry_data/Spatial/changedtxt/newparam.txt", "w") as i:
     #   i.write(d_replaced)
    
     
        cal_open2 = ["C:\ech2o\Documentation\dry_data\Spatial", r'\\', cal_open, ".asc"]
        cal_open2="".join(cal_open2)
    
        with open(cal_open2, "w") as i:
            i.write(d_replaced)
    
        #change the ascii file to a map file 
        mpfile = ["C:\ech2o\Documentation\dry_data\Spatial", r'\\', cal_open, ".map"]
        mpfile="".join(mpfile)
        
        os.chdir("C:/ech2o/Documentation/dry_data/Spatial/")
        t= ["asc2map -a --clone C:/ech2o/Documentation/dry_data/Spatial/base.map", cal_open2, mpfile ]
        t=" ".join(t)
        os.system(str(t))
            
#change back
        os.chdir("C:\\ech2o\\")




#%% 
#print("starting run %d" %(modelruns))   
def modrun():
    


    os.chdir("C:\\ech2o\\") 
    os.system('cls||clear')
    os.system("ech2o dry_config.ini") #run the model
    
    
##transpiration##
    #import the transpiration
    tldp= pd.read_csv("E:\Dissertation\Modeling\ech2o\observation_data\sap_2016_2017.csv")
    tldp['DateTime'] = pd.to_datetime(tldp['DateTime'])
    
    modt2= pd.read_table("E:/Dissertation/Modeling/ech2o/Results/Transpiration[2].tab", sep="\t", index_col=0, skiprows=8,
                    names = ['p2', 'p1', 'p5', 'p3','p4',  'N'], header=None)
    
    modt2['p5']= modt2['p5'] *1*60*60*24 #change to m/day
    
    modt2["dt"]= pd.date_range(start="2015-10-01",end="2019-9-30")
    modt2['dt'] = modt2['dt'].dt.strftime('%Y-%m-%d')
    modt2['dt']=pd.to_datetime(modt2['dt'], errors = 'coerce')
    
    mod_meas= modt2.merge(tldp, left_on = 'dt', right_on='DateTime')
    mod_meas['dt'] =pd.to_datetime(mod_meas['dt'], errors = 'coerce')
   

#calculate the NSE or KGE
    def nse(predictions, targets):
        return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

    obj_t= nse(mod_meas['p5'], mod_meas['TCFlo_mperday'])
    
#calculate the KGE
    #kge_calc_t = he.evaluator(he.kge, mod_meas['p5'], mod_meas['TCFlo_mperday']) #non parametric
    kge_calc_t = kge(mod_meas['p5'], mod_meas['TCFlo_mperday']) #mod, meas from function below
    #print("objective function kge", kge_calc)
    # store the objective function 
    list_of_nse_transp.append(obj_t)
    list_of_kge_transp.append(kge_calc_t)

#save the model output elsewhere
    moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
    dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/transpiration_calib", moment, ".tab"]
    dtosave="_".join(dtosave)
    modt2.to_csv(dtosave, sep="\t")
    
###modis transpiration at TL###
    tl_et= pd.read_csv("E:\Dissertation\Modeling\ech2o\observation_data\modis_et_sd_20162017.csv")
    tl_et['date'] = pd.to_datetime(tl_et['date'])
    
    modt2= pd.read_table("E:/Dissertation/Modeling/ech2o/Results/Transpiration[1].tab", sep="\t", index_col=0, skiprows=8,
                names = ['p2', 'p1', 'p5', 'p3', 'p4', 'N'], header=None)


    modt2['p3']= modt2['p3'] *60*60*24*1000 #mm/day

    modt2['p3_rolling']= modt2['p3'].rolling(8).sum().shift(-8)

    modt2["dt"]= pd.date_range(start="2015-10-01",end="2019-9-30")
    modt2['dt'] = modt2['dt'].dt.strftime('%Y-%m-%d')
    modt2['dt']=pd.to_datetime(modt2['dt'], errors = 'coerce')

    mod_meas= modt2.merge(tl_et, left_on = 'dt', right_on='date')
    mod_meas['dt'] =pd.to_datetime(mod_meas['dt'], errors = 'coerce')    
    mod_meas=mod_meas[mod_meas['et_summer'].notna()] #drop the na
    
#calculate the NSE or KGE
    def nse(predictions, targets):
        return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

    obj_t_tl= nse(mod_meas['p3_rolling'], mod_meas['et_summer'])
    
#calculate the KGE
    #kge_calc_t = he.evaluator(he.kge, mod_meas['p5'], mod_meas['TCFlo_mperday']) #non parametric
    kge_calc_t_tl = kge(mod_meas['p3_rolling'], mod_meas['et_summer']) #mod, meas from function below
    #print("objective function kge", kge_calc)
    # store the objective function 
    list_of_nse_transp_tl.append(obj_t_tl)
    list_of_kge_transp_tl.append(kge_calc_t_tl)

    #save the model output elsewhere
    moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
    dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/transpirationTL_calib", moment, ".tab"]
    dtosave="_".join(dtosave)
    modt2.to_csv(dtosave, sep="\t")
    
###streamflow####
    qlg= pd.read_csv("E:\Dissertation\Modeling\ech2o\observation_data\discharge_lg_daily.csv")
    qlg['DateTime'] = pd.to_datetime(qlg['DateTime'])
    qlg['DateTime'] = qlg['DateTime'].dt.strftime('%Y-%m-%d')

#import the results data
    modq= pd.read_table("E:/Dissertation/Modeling/ech2o/Results/Streamflow.tab", sep="\t", index_col=0, skiprows=8,
                    names = ['p2', 'p1', 'p5', 'p3', 'p4', 'N'], header=None)

    modq["dt"]= pd.date_range(start="2015-10-01",end="2019-9-30")
    modq['dt'] = modq['dt'].dt.strftime('%Y-%m-%d')

    mod_meas_lg= modq.merge(qlg, left_on = 'dt', right_on='DateTime', how='left')
    mod_meas_lg['dt'] =pd.to_datetime(mod_meas_lg['dt'], errors = 'coerce')
    mod_meas_lg = mod_meas_lg.dropna(subset=['cms']) #drop the na values
    
#calculate the NSE or KGE
    def nse(predictions, targets):
        return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

    obj_q= nse(mod_meas_lg['p4'], mod_meas_lg['cms'])
    
#calculate the KGE
    #kge_calc_q = he.evaluator(he.kge, mod_meas_lg['p4'], mod_meas_lg['cms']) #non parametric
    kge_calc_q = kge(mod_meas_lg['p4'], mod_meas_lg['cms']) #mod, meas from func below
    #print("objective function kge", kge_calc)
    # store the objective function 
    list_of_nse_stream.append(obj_q)
    list_of_kge_stream.append(kge_calc_q) 
    
    moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
    dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/streamflow_calib", moment, ".tab"]
    dtosave="_".join(dtosave)
    modq.to_csv(dtosave, sep="\t")
    
      
##soil moisture from ldp or same location as transpiration##
    #import the sm
    smldp= pd.read_csv("E:\Dissertation\Modeling\ech2o\observation_data\LDP_soilmoisture_calib.csv")
    smldp['DateTime'] = pd.to_datetime(smldp['DateTime'])
    
    modsm= pd.read_table("E:/Dissertation/Modeling/ech2o/Results/SoilMoistureL1.tab", sep="\t", index_col=0, skiprows=8,
                    names = ['p2', 'p1', 'p5', 'p3', 'p4', 'N'], header=None)
    
    modsm["dt"]= pd.date_range(start="2015-10-01",end="2019-9-30")
    modsm['dt'] = modsm['dt'].dt.strftime('%Y-%m-%d')
    modsm['dt']=pd.to_datetime(modsm['dt'], errors = 'coerce')
    
    mod_meas= modsm.merge(smldp, left_on = 'dt', right_on='DateTime')
    mod_meas['dt'] =pd.to_datetime(mod_meas['dt'], errors = 'coerce')
    mod_meas = mod_meas.dropna(subset=['sm_p1_8cm'])
  

#calculate the NSE or KGE
    def nse(predictions, targets):
        return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

    obj_sm= nse(mod_meas['p5'], mod_meas['sm_p1_8cm'])
    
#calculate the KGE
    #kge_calc_sm = he.evaluator(he.kge, mod_meas['p5'], mod_meas['sm_p1_8cm']) #non parametric
    kge_calc_sm = kge(mod_meas['p5'], mod_meas['sm_p1_8cm']) #mod, meas from function below
    #print("objective function kge", kge_calc)
    # store the objective function 
    list_of_nse_sm.append(obj_sm)
    list_of_kge_sm.append(kge_calc_sm)

#save the model output elsewhere
    moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
    dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/sm_calib", moment, ".tab"]
    dtosave="_".join(dtosave)
    modsm.to_csv(dtosave, sep="\t")
    
      
##SWE from BR##
    #import the swe
    swebr= pd.read_csv("E:/Dissertation/Modeling/ech2o/observation_data/bogusfilledswe.csv")
    swebr['DateTime'] = pd.to_datetime(swebr['DateTime'])
    
    modswe= pd.read_table("E:/Dissertation/Modeling/ech2o/Results/SWE.tab", sep="\t", index_col=0, skiprows=8,
                    names = ['p2', 'p1', 'p5', 'p3', 'p4', 'N'], header=None)
    
    modswe["dt"]= pd.date_range(start="2015-10-01",end="2019-9-30")
    modswe['dt'] = modswe['dt'].dt.strftime('%Y-%m-%d')
    modswe['dt']=pd.to_datetime(modswe['dt'], errors = 'coerce')
    
    mod_meas= modswe.merge(swebr, left_on = 'dt', right_on='DateTime')
    mod_meas['dt'] =pd.to_datetime(mod_meas['dt'], errors = 'coerce')
   

#calculate the NSE or KGE
    def nse(predictions, targets):
        return (1-(np.sum((predictions-targets)**2)/np.sum((targets-np.mean(targets))**2)))

    obj_swe= nse(mod_meas['p2'], mod_meas['br_swe'])
    
#calculate the KGE
    #kge_calc_swe = he.evaluator(he.kge, mod_meas['p5'], mod_meas['br_swe']) #non parametric
    kge_calc_swe = kge(mod_meas['p2'], mod_meas['br_swe']) #mod, meas from function below
    #print("objective function kge", kge_calc)
    # store the objective function 
    list_of_nse_swe.append(obj_swe)
    list_of_kge_swe.append(kge_calc_swe)

#save the model output elsewhere
    moment=time.strftime("%Y%b%d__%H_%M_%S", time.localtime())
    dtosave= ["E:/Dissertation/Modeling/ech2o/Results/mc/swe_calib", moment, ".tab"]
    dtosave="_".join(dtosave)
    modswe.to_csv(dtosave, sep="\t")
    
    
    
##pereto front objective###
    #obj = math.sqrt((obj_q-1)**2 + (obj_t-1)**2) #nse
    #kge_calc = math.sqrt((kge_calc_q[0]-1)**2 + (kge_calc_t[0]-1)**2) #kge
    obj= 1 * (1-obj_q) + 1* (1-obj_t) + 1* (1-obj_t_tl) + 1* (1-obj_sm) + 1*(1-obj_swe) #nse
    #kge_calc= 1*(kge_calc_q[0]-1) + 1*(kge_calc_t[0]-1) + 1*(kge_calc_sm[0]-1) + 1*(kge_calc_swe[0]-1) 
    #kge_calc= 1*(1-kge_calc_q) + 1*(1-kge_calc_t) + 1*(1-kge_calc_t_tl) + 1*(1-kge_calc_sm) + 1*(1-kge_calc_swe)
    kge_calc= 1*(1-kge_calc_q) + 1*(1-kge_calc_t) + 1*(1-kge_calc_sm) + 1*(1-kge_calc_swe)

    list_of_obj_funcs.append(obj)
    list_of_kge_obj.append(kge_calc) 

    pd.DataFrame(list_of_kge_obj).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_obj.csv') #savee to monitor
    pd.DataFrame(list_of_nse_stream).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_stream.csv') #savee to monitor
    pd.DataFrame(list_of_obj_funcs).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_obj.csv')
    pd.DataFrame(list_of_params).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/params_values.csv')
    pd.DataFrame(list_of_params_txt).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/params_names.csv')
    pd.DataFrame(list_of_kge_transp).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_trans.csv')
    pd.DataFrame(list_of_kge_transp_tl).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_trans_tl.csv')
    pd.DataFrame(list_of_kge_stream).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_stream.csv')
    pd.DataFrame(list_of_nse_transp).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_trans.csv')
    pd.DataFrame(list_of_nse_transp_tl).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_trans_tl.csv')
    pd.DataFrame(list_of_nse_sm).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_sm.csv')
    pd.DataFrame(list_of_nse_swe).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_swe.csv')
    pd.DataFrame(list_of_kge_swe).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_swe.csv')
    pd.DataFrame(list_of_kge_sm).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_sm.csv')
    
    
    obj_func= float(kge_calc) #change to nse if desired
    print("objective function kge", obj_func)
    return(obj_func) 
    #remove the results file cause it causes an error to overwrite
    #os.remove('E:/Dissertation/Modeling/ech2o/Results/SWE.TAB')    
print("model ran, objective function saved")


#%%
#input is the calibration table with just the species params values
def change_table(calibtable_tble):
    with open("C:\ech2o\Documentation\dry_data\Spatial\SpeciesParams_temp.txt", "r") as a:
        spc=a.read()
    #want to adjust the canopy water paramter
    #assuming uniform values for now...
#replace the values in the file with the value from dds
    #loop through the calibtable_tble
    for i in range(len(calibtable_tble)):
        list_of_params_txt.append(calibtable_tble['op'][i]) #record what we are looking at
        list_of_params.append(calibtable_tble['value'][i])
        #var1-3 are for max can storage
        if calibtable_tble['op'].str.contains('var1')[i]:
            v= calibtable_tble['value'][i] 
            sp_replaced= spc.replace("var1", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var2')[i]:
            v= calibtable_tble['value'][i] 
            sp_replaced= sp_replaced.replace("var2", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var3')[i]:
            v= calibtable_tble['value'][i] 
            sp_replaced= sp_replaced.replace("var3", str(v)) #replace the place holder with the new value v
        #var 4-6 are kbeers- if can storage gets skipped then need to change the sp_replaced in first one.
        if calibtable_tble['op'].str.contains('var4')[i]:
            v= round(calibtable_tble['value'][i],6) 
            sp_replaced= sp_replaced.replace("var4", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var5')[i]:
            v= round(calibtable_tble['value'][i], 6)
            sp_replaced= sp_replaced.replace("var5", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var6')[i]:
            v= round(calibtable_tble['value'][i], 6)
            sp_replaced= sp_replaced.replace("var6", str(v)) #replace the place holder with the new value v
        #var 7-9 are gsmax- if can storage and kbeers gets skipped then need to change the sp_replaced in first one.
        if calibtable_tble['op'].str.contains('var7')[i]:
            v= round(calibtable_tble['value'][i], 6)
            sp_replaced= sp_replaced.replace("var7", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var8')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            sp_replaced= sp_replaced.replace("var8", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('var9')[i]:
            v= round(calibtable_tble['value'][i], 6)
            sp_replaced= sp_replaced.replace("var9", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari10')[i]:
            v= round(calibtable_tble['value'][i], 6)
            sp_replaced= sp_replaced.replace("vari10", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari11')[i]:
            v= round(calibtable_tble['value'][i], 6)
            if v<0.5:
                v=2.5
            sp_replaced= sp_replaced.replace("vari11", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari12')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            if v<8:
                v=8.1
            sp_replaced= sp_replaced.replace("vari12", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari13')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            if v<40:
                v=40
            sp_replaced= sp_replaced.replace("vari13", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari14')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            if v>8:
                v=8
            sp_replaced= sp_replaced.replace("vari14", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari15')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            sp_replaced= sp_replaced.replace("vari15", str(v)) #replace the place holder with the new value v
            
        if calibtable_tble['op'].str.contains('vari16')[i]:
            v= round(calibtable_tble['value'][i], 20) 
            sp_replaced= sp_replaced.replace("vari16", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari17')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            sp_replaced= sp_replaced.replace("vari17", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari18')[i]:
            v= round(calibtable_tble['value'][i], 6) 
            sp_replaced= sp_replaced.replace("vari18", str(v)) #replace the place holder with the new value v 
        if calibtable_tble['op'].str.contains('vari19')[i]:
            v= round(calibtable_tble['value'][i], 20) 
            sp_replaced= sp_replaced.replace("vari19", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari20')[i]:
            v= round(calibtable_tble['value'][i], 20) 
            sp_replaced= sp_replaced.replace("vari20", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari21')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari21", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari22')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari22", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari23')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari23", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari24')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari24", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari25')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari25", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari26')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari26", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari27')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari27", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari28')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari28", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari29')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari29", str(v)) #replace the place holder with the new value v
        if calibtable_tble['op'].str.contains('vari30')[i]:
            v= round(calibtable_tble['value'][i], 15) 
            sp_replaced= sp_replaced.replace("vari30", str(v)) #replace the place holder with the new value v
        
#save the file
    with open("C:\ech2o\Documentation\dry_data\Spatial\SpeciesParams.txt", "w") as i:
        i.write(sp_replaced)
     

#%%
os.chdir("E:\Dissertation\Modeling\python")   
print(os.getcwd())

from dds import *

#bring in the paramter bounds table
pdf = pd.read_table("C:\ech2o\Documentation\dry_data\Spatial\params_bounds2.txt",sep= "\t")   
pdf["BestValue"] = pdf["Init"]
pdf["ThisValue"] = pdf["Init"]
pdf = pdf.set_index("Parameter")


def kge(mod, obs):
    #
    #obs=obs.replace([np.inf, -np.inf], np.nan).drop.na()
    #mod=mod.replace([np.inf, -np.inf], np.nan).drop.na()
    
    mobs = np.mean(obs)
    sobs = np.std(obs)

    # mean ratio
    b = np.mean(mod) / mobs
    # std
    a = np.std(mod) / sobs
    # corr coeff
    r = np.corrcoef(mod, obs)[0, 1]  # corrcoef returns the correlation matrix...
    # the diagonals are 1, the off-diags are the 'r'
    # value that we want
    kgeval = 1-np.sqrt((r - 1.)**2 + (a - 1.)**2 + (b - 1)**2)
    return kgeval

#best_kge_score = 0.9 #iniate the kge score

#initiate some lists to store variables

list_of_obj_funcs = []
list_of_params = []
list_of_params_txt = []
list_of_kge_obj=[]
list_of_kge_transp=[]
list_of_kge_transp_tl=[]
list_of_kge_stream=[]
list_of_kge_sm=[]
list_of_kge_swe=[]
list_of_nse_transp=[]
list_of_nse_transp_tl=[]
list_of_nse_stream=[]
list_of_nse_sm=[]
list_of_nse_swe=[]
list_of_clonefiles=[]

#%%
#run dds with the below function

##dds input:
#the pdf is the file with the bounds
#fx is the function- calib function that takes the x0 parameter set
#max iterations- when to stop and say good enough

os.chdir("C:\\ech2o\\") 

DDS(pdf, calib, 2000)

#%%
#calibtable= pd.read_table("C:\ech2o\Documentation\dry_data\Spatial\optimize_params.txt",sep= "\t", 
 #                         header = None, names=['op', 'fctor', 'operation', 'type'])
'''
#to connect to DDS:
- bring in the x0 file with the new parameters. These are in the same order as the calibration parameter file. 
- change the values in the map or tables
- run the model and output the objective function
'''
pd.DataFrame(list_of_kge_obj).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_obj.csv')
pd.DataFrame(list_of_obj_funcs).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_obj.csv')
pd.DataFrame(list_of_params).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/params_values.csv')
pd.DataFrame(list_of_params_txt).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/params_names.csv')
pd.DataFrame(list_of_kge_transp).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_trans.csv')
pd.DataFrame(list_of_kge_stream).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/kge_stream.csv')
pd.DataFrame(list_of_nse_transp).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_trans.csv')
pd.DataFrame(list_of_nse_stream).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_stream.csv')
pd.DataFrame(list_of_nse_sm).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_sm.csv')
pd.DataFrame(list_of_nse_swe).to_csv('E:/Dissertation/Modeling/ech2o/Results/mc/nse_swe.csv')