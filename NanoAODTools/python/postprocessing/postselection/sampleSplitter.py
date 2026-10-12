import ROOT
# ROOT.EnableImplicitMT()
ROOT.gStyle.SetOptStat(0)
import sys
import os
import optparse
import json
import numpy as np
import math
import shutil
from datetime import datetime
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
sys.path.append('../')

usage="python3 splitSamples.py -d dataset -s sample --partsize number_of_files_per_job"
parser                  = optparse.OptionParser(usage)
parser.add_option('-d', '--datasets',           dest='datasets',            type=str,               default="TT_2024",                             help='Datasets to process, in the form: QCD_2023,TT_2023...')
parser.add_option('-s', '--sample',           dest='sample',            type=str,               default="TT_semilep_2024",                             help='Datasets to process, in the form: QCD_2023,TT_2023...')

parser.add_option(      '--dict_samples_file',  dest='dict_samples_file',   type=str,               default="../samples/dict_samples_2024_acp.json",    help='Path to the JSON file containing the sample definitions')
parser.add_option(      '--partsize',       dest='partsize',        type=int,    default=-1,                                  help='size of the dataset portion to get. To use if you are doing the a-priori splitting option, together with npart ')

parser.add_option(      '--npart',       dest='npart',        type=int,    default=1,                                  help='sequential number of the dataset to get. To use if you are doing the a-priori splitting option, together with npart')
(opt, args)             = parser.parse_args()


njobsperpart= opt.partsize
samp = opt.sample
dat = opt.datasets
dict_samples_file = opt.dict_samples_file
#### LOAD samples.py ####
with open(dict_samples_file, "rb") as sample_file:
    samples = json.load(sample_file)





datasets = []
in_d              = opt.datasets
if not in_d in sample_dict.keys():
    print("Check the in_dataset string... ", sample_dict.keys())
else: 
    datasets.append(sample_dict[in_d])
print("Datasets to process: ", [d.label for d in datasets])


def sampleSplitter(samplesfile, sample,dataset,njobs_per_part ):

    
    print("dataset ", dataset.label, "has components? ",hasattr(dataset, "components")  )
    if hasattr(dataset, "components"):
        comps        = dataset.components
        comp_list = [s.label for s in comps]
        if not (sample in comp_list):
            print(f"sample {sample} not in dataset{dataset.label}, check they match!")
            return
    else:
        if sample != dataset.label:
            print(f"sample {sample} does not correspond to dataset{dataset.label}, check they match!")


            #    print(samples)
    
    totfiles=len(samplesfile[dataset.label][sample]['strings'])
    if (njobs_per_part==-1):
        return 1,totfiles

    nparts = int(totfiles/njobs_per_part)+1
    print("njobs_per_part is ",njobs_per_part," totfiles is ", totfiles," --> nparts is " , nparts)
    lenlastpart=totfiles-njobs_per_part*(nparts-1)
    print("len last part is: ", lenlastpart )
    return nparts, lenlastpart 

#sampleSplitter(samp,datasets[0],njobsperpart)
