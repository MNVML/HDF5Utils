#!/usr/bin/env python
"""
Usage:
    python capper.py <input file> <cap string> <cap value>

Choose a dataset in the HDF5 file, e.g., "hadro_data/n_hadmultmeas", and a
cap value (cast as an `int`) and set every value in the dataset _greater than_
the cap value to be _equal to_ the cap value.

The output file name is the input name with 'capped' appended just before the
file type extension.

Warning - this script might have trouble on very large HDF5s.
"""
from __future__ import print_function
import h5py
import numpy as np
import os
import sys


if '-h' in sys.argv or '--help' in sys.argv:
    print(__doc__)
    sys.exit(1)

if not len(sys.argv) == 4:
    print(__doc__)
    sys.exit(1)

input_hdf5_file = sys.argv[1]
output_hdf5_file = '.'.join(input_hdf5_file.split('.')[:-1]) + 'capped.hdf5'
capstring = sys.argv[2]
capvalue = int(sys.argv[3])


def prepare_hdf5_file(hdf5file):
    if os.path.exists(hdf5file):
        os.remove(hdf5file)
    f = h5py.File(hdf5file, 'w')
    return f


fin = h5py.File(input_hdf5_file, 'r')
fout = prepare_hdf5_file(output_hdf5_file)

# prep the structure of the ouptut hdf5
for group in fin:
    print('making fout group {}...'.format(group))
    grp = fout.create_group(group)
    for dset in fin[group]:
        shp = list(np.shape(fin[group][dset]))
        dtyp = fin[group][dset].dtype
        print('  making fout dset {} with shape {} and dtyp {}...'.format(
            dset, shp, dtyp
        ))
        grp.create_dataset(dset, shp, dtype=dtyp, compression='gzip')

# copy the data in the input hdf5 to the output hdf5, but cap the values for
# the specified dataset.
for group in fin:
    for dset in fin[group]:
        print('filling {}/{}'.format(group, dset))
        if group + '/' + dset == capstring:
            arr = fin[group][dset][:]
            arr[arr > capvalue] = capvalue
            fout[group][dset][:] = arr
        else:
            fout[group][dset][:] = fin[group][dset][:]

fin.close()
fout.close()
