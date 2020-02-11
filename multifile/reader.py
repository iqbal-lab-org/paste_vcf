import itertools


class MultiVCFReader:
    def __init__(self, input_paths):
        self._input_paths = input_paths
        self.headers = set()

    def __enter__(self):
        self._files = map(lambda p: open(p, 'r'), self._input_paths)
        self._file_cycle = itertools.cycle(self._files)
        return self

    def __exit__(self, *args, **kwargs):
        [f.close() for f in self._files]

    def __next__(self):
        if not getattr(self, '_files', None):
            raise BadUsageError

        line = next(self._file_cycle).readline()
        if not line:
            raise StopIteration

        line = line.rstrip()

        if line.startswith('##'):
            self.headers.add(line)

        return line

    def __iter__(self):
        return self


class BadUsageError(Exception):
    def __str__(self):
        return "MultiVCFReader should be used inside a context manager"
