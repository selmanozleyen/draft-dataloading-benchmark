import argparse
from dl_benchmark.utils import concatenate_zarr_files


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Concatenate multiple zarr files into a single zarr file"
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=str,
        help="List of zarr file paths to concatenate"
    )
    parser.add_argument(
        "--output-path",
        "-o",
        type=str,
        default="concatenated.zarr",
        help=(
            "Path where the concatenated zarr file will be saved "
            "(default: concatenated.zarr)"
        )
    )

    args = parser.parse_args()
    output_path = args.output_path
    if output_path is None:
        output_path = "concatenated.zarr"
    concatenate_zarr_files(
        paths=args.paths,
        output_path=output_path,
    )
