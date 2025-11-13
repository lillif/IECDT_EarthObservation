# IECDT AI for Earth Observation Computing Lab

## Overview

This course provides an introduction to machine learning with earth observation data. The course contains three exercises (found in the `challenges' directory) to work through, each of which explores a different type of ML challenge using different EO data:

  1. Sunny Oxford: forecast daily hours of sunlight using satellite observations and weather station data
  2. Night Vision: train an image-to-image prediction model to reconstruct visible satellite images from infra-red observations at night
  3. Sentinel Maps: create a regression model to predict vegetation fraction from satellite images

For the 2025 course, you should pick either the Sunny Oxford or Night Vision challenges to work through during the lab, but you are free to work through any of the challenges in your own time.

## Setup instructions

### Clone the repository into your JASMIN home directory
```bash
git clone https://github.com/lillif/IECDT_EarthObservation.git
```

### Environment and kernel installation on JASMIN
To install the `iecdt-earth-observation` environment and create a Jupyter kernel to use on JASMIN's JupyterHub, run the following command on JASMIN:

```bash
chmod u+x setup.sh
./setup.sh
```

### Environment installation only

Run the following commands to create the `iecdt-earth-observation` environment:

```bash
conda env create -f environment.yml

conda activate iecdt-earth-observation
```
