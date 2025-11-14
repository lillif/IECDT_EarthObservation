mamba env create -f environment.yml -p ~/iecdt_earth_observation_env
conda run -p ~/iecdt_earth_observation_env python -m ipykernel install --user --name=iecdt-earth-observation
