# HDF5 Utility Scripts

Collection of utility scripts for HDF5.

* `capper.py` - Choose a dataset in the HDF5 file, e.g., "hadro_data/n_hadmultmeas", and a cap value (cast as an `int`) and set every value in the dataset _greater than_ the cap value to be _equal to_ the cap value.
* `concatenator.py` - Concatenate two HDF5 files into one. The second file is effectively appended to the first and the combination is written to the output file.
* `examine_hdf5.py` - Print the groups and datasets in an HDF5 along with some sampled information about the values in those datasets (the values shown are samples, and are not exact for the full dataset).
