#!/usr/bin/env python

from cpt.packager import ConanMultiPackager
import copy

if __name__ == "__main__":
    builder = ConanMultiPackager()
    builder.add_common_builds()
    builder.run()
