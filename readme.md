Env setup
```
mamba create -n dataloading python=3.11
mamba activate dataloading
mamba install conda-build
pip install asv torch
pip install git+https://github.com/scverse/anndata.git
```

To run the simple case
```
# first create data
python create_data.py
# then run
python simple_run.py # --help
```
