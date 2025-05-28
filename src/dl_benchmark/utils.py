import anndata as ad
import zarr
import scipy.sparse as sp
from pathlib import Path


def convert_format(data_path, chunk_size):
    data_path = Path(data_path)
    assert data_path.exists()
    assert data_path.suffix == ".h5ad" or data_path.suffix == ".zarr"

    if data_path.suffix == ".h5ad":
        adata = ad.read_h5ad(data_path, backed="r")
    else:
        group = zarr.open(data_path, mode="r")
        adata = ad.AnnData(
            X=ad.experimental.read_elem_lazy(group["X"]),
            obs=ad.io.read_elem(group["obs"]),
        )
    print("Read adata:", adata)

    chunks = chunk_size
    output_path = Path(
        data_path.parent, data_path.stem + ".zarr" if data_path.suffix == ".h5ad" else data_path.with_suffix(".zarr")
    )
    if output_path.suffix == ".h5ad":
        adata.write_h5ad(output_path)
    else:
        adata.write_zarr(output_path, chunks=chunks)
    print("Wrote adata to", output_path)


def concatenate_zarr_files(paths: list[str | Path], output_path: str | Path) -> None:
    """Concatenate multiple zarr files on disk using anndata.concat_on_disk.

    Args:
        paths: List of paths to zarr files to concatenate
        output_path: Path where the concatenated zarr file will be saved
    """
    # Convert all paths to Path objects and resolve them
    zarr_paths = [Path(p).resolve() for p in paths]
    # Verify all paths exist
    for path in zarr_paths:
        if not path.exists():
            raise ValueError(
                f"Path does not exist: {path}"
            )

    output_path = Path(output_path).resolve()
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    print(zarr_paths)
    print(output_path)
    ad.experimental.concat_on_disk(
        zarr_paths,
        output_path,
    )
    print(
        f"Concatenated {len(zarr_paths)} files into {output_path}"
    )
