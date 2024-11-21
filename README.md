# IECDT AI for Earth Observation Computing Lab

## Environment and Kernel Installation on JASMIN
To install the `iecdt-earth-observation` environment and create a Jupyter kernel to use on JASMIN's JupyterHub, run the following command on JASMIN:

```bash
chmod u+x setup.sh
./setup.sh
```

## Environment Installation only

Run the following commands to create the `iecdt-earth-observation` environment:

```bash
conda env create -f environment.yml

conda activate iecdt-earth-observation
```
