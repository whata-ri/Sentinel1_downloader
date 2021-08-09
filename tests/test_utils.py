from datetime import datetime
import os
import sys

sys.path.append(os.path.join(os.path.abspath(''), "../"))
from src import get_metadata

def test_metadata_parser():
    fname = "S1A_IW_GRDH_1SDV_20180108T133512_20180108T133537_020064_022310_6C20.tif"

    metadata = get_metadata(fname)

    assert metadata["satellite"] == "S1A"
    assert metadata["mode"] == "IW"
    assert metadata["process"] == "GRDH"
    assert metadata["date"] == datetime(2018, 1, 8, 13, 35, 12)
