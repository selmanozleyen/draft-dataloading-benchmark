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
    output_path = Path(data_path.parent, data_path.stem + ".zarr" if data_path.suffix == ".h5ad" else data_path.with_suffix(".zarr"))
    if output_path.suffix == ".h5ad":
        adata.write_h5ad(output_path)
    else:
        adata.write_zarr(output_path, chunks=chunks)
    print("Wrote adata to", output_path)
