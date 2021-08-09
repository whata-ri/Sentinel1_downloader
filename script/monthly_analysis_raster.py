import rasterio as rio
import glob
import numpy as np
import os
import sys
import pandas as pd
from datetime import datetime

sys.path.append(os.path.join(os.path.abspath(''), "../"))
from src import get_affine, get_metadata, vectorize_raster


target_date = [
    datetime.strptime("20200101", "%Y%m%d"),
    datetime.strptime("20201231", "%Y%m%d")
]

data_root = os.path.join("..", "data", "Karachi")
flist = glob.glob(os.path.join(data_root, "*"))

x = [1000, 2000]
y = [2000, 3500]

sigma = 1.5
thresh_sigma = 5
output_root = os.path.join("..", "output", "raster")
os.makedirs(output_root, exist_ok=True)

filtered_flist = []
for fname in flist:
    dt = get_metadata(fname)["date"]
    if dt > target_date[0] and dt < target_date[1]:
        filtered_flist.append(fname)

month_list = [get_metadata(fname)["date"].month for fname in filtered_flist]
datetime_list = [get_metadata(fname)["date"] for fname in filtered_flist]

master_df = pd.DataFrame({
    "fname": filtered_flist,
    "month": month_list,
    "datetime": datetime_list
})

m = master_df["month"].unique()
m.sort()

VV_imgs = []

for i in m:
    img_mean = np.zeros((x[1] - x[0], y[1] - y[0]))
    m_i_list = list(master_df[master_df["month"] == i]["fname"])
    for img in m_i_list:
        with rio.open(img) as src:
            VV = src.read(1)
        img_mean += VV[x[0]:x[1], y[0]:y[1]]
        print(f"Read: {img}")
    img_mean = img_mean/len(m_i_list)
    VV_imgs.append(img_mean)

transform = get_affine(m_i_list[0], x, y)

for i in range(len(VV_imgs)):
    if i != 0:
        diff = VV_imgs[i] - VV_imgs[i-1]
        mean = diff.mean()
        std = diff.std()
        normalized = (diff - mean)/std

        removed = np.where(diff < mean - sigma*std, -1*normalized, 0)
        constructed = np.where(diff > mean + sigma*std, normalized, 0)

        removed = np.clip(removed * 255/thresh_sigma, 0, 255).astype(np.uint8)
        constructed = np.clip(constructed * 255/thresh_sigma, 0, 255).astype(np.uint8)

        img = np.array([removed, constructed, constructed])

        fname = os.path.join(
            output_root,
            f"month{i}-month{i+1}.tif"
        )

        with rio.open(
            fname,
            "w",
            driver="GTiff",
            dtype=np.uint8,
            height=x[1] - x[0],
            width=y[1] - y[0],
            count=3,
            crs=src.crs,
            transform=transform,
        ) as dst:

            dst.write(img)
        print(f"Finish: {fname}")
