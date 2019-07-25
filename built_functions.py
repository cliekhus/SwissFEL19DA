import h5py
import numpy as np

import jungfrau_utils as ju

from .channels import *
from .utils import crop_roi, make_roi

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
