import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

gitdeps = [ "anki", "genanki" ]
for dep in gitdeps:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', "deps", dep))

import sdgenanki
