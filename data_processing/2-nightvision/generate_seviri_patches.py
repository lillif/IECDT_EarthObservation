#!/home/users/wkjones/miniforge3/envs/tobac_flow/bin/python
import pathlib
import warnings
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import pyproj
pyproj.datadir.set_data_dir("/home/users/wkjones/miniforge3/envs/tobac_flow/share/proj")

from satpy import Scene
from satpy.writers import to_image
from pyresample.geometry import AreaDefinition
from pyproj.crs import CRS

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("date", help="Start date for processing", type=str)
args = parser.parse_args()


start_date = datetime.strptime(args.date, "%Y-%m-%d")
end_date = start_date + timedelta(days=1)

seviri_path = pathlib.Path("/gws/nopw/j04/eo_shared_data_vol1/satellite/seviri/Data")

files = []

for date in pd.date_range(start_date, end_date, freq="h", inclusive="left").to_pydatetime():
    seviri_files = sorted(list((seviri_path / date.strftime("%Y/%m/%d")).glob(
        f'MSG[1234]-SEVI-MSG15-0100-NA-{date.strftime("%Y%m%d%H")}*-NA.nat'
    )))
    if len(seviri_files):
        files.append(seviri_files[0])

def get_random_lonlat(resolution=0.05, offset=3.2, number=1):
    lons = np.arange(-30+offset, 30-offset, resolution)
    lats = np.arange(30+offset, 60-offset, resolution)
    return np.random.choice(lons, number), np.random.choice(lats, number)
    
def create_nightvision_patches(filename, save_path, number_of_patches=1, patch_size=128, resolution=0.05):
    filename = str(filename)
    save_path = pathlib.Path(save_path)
    
    scene = Scene([filename], reader="seviri_l1b_native")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        scene.load(["cloudtop", "natural_color"], unload=True) 

    europe_grid = AreaDefinition(
        "Europe_grid", 
        "Europe equal latitude/longitude grid", 
        "longlat",
        projection="4326",
        width=int(60/resolution), height=int(30/resolution), area_extent=(-30,30,30,60)
    )
    
    grid_scene = scene.resample(europe_grid, resampler="bilinear")

    offset = patch_size/2 * resolution
    lon_slice_offset = resolution*0.25
    lat_slice_offset = resolution*0.75

    lons, lats = get_random_lonlat(resolution=resolution, offset=offset, number=number_of_patches)
    for lon, lat in zip(lons, lats):
        crop_scene = grid_scene.crop(xy_bbox=[
            lon-offset+lon_slice_offset, 
            lat-offset+lat_slice_offset, 
            lon+offset-lon_slice_offset, 
            lat+offset-lat_slice_offset
        ])
        assert crop_scene.to_xarray().natural_color.shape == (3, patch_size, patch_size), f'Patch size: {crop_scene.to_xarray().natural_color.shape}'

        save_id = f'{filename.split("/")[-1].split("-")[-2][:10]}0000_{lon:05.2f}_{lat:05.2f}.png'

        img = to_image(crop_scene["cloudtop"])
        img.stretch(min_stretch=[245, 220, 225], max_stretch=[310, 300, 295])
        img.invert(True)
        img.save(
            save_path / f'cloudtop_{save_id}'
        )
    
        crop_scene.show("natural_color").save(
            save_path / f'natural_color_{save_id}'
        )

for file in files:
    create_nightvision_patches(
        file, "/work/scratch-nopw2/iecdt_ai4eo/preprocessing/nightvision_patches", number_of_patches=1, patch_size=128, resolution=0.1
    )