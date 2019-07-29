import h5py
import numpy as np

import jungfrau_utils as ju

from alvra_tools.channels import *
from alvra_tools.utils import crop_roi, make_roi

def get_xes_croped(filename, DIR, DIRBS, roi, numstds=2, minIzero=0.002, imageThreshold=1.5, hotpixel=7.5):

    images, _ = load_JF_cropped_data(DIR + filename + ".JF02T09V02crop.h5" , roi, nshots=None)

    print(DIR + filename + ".JF02T09V02crop.h5")
    print(DIRBS + filename + ".BSREAD.h5")

    (_, _, IzeroFEL, _, _, _, Energy, _, _, _ )\
        = load_PumpProbe_events_withTwoVariables(DIRBS + filename + ".BSREAD.h5", channel_BS_pulse_ids, channel_energy)

    total = 0


    IzeroMedian = np.median(IzeroFEL)
    IzeroSTD = np.std(IzeroFEL)

    nframes = images.shape

    IzeroMedian = np.median(IzeroFEL)
    IzeroSTD = np.std(IzeroFEL)

    print('number of frames')
    print(nframes)

    images_good = images

    images_thr = images_good.copy()
    images_thr[images_good < image_threshold] = 0
    images_thr[images_good > hot_pixel] = 0

    conditionMax = IzeroFEL < IzeroMedian+numstds*IzeroSTD
    conditionMin = IzeroFEL > IzeroMedian-numstds*IzeroSTD
    conditionLow = IzeroFEL > minIzero
    condition = np.logical_and.reduce((conditionLow, conditionMin, conditionMax)).T[0]

    images_thr = images_thr[condition]

    print('number of surviving frames')
    print(images_thr.shape[0])

    XES = images_thr.sum(axis=0)/images_thr.shape[0]

    print("XES size")
    print(XES.shape)

    return XES


# Python program to convert a list 
# of character 
  
def list2Str(s): 
  
    # initialization of string to "" 
    new = "" 
    # traverse in the string  
    for x in s: 
        new += '_'
        new += str(x)
  
    # return string  
    return new 



def filterData(IzeroFEL_pump, IzeroFEL_unpump, DataFluo_pump, DataFluo_unpump, numstds, minIzero, lin_filter):
#    numstds = 3
#minIzero = 0.025
#lin_filter = 0.1

        if DataFluo_pump.ndim == 2 and DataFluo_pump.shape[1]==1:
            DataFluo_pump = DataFluo_pump.T[0]
            DataFluo_unpump = DataFluo_unpump.T[0]
            IzeroFEL_pump = IzeroFEL_pump.T[0]
            IzeroFEL_unpump = IzeroFEL_unpump.T[0]
        
        IzeroMedian = np.median(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))
        IzeroSTD = np.std(np.concatenate([IzeroFEL_pump, IzeroFEL_unpump]))

        #apply filter to points which are not linear
        linFit_pump = np.polyfit(IzeroFEL_pump,DataFluo_pump,1)
        linFit_unpump = np.polyfit(IzeroFEL_unpump,DataFluo_unpump,1)
        
        
        conditionPumpLinHigh =  DataFluo_pump < IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]+lin_filter
        conditionPumpLinLow =  DataFluo_pump > IzeroFEL_pump*linFit_pump[0]+linFit_pump[1]-lin_filter
        
        conditionUnPumpLinHigh =  DataFluo_unpump < IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]+lin_filter
        conditionUnPumpLinLow =  DataFluo_unpump > IzeroFEL_unpump*linFit_unpump[0]+linFit_unpump[1]-lin_filter
        
        condLin_pump =  conditionPumpLinHigh & conditionPumpLinLow
        condLin_unpump = conditionUnPumpLinHigh & conditionUnPumpLinLow


        conditionPumpMax = IzeroFEL_pump < IzeroMedian+numstds*IzeroSTD
        conditionPumpMin = IzeroFEL_pump > IzeroMedian-numstds*IzeroSTD
        conditionPumpLow = IzeroFEL_pump > minIzero

        conditionUnPumpMax = IzeroFEL_unpump < IzeroMedian+numstds*IzeroSTD
        conditionUnPumpMin = IzeroFEL_unpump > IzeroMedian-numstds*IzeroSTD
        conditionUnPumpLow = IzeroFEL_unpump > minIzero

        condIzeroPump = conditionPumpMax & conditionPumpMin & conditionPumpLow
        condIzeroUnPump = conditionUnPumpMax & conditionUnPumpMin & conditionUnPumpLow
        
        
        condFinalPump = condLin_pump & condIzeroPump
        condFinalUnPump = condLin_unpump & condIzeroUnPump
        
        #update Fluo and Izero    

        IzeroFEL_pump = IzeroFEL_pump[condFinalPump]
        IzeroFEL_unpump = IzeroFEL_unpump[condFinalUnPump]
    
        DataFluo_pump = DataFluo_pump[condFinalPump]
        DataFluo_unpump = DataFluo_unpump[condFinalUnPump]


        return IzeroFEL_pump, IzeroFEL_unpump, DataFluo_pump, DataFluo_unpump, condFinalPump, condFinalUnPump



def err_adder (Ea, Eb):
    Ea = Ea*Ea
    Eb = Eb*Eb
    Eab = Ea+Eb
    Eab = np.sqrt(Eab)
    return Eab













