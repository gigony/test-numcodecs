# test-numcodecs

Temporary repository for reproducing numcodecs issue (https://github.com/zarr-developers/numcodecs/pull/234).

## Getting Started

```bash
./run_numcodecs_leak.sh leak  # execute reproducer without patch
./run_numcodecs_leak.sh patch # execute reproducer with patch (0001-Create-free-mutex-in-init-destroy.patch)
```
