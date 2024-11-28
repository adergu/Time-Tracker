# tests/__init.py

import sys
from os.path import abspath, dirname

# Add the src directory to the system path for tests
sys.path.insert(0, abspath(dirname(dirname(__file__))) + "/src")
