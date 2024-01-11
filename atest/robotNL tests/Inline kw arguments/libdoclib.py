import json
import os
import tempfile

from robot.libdoc import libdoc

class libdoclib:
    def __init__(self):
        self.output = {}

    def run_libdoc(self):
        self.output = {}
        libfile = os.path.join(os.path.dirname(__file__), 'inline_kw_args.py')
        with tempfile.TemporaryDirectory() as tmpdirname:
            outfile = os.path.join(tmpdirname, "libdoc_gen.json")
            libdoc(libfile, outfile)
            self.output = json.load(open(outfile))

    def libdoc_registered_types(self):
        return [td['name'] for td in self.output['typedocs']]
