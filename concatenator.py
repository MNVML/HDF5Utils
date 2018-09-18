#!/usr/bin/env python
'''
Usage:
    python concatenator.py <hdf5 file 1> <hdf5 file 2> <output name>

Concatenate two HDF5 files into one. The second file is effectively appended
to the first and the combination is written to the output file.

Warning - this script might have trouble on very large HDF5s.
'''
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

input_hdf5_file1 = sys.argv[1]
input_hdf5_file2 = sys.argv[2]
output_hdf5_file = sys.argv[3]


def prepare_hdf5_file(hdf5file):
    if os.path.exists(hdf5file):
        os.remove(hdf5file)
    f = h5py.File(hdf5file, 'w')
    return f


fin1 = h5py.File(input_hdf5_file1, 'r')
fin2 = h5py.File(input_hdf5_file2, 'r')
fout = prepare_hdf5_file(output_hdf5_file)


struct_dict = {}

for group in fin1:
    struct_dict[group] = {}
    for dset in fin1[group]:
        struct_dict[group][dset] = {}
        shp = list(np.shape(fin1[group][dset]))
        dtyp = fin1[group][dset].dtype
        struct_dict[group][dset]['shp1'] = shp
        struct_dict[group][dset]['dtyp'] = dtyp

for group in fin2:
    for dset in fin2[group]:
        shp = list(np.shape(fin2[group][dset]))
        dtyp = fin2[group][dset].dtype
        assert struct_dict[group][dset]['shp1'][1:] == shp[1:]
        assert struct_dict[group][dset]['dtyp'] == dtyp
        struct_dict[group][dset]['shp2'] = shp

print(struct_dict)

for group in struct_dict:
    print('making fout group {}...'.format(group))
    grp = fout.create_group(group)
    for dset in struct_dict[group]:
        dtyp = struct_dict[group][dset]['dtyp']
        shp1 = struct_dict[group][dset]['shp1']
        shp2 = struct_dict[group][dset]['shp2']
        new_shp = shp1[:]
        new_shp[0] = shp1[0] + shp2[0]
        print('  making fout dset {} with shape {} and dtyp {}...'.format(
            dset, new_shp, dtyp
        ))
        grp.create_dataset(dset, new_shp, dtype=dtyp, compression='gzip')
        fout[group][dset][0:shp1[0]] = fin1[group][dset][:]
        fout[group][dset][shp1[0]:] = fin2[group][dset][:]

fin1.close()
fin2.close()
fout.close()
