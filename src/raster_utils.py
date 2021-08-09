
import glob
import os
import numpy as np
from typing import List, Tuple, Union

import rasterio as rio


def crop_raster(input_img: str, dest_dir: str, x_range: List[int], y_range: List[int]):
    """Crop raster into subgrids
    Args:
        input_img (str): Path to raster file
        dest_dir (str): Destination directory
        x_range (List[int]): x range of cropping
        y_range (List[int]): y range of cropping
    """

    os.makedirs(dest_dir, exist_ok=True)

    with rio.open(input_img) as src:

        img = np.array([src.read(i + 1) for i in range(src.count)])

        (band, _, _) = img.shape

        (west, north) = src.xy(x_range[0], y_range[0])
        (east, south) = src.xy(x_range[1], y_range[1])
        x_pix = x_range[1] - x_range[0]
        y_pix = y_range[1] - y_range[0]

        affine = rio.transform.from_bounds(
            west, south, east, north, y_pix, x_pix
        )

        crop_img = img[:, x_range[0]:x_range[1], y_range[0]:y_range[1]]

        crop_img_name = (
            os.path.splitext(input_img)[0]
            + f"_{x_range[0]}_{y_range[0]}_{x_range[1]}_{y_range[1]}.tif"
        )

        save_path = os.path.join(dest_dir, os.path.split(crop_img_name)[-1])
        print(f"creating {save_path}")

        with rio.open(
            save_path,
            "w",
            driver="GTiff",
            dtype=crop_img.dtype,
            height=x_pix,
            width=y_pix,
            count=band,
            crs=src.crs,
            transform=affine,
        ) as dst:

            dst.write(crop_img)

def get_affine(input_img: str, x_range: List[int], y_range: List[int]) -> np.array:
    """Get affine transform matrix

    Args:
        input_img (str): Path to raster file
        x_range (List[int]): x range of cropping
        y_range (List[int]): y range of cropping

    Returns:
        np.array: Affine transform matrix
    """
    with rio.open(input_img) as src:

        (west, north) = src.xy(x_range[0], y_range[0])
        (east, south) = src.xy(x_range[1], y_range[1])
        x_pix = x_range[1] - x_range[0]
        y_pix = y_range[1] - y_range[0]

        affine = rio.transform.from_bounds(
            west, south, east, north, y_pix, x_pix
        )

    return affine