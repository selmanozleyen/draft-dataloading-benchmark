import argparse
from pathlib import Path

from dl_benchmark.utils import convert_format

if __name__ == "__main__":
    # Example usage
    parser = argparse.ArgumentParser(description="Convert h5ad to Zarr")
    parser.add_argument("--data-path", type=str, default="benchmarks/data/synthetic_data.zarr")
    parser.add_argument("--output-path", type=str, default="benchmarks/data/synthetic_data.h5ad")
    parser.add_argument("--chunk-size", type=int, default=4096)
    parser.add_argument("--sparse", action="store_true")

    args = parser.parse_args()

    data_path = Path(args.data_path)
    output_path = Path(args.output_path)
    convert_format(data_path, output_path, args.chunk_size, args.sparse)
