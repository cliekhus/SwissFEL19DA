#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 03:36:46 2019

@author: ext-liekhussc_c
"""

import h5py

DIR = '/sf/alvra/data/p17983/raw/2850eV_pink/'

filename1 = 'run_000006.JF02T09V02.h5'
filename2 = 'run_000006.JF06T04V01.h5'

data1 = h5py.File(DIR + filename1)
data2 = h5py.File(DIR + filename2)

pulse_id = list(data1['data/JF02T09V02/pulse_id'])
data1 = list(data1['data/JF02T09V02/data'])