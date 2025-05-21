# taken from https://github.com/laminlabs/modlyn/blob/main/modlyn/io/loading.py
# will be added as dependency after development

import random

import anndata as ad
import numpy as np
import zarr
from torch.utils.data import IterableDataset


def read_lazy(path):
    g = zarr.open(path, mode="r")
    adata = ad.AnnData(
        X=ad.experimental.read_elem_lazy(g["X"]), obs=ad.io.read_elem(g["obs"])
    )

    return adata


def _combine_chunks(lst, chunk_size):
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def _yield_samples(x, y, shuffle=True):
    num_samples = len(x)
    indices = np.arange(num_samples)
    if shuffle:
        np.random.shuffle(indices)  # noqa: NPY002

    for i in indices:
        yield x[i], y[i]


class ZarrDataset(IterableDataset):
    def __init__(
        self,
        adata: ad.AnnData,
        label_column: str,
        n_chunks: int = 16,
        shuffle: bool = True,
    ):
        self.adata = adata
        self.label_column = label_column
        self.n_chunks = n_chunks
        self.shuffle = shuffle

    def _get_chunks(self):
        chunk_boundaries = np.cumsum([0] + list(self.adata.X.chunks[0]))
        slices = [
            slice(int(start), int(end))
            for start, end in zip(chunk_boundaries[:-1], chunk_boundaries[1:])
        ]
        blocks_idxs = np.arange(len(self.adata.X.chunks[0]))
        assert len(slices) == len(blocks_idxs)  # noqa: S101
        chunks = list(zip(blocks_idxs, slices))
        if self.shuffle:
            random.shuffle(chunks)

        return chunks

    def __iter__(self):
        for chunks in _combine_chunks(self._get_chunks(), self.n_chunks):
            block_idxs, slices = zip(*chunks)
            x = self.adata.X.blocks[list(block_idxs)].compute(scheduler="threads")
            obs = self.adata.obs[self.label_column].iloc[np.r_[slices]].to_numpy()
            yield from _yield_samples(x, obs, self.shuffle)

    def __len__(self):
        return len(self.adata)

def _yield_chunks_batched(x, y, batch_size, shuffle=True):
    num_samples = x.shape[0] # for sparse compatibility
    indices = np.arange(num_samples)
    if shuffle:
        np.random.shuffle(indices)  # noqa: NPY002

    for i in range(0, num_samples, batch_size):
        yield x[indices[i:i+batch_size]], y[indices[i:i+batch_size]]


class BatchedZarrDataset(IterableDataset):
    def __init__(
        self,
        adata: ad.AnnData,
        label_column: str,
        batch_size: int,
        n_chunks: int = 2,
        shuffle: bool = True,
    ):
        self.adata = adata
        self.label_column = label_column
        self.batch_size = batch_size
        self.n_chunks = n_chunks
        self.shuffle = shuffle

    def _get_chunks(self):
        chunk_boundaries = np.cumsum([0] + list(self.adata.X.chunks[0]))
        slices = [
            slice(int(start), int(end))
            for start, end in zip(chunk_boundaries[:-1], chunk_boundaries[1:])
        ]
        blocks_idxs = np.arange(len(self.adata.X.chunks[0]))
        assert len(slices) == len(blocks_idxs)  # noqa: S101
        chunks = list(zip(blocks_idxs, slices))
        if self.shuffle:
            random.shuffle(chunks)

        return chunks

    def __iter__(self):
        for chunks in _combine_chunks(self._get_chunks(), self.n_chunks):
            block_idxs, slices = zip(*chunks)
            x = self.adata.X.blocks[list(block_idxs)].compute(scheduler="threads")
            obs = self.adata.obs[self.label_column].iloc[np.r_[slices]].to_numpy()
            yield from _yield_chunks_batched(x, obs, self.batch_size, self.shuffle)

    def __len__(self):
        return self.adata.X.shape[0]