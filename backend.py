import pandas as pd
import numpy as np
import nbconvert

import json


if __name__ == "__main__":
    fname = "./sample.ipynb"

    with open(fname) as fp:
        nb = json.load(fname)
