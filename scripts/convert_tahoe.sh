#! /bin/bash

# take data-path as first argument
data_path=$1

# strip the extension from the data-path
data_path_no_ext=${data_path%.*}

# convert to zarr
zarr_dense_path=${data_path_no_ext}_dense.zarr
zarr_sparse_path=${data_path_no_ext}_sparse.zarr

h5ad_dense_path=${data_path_no_ext}_dense.h5ad
h5ad_sparse_path=${data_path_no_ext}_sparse.h5ad

# convert to dense zarr
python convert_data.py --data-path $data_path --output-path $zarr_dense_path --chunk-size 4096

# convert to sparse zarr
python convert_data.py --data-path $data_path --output-path $zarr_sparse_path --chunk-size 4096 --sparse

# convert to dense h5ad
python convert_data.py --data-path $data_path --output-path $h5ad_dense_path --sparse

# convert to sparse h5ad
python convert_data.py --data-path $data_path --output-path $h5ad_sparse_path --sparse






