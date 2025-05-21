Env setup
```
mamba create -n dataloading python=3.11
mamba activate dataloading
pip install -e .
```

To run the simple case
```
# first create data
python create_data.py --data-path=/Users/selman.ozleyen/projects/draft-dataloading-benchmark/benchmarks/data/synthetic_data_sparse.zarr --sparse --cells-per-condition=1000

python create_data.py --data-path=/Users/selman.ozleyen/projects/draft-dataloading-benchmark/benchmarks/data/synthetic_data_dense.zarr --cells-per-condition=1000

>   return dispatch(args[0].__class__)(*args, **kw)
{'adata': AnnData object with n_obs × n_vars = 541200 × 50
    obs: 'control', 'cell_type', 'drug', 'dosage', 'batch'
    uns: 'drug', 'cell_type', 'batch', 'sample_rep': 'X', 'control_key': 'control', 'split_covariates': ['cell_type', 'batch'], 'perturbation_covariates': {'drug': ['drug'], 'dosage': ['dosage']}, 'perturbation_covariate_reps': {'drug': 'drug'}, 'sample_covariates': ['cell_type', 'batch'], 'sample_covariate_reps': {'cell_type': 'cell_type', 'batch': 'batch'}}
```



To run the simple case
```
❯ python simple_run.py --data-path=/Users/selman.ozleyen/projects/draft-dataloading-benchmark/benchmarks/data/synthetic_data_sparse.zarr --batch-size=128
adata.X shape: (541200, 50)
adata.X type: <class 'dask.array.core.Array'>

--------------------------------[Timing Results]--------------------------------
Total time:              1.64 s
Total samples:        541,200
Number of batches:      4,330
Avg time/element:        3.03 μs
Throughput:          330,490.9 samples/s
--------------------------------------------------------------------------------
❯ python simple_run.py --data-path=/Users/selman.ozleyen/projects/draft-dataloading-benchmark/benchmarks/data/synthetic_data_sparse.zarr --batch-size=128
adata.X shape: (541200, 50)
adata.X type: <class 'dask.array.core.Array'>

--------------------------------[Timing Results]--------------------------------
Total time:              1.17 s
Total samples:        541,200
Number of batches:      4,330
Avg time/element:        2.17 μs
Throughput:          461,799.7 samples/s
--------------------------------------------------------------------------------
```

