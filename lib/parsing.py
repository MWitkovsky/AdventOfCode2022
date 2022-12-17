import json


class InputParser:
    def _check_file_closed(method):
        def inner(self, *args, **kwargs):
            if self.file.closed:
                raise IOError("File has already been closed")
            return method(self, *args, **kwargs)
        return inner

    def __init__(self, fname):
        try:
            self.file = open(fname, "r")
        except IOError:
            raise

    def __del__(self):
        if not self.file.closed:
            self.file.close()

    @_check_file_closed
    def to_array(self, elem_type=str, suppress_warnings=False):
        """
        Will try to convert every line of input to specified type, but will
        skip any elements that fail to parse
        """
        content = self.file.read().splitlines()
        if elem_type != str:
            elem_func = elem_type
            if elem_type == "json":
                def elem_func(x): return json.loads(x) if len(x) > 0 else ""

            for i, elem in enumerate(content):
                try:
                    content[i] = elem_func(elem)
                except:
                    if not suppress_warnings:
                        print(f"[WARNING]: element at line {i} failed to "
                              f"parse ({elem})")

        return content

    @_check_file_closed
    def close(self):
        self.file.close()
