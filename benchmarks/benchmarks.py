import os
import multiprocessing as _mp
_mp.set_start_method("spawn", force=True)

from .project.loading import read_lazy, ZarrDataset
from torch.utils.data import DataLoader

DATA_PATH = os.path.expanduser("~/projects/dataloading-benchmark/benchmarks/data/synthetic_data.zarr")

class TimeSuite:

    def setup(self):
        # keep only the path around
        self.path = DATA_PATH

    def time_dataloader(self):
        adata = read_lazy(self.path)
        ds = ZarrDataset(adata, "cell_type")
        for x in ds:
            pass

    def time_dataloader_torch(self):
        adata = read_lazy(self.path)
        ds = ZarrDataset(adata, "cell_type")
        loader = DataLoader(
            ds,
            batch_size=2,
            num_workers=4,
            persistent_workers=True,
            pin_memory=False
        )
        for x in loader:
            pass
