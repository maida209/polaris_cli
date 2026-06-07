from api.iharp_query_processor import *

from api.iharp_query_processor.src.utils.const import DataRange
metadata_fpath = "/Users/Maida/django-react-starter/backend/metadata.csv"

def find_area(data, **kwargs):
    eq = FindAreaExecutor(
        variable = data.name,
        start_datetime = data.start_t,
        end_datetime = data.end_t,
        min_lat =  data.latitude_range[0],
        max_lat =  data.latitude_range[1],
        min_lon =  data.longitude_range[0],
        max_lon =  data.longitude_range[1],
        temporal_resolution =  data.t_res,  # e.g., "hour", "day", "month", "year"
        spatial_resolution =  data.space_res, # e.g., 0.25, 0.5, 1.0
        aggregation = data.aggregation,
        heatmap_aggregation_method =  data.aggregation,
        filter_predicate = kwargs["filter"],
        filter_value = kwargs["value"]
    )
    return eq.execute()


    
def find_time (data, **kwargs):
    eq = FindTimeExecutor(
        variable = data.name,
        start_datetime = data.start_t,
        end_datetime = data.end_t,
        min_lat =  data.latitude_range[0],
        max_lat =  data.latitude_range[1],
        min_lon =  data.longitude_range[0],
        max_lon =  data.longitude_range[1],
        temporal_resolution =  data.t_res,  # e.g., "hour", "day", "month", "year"
        spatial_resolution =  data.space_res, # e.g., 0.25, 0.5, 1.0
        aggregation = data.aggregation,
        heatmap_aggregation_method =  data.aggregation,
        filter_predicate = kwargs["filter"],
        filter_value = kwargs["value"]
    )
     
    return eq.execute()
def heatmap(data, **kwargs):
    # eq = HeatmapExecutor(
    #     metadata = metadata_fpath,
    #     variable = data.name,
    #     start_datetime = data.start_t,
    #     end_datetime = data.end_t,
    #     min_lat =  data.latitude_range[0],
    #     max_lat =  data.latitude_range[1],
    #     min_lon =  data.longitude_range[0],
    #     max_lon =  data.longitude_range[1],
    #     temporal_resolution =  data.t_res,  # e.g., "hour", "day", "month", "year"
    #     spatial_resolution =  data.space_res, # e.g., 0.25, 0.5, 1.0
    #     aggregation = data.aggregation,
    #     heatmap_aggregation_method =  data.aggregation,
    #     log_info = None,
    #     range_info = None
    # )
     
    # return eq.execute()
    dr = DataRange(
        variable=data.variable,
        start_datetime=str(data.start_t),
        end_datetime=str(data.end_t),
        min_lat=float(data.latitude_range[0]),
        max_lat=float(data.latitude_range[1]),
        min_lon=float(data.longitude_range[0]),
        max_lon=float(data.longitude_range[1]),
        temporal_resolution=str(data.t_res),  
        spatial_resolution=float(data.space_res),
        aggregation=data.aggregation
    )

    eq = HeatmapExecutor(
        dr=dr,
        heatmap_aggregation_method=data.aggregation,
        log_info=None,
        range_info=None
    )
     
    return eq.execute()
def timeseries(data, **kwargs):
    eq = TimeseriesExecutor(
        variable = data.variable,
        start_datetime = data.start_t,
        end_datetime = data.end_t,
        min_lat =  data.latitude_range[0],
        max_lat =  data.latitude_range[1],
        min_lon =  data.longitude_range[0],
        max_lon =  data.longitude_range[1],
        temporal_resolution =  data.t_res,  # e.g., "hour", "day", "month", "year"
        spatial_resolution =  data.space_res, # e.g., 0.25, 0.5, 1.0
        aggregation = data.aggregation,
        time_series_aggregation_method =  data.aggregation,
        log_info = None,
    )
     
    return eq.execute()

def run_plot(data, type, **kwargs):
    if type == "find_area":
        return find_area(data, **kwargs)
    elif type == "find_time":
        return find_time(data, **kwargs)
    elif type == "heatmap":
        return heatmap(data, **kwargs)
    elif type == "timeseries":
        return timeseries(data, **kwargs)
    else:
        raise ValueError("Wrong Type.")
