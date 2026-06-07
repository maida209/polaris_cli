from .query_executor import *
from .query_executor_get_raster import GetRasterExecutor


class TimeseriesExecutor(QueryExecutor):
    def __init__(
        self,
        dr: DataRange,
        time_series_aggregation_method: str,  # e.g., "mean", "max", "min"
        log_info=None,
    ):
        dr.spatial_resolution = 0.25
        super().__init__(
            dr=dr,
        )
        self.time_series_aggregation_method = time_series_aggregation_method
        self.log_info = log_info if log_info is not None else []

    def execute(self):
        # print(f"[TimeseriesExecutor] Starting execution")
        temp_dr = self.dr.__copy__()
        temp_dr.aggregation = self.time_series_aggregation_method
        get_raster_executor = GetRasterExecutor(
            dr=temp_dr,
        )
        raster = get_raster_executor.execute()

        print(f"[DEBUG] self.log_info type: {type(self.log_info)}")
        print(f"[DEBUG] self.log_info content: {self.log_info}")
        self.log_info.append(get_raster_executor.get_log())

        if self.time_series_aggregation_method == "mean":
            return raster.mean(dim=["latitude", "longitude"]).compute()
        elif self.time_series_aggregation_method == "max":
            return raster.max(dim=["latitude", "longitude"]).compute()
        elif self.time_series_aggregation_method == "min":
            return raster.min(dim=["latitude", "longitude"]).compute()
        else:
            raise ValueError(f"Invalid time series aggregation method: {self.time_series_aggregation_method}")
