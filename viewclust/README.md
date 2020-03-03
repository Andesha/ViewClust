# ViewClust
This package functions as a tool for interpreting scheduler information and displaying it graphically.

## Installation
These instructions apply to testing functionality on the Graham system.

1. Log into Graham and enter a workspace of your choice.

2. Create a working directory and clone the ViewCLust package:

```bash
mkdir viewclust-tutorial
cd viewclust-tutorial
git clone https://git.computecanada.ca/cc-analytics/viewclust.git
```

3. Create and activate the virtual environment then install the package dependencies:

```bash
python3 -m venv viewclust-tutorial-env
source viewclust-tutorial-env/bin/activate
pip install -r viewclust/requirements.txt
pip install -r ccmnt/requirements.txt
```

Your project should now have ViewClust nested inside of it with the necessary dependencies installed.

If there appears to be a version error and pip was unable to install the necessary packages by default, run pip install `PACKAGE_NAME` where `PACKAGE_NAME` is each item in the following list:
* `numpy`
* `pandas`
* `plotly`

ViewClust can then be imported as usual per `import viewclust as vc` and then called via `vc.job_use()`

## Documentation
Functions in this package contain standard Python docstrings. See individual functions for specific information.

The test directory in this repository contains example scripts of typical usage.

If this repository is being used as part of a tutorial you may be asked to copy scripts from this location.
