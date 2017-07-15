from context import sdgenanki
import sys
import os
def test_import():
    gitdeps = [ "anki", "genanki" ]
    for dep in gitdeps:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', "deps", dep))
    print(sys.path)
    import anki
    import genanki
