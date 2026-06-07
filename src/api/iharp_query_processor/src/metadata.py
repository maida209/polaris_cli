import numpy as np
import pandas as pd
import xarray as xr

from .utils.const import DataRange, get_lat_lon_range, time_resolution_to_freq

_f_path = ""
_df_meta: pd.DataFrame

def init_metadata(f_path):
    global _f_path, _df_meta
    _f_path = f_path
    _df_meta = pd.read_csv(f_path)

def add_metadata(dr: DataRange):
    pass

def remove_metadata(dr: DataRange):
    pass


def _gen_empty_xarray(
    min_lat,
    max_lat,
    min_lon,
    max_lon,
    start_datetime,
    end_datetime,
    temporal_resolution,
    spatial_resolution,
):
    lat_range, lon_range, lat_range_reverse = get_lat_lon_range(spatial_resolution)
    lat_start = lat_range.searchsorted(min_lat, side="left")
    lat_end = lat_range.searchsorted(max_lat, side="right")
    lat_reverse_start = len(lat_range) - lat_end
    lat_reverse_end = len(lat_range) - lat_start
    lon_start = lon_range.searchsorted(min_lon, side="left")
    lon_end = lon_range.searchsorted(max_lon, side="right")
    ds_empty = xr.Dataset()
    ds_empty["time"] = pd.date_range(
        start=start_datetime,
        end=end_datetime,
        freq=time_resolution_to_freq(temporal_resolution),
    )
    ds_empty["latitude"] = lat_range_reverse[lat_reverse_start:lat_reverse_end]
    ds_empty["longitude"] = lon_range[lon_start:lon_end]
    return ds_empty

def _gen_xarray_for_meta_row(row, overwrite_temporal_resolution=None):
    if overwrite_temporal_resolution is not None:
        t_resolution = overwrite_temporal_resolution
    else:
        t_resolution = row.temporal_resolution
    return _gen_empty_xarray(
        row.min_lat,
        row.max_lat,
        row.min_lon,
        row.max_lon,
        row.start_datetime,
        row.end_datetime,
        t_resolution,
        row.spatial_resolution,
    )

def _mask_query_with_meta(ds_query, ds_meta):
    return (
        ds_query["time"].isin(ds_meta["time"])
        & ds_query["latitude"].isin(ds_meta["latitude"])
        & ds_query["longitude"].isin(ds_meta["longitude"])
    )

def query_get_overlap_and_leftover(dr: DataRange):
    df_overlap = _df_meta[
        (_df_meta["variable"] == dr.variable)
        & (_df_meta["min_lat"] <= dr.max_lat)
        & (_df_meta["max_lat"] >= dr.min_lat)
        & (_df_meta["min_lon"] <= dr.max_lon)
        & (_df_meta["max_lon"] >= dr.min_lon)
        & (pd.to_datetime(_df_meta["start_datetime"]) <= pd.to_datetime(dr.end_datetime))
        & (pd.to_datetime(_df_meta["end_datetime"]) >= pd.to_datetime(dr.start_datetime))
        & (_df_meta["temporal_resolution"] == dr.temporal_resolution)
        & (_df_meta["spatial_resolution"] == dr.spatial_resolution)
        & (_df_meta["aggregation"] == dr.aggregation)
    ]

    ds_query = _gen_empty_xarray(
        dr.min_lat,
        dr.max_lat,
        dr.min_lon,
        dr.max_lon,
        dr.start_datetime,
        dr.end_datetime,
        dr.temporal_resolution,
        dr.spatial_resolution,
    )

    false_mask = xr.DataArray(
        data=np.zeros(
            (
                ds_query.sizes["time"],
                ds_query.sizes["latitude"],
                ds_query.sizes["longitude"],
            ),
            dtype=bool,
        ),
        coords={
            "time": ds_query["time"],
            "latitude": ds_query["latitude"],
            "longitude": ds_query["longitude"],
        },
        dims=["time", "latitude", "longitude"],
    )

    for row in df_overlap.itertuples():
        ds_meta = _gen_xarray_for_meta_row(row)
        mask = _mask_query_with_meta(ds_query, ds_meta)
        false_mask = false_mask | mask

    leftover = false_mask.where(false_mask == False, drop=True)
    if leftover.values.size > 0:
        return df_overlap, leftover
    else:
        return df_overlap, None
