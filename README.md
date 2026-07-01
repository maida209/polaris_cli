# PolarIS CLI
polaris_api should be in this directory with in the django repo. 

<img width="307" height="226" alt="Screenshot 2026-06-30 at 8 46 20 PM" src="https://github.com/user-attachments/assets/54de3e30-09ad-4b38-a841-7da67fb9759d" />

*** Where the polaris_api folder is should be the polaris_cli. ***
## Running PolarIS

From the project root, run:

```bash
cd backend
bash init_venv.sh
source venv/bin/activate
cd polaris_api
pip install -e .
polar-is
```

You should see:

```text
Starting PolarIS
PolarIS $
```

---

## Creating a Data Object

Use the following format:

```text
data_object <name> <dataset> <variable> <start_time> <end_time> <temporal_resolution> <lat_range> <lon_range> <spatial_resolution> <aggregation>
```

Example:

```text
data_object aktemp ERA5 2m_temperature 2020-01-01T00:00 2020-12-31T23:00 day [55,60] [-160,-140] 0.25 mean
```

Expected output:

```text
Saved DataObject 'aktemp'
```

---

## Creating a Plot

Use the following format:

```text
plot <data_object_name> <plot_type>
```

Example:

```text
plot aktemp heatmap
```

Expected output:

```text
Plotting...
Plot complete.
```

---

## Example Session

```text
PolarIS $ data_object temp1 era5 2m_temperature 2020-01-01T00:00 2020-12-31T23:00 day [40,45] [-95,-90] 0.25 mean

Saved DataObject 'temp1'

PolarIS $ plot temp1 heatmap

Plotting...
Plot complete.
```

---

## Exiting PolarIS

```text
quit
```

Example:

```text
PolarIS $ quit
Exiting.
```

---

## Notes

- Ensure the virtual environment is activated before running `polar-is`.
- Verify that `METADATA_PATH` in `iharpconfig.toml` points to the correct metadata file.
