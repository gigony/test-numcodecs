from pathlib import Path
import dask.array as da


class ZarrReader:
    def __init__(self, input_folder, pattern="*.zarr"):
        try:
            self.input_path = next(Path(input_folder).glob(pattern))
        except StopIteration:
            raise RuntimeError(
                "'{}' folder doesn't have {} file".format(input_folder, pattern)
            )
        # self._lock = threading.Lock()

    def _tile_generator(self):
        if str(self.input_path).endswith('zarr'):
            level_array = da.from_zarr(
                str(self.input_path)
            )
        else:
            level_array = da.from_npy_stack(
                str(self.input_path)
            )
        block_array = level_array.blocks[0,0].compute()
        yield block_array

    def generator(self):
        gen = self._tile_generator()
        while True:
            # with self._lock:
                yield next(gen)


def load_zarr(pattern="fail.zarr"):
    for block_array in ZarrReader(
        '.',
        pattern=pattern,
    ).generator():
        b = block_array
        print("Done:", b.shape)



if __name__ == '__main__':
    if len(list(Path('.').glob('fail.zarr'))) == 0:
        from numcodecs import Blosc
        compressor = Blosc()
        x = da.random.random((100, 100, 3), chunks=(100, 100,3))
        x.to_zarr('fail.zarr', compressor=compressor, overwrite=True)
    if len(list(Path('.').glob('fail.npystack'))) == 0:
        x = da.random.random((100, 100, 3), chunks=(100, 100,3))
        da.to_npy_stack('fail.npystack', x)


    from dask.distributed import LocalCluster, Client
    # cluster = LocalCluster(host='0.0.0.0', n_workers=1, threads_per_worker=1)
    # client = Client(cluster)              # 'fail'
    client = Client(threads_per_worker=1)   # 'fail'
    # client = Client(processes=False, threads_per_worker=1)   # 'not fail'

    load_zarr() # 'fail' with zarr

    #load_zarr('fail.npystack') # 'not fail' with npystack



