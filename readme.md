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
❯ python simple_run.py --data-path=/Users/selman.ozleyen/projects/draft-dataloading-benchmark/benchmarks/data/synthetic_data_sparse.zarr
adata.X shape: (541200, 50)
adata.X type: <class 'dask.array.core.Array'>
Average batch size: 124.98845265588915
Average batch time: 0.00027976460049389143 seconds (+/- 0.0013937197356093348 seconds)
Average time per element: 2.2383235774917773e-06 seconds
Total time: 1.2113807201385498 seconds
Number of iterations: 4330
```

