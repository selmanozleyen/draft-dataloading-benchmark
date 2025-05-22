# create a dense a dense zarr dataset
python create_data.py --data-path benchmarks/data/synthetic_data_dense.zarr --chunk-size 4096 

# convert the dense zarr dataset to a sparse h5ad dataset
python convert_data.py --data-path benchmarks/data/synthetic_data_dense.zarr --output-path benchmarks/data/synthetic_data_sparse.h5ad --sparse

# convert the sparse h5ad dataset to a sparse zarr dataset
python convert_data.py --data-path benchmarks/data/synthetic_data_sparse.h5ad --output-path benchmarks/data/synthetic_data_sparse.zarr --sparse

# convert the sparse zarr dataset to a dense h5ad dataset
python convert_data.py --data-path benchmarks/data/synthetic_data_sparse.zarr --output-path benchmarks/data/synthetic_data_dense.h5ad
