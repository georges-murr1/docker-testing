import os
# Set the environment variable to ignore DeprecationWarnings as early as possible
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

# Import dateutil.tz and clear its warning registry (if it exists)
import dateutil.tz
if hasattr(dateutil.tz, "__warningregistry__"):
    dateutil.tz.__warningregistry__.clear()

import sys
import matplotlib
# Use a non-interactive backend early
matplotlib.use("Agg")

# Add the src directory to the Python module search path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
