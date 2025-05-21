import time
from benchmarks.project.loading import read_lazy, BatchedZarrDataset
from torch.utils.data import DataLoader
import numpy as np
import argparse
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str)
    parser.add_argument("--torch", action="store_true")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--n-chunks", type=int, default=4)
    parser.add_argument("--shuffle", action="store_true")

    args = parser.parse_args()
    data_path = Path(args.data_path)
    assert data_path.exists(), f"Data path {data_path} does not exist"
    adata = read_lazy(data_path)
    print("adata.X shape:", adata.X.shape)
    print("adata.X type:", type(adata.X))
    loader = BatchedZarrDataset(adata, "cell_type", args.batch_size, args.n_chunks, args.shuffle)
    if args.torch:
        loader = DataLoader(
            loader,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            persistent_workers=False,
            pin_memory=False
        )
    time0 = time.time()
    batch_times = []
    batch_sizes = []
    for x in loader:
        batch_times.append(time.time() - time0)
        batch_sizes.append(x[0].shape[0] if not args.torch else len(x[0])) # also to make sure it is not optimized out
        time0 = time.time()
    # give in plus and minus
    avg_batch_size = sum(batch_sizes)/(len(batch_sizes) * 1.0)
    print(f"Average batch size: {avg_batch_size}")
    print(f"Average batch time: {sum(batch_times)/len(batch_times)} seconds (+/- {np.std(batch_times)} seconds)")
    print(f"Total time: {sum(batch_times)} seconds")
    print(f"Number of samples: {sum(batch_sizes)}")
    print(f"Number of iterations: {len(batch_times)}")
    print(f"Average time per element: {sum(batch_times)/(len(batch_times) * avg_batch_size)} seconds")
    print(f"Samples per second: {sum(batch_sizes)/sum(batch_times)}")