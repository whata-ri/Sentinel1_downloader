import glob
from datetime import datetime
from typing import Dict


def get_metadata(fname) -> Dict:
    """Get metadata by filename of Sentinel-1 data

    Args:
        fname (str): Sentinel-1 file name
            eg) S1A_IW_GRDH_1SDV_20180108T133512_20180108T133537_020064_022310_6C20.tif

    Returns:
        Dict: metadata
    """

    block = fname.split("_")
    metadata = {
        "satellite": block[0],
        "mode": block[1],
        "process": block[2],
        "date": datetime.strptime(block[4], "%Y%m%dT%H%M%S")
    }

    return metadata

if __name__ == "__main__":
    metadata = get_metadata("S1A_IW_GRDH_1SDV_20180108T133512_20180108T133537_020064_022310_6C20")
    print(metadata)