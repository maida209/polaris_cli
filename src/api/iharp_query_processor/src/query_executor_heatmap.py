import numpy as np
import xarray as xr

from .query_executor import QueryExecutor
from .query_executor_get_raster import GetRasterExecutor
from .utils.const import DataRange
from .utils.get_whole_period import (
    get_whole_ranges_between,
    get_total_hours_in_year,
    get_total_hours_in_month,
    iterate_months,
    number_of_days_inclusive,
    number_of_hours_inclusive,
    get_total_hours_between,
)


class HeatmapExecutor(QueryExecutor):
    def __init__(
        self,
        dr: DataRange,
        heatmap_aggregation_method: str,  # e.g., "mean", "max", "min"
        log_info=None,
        range_info=None,
    ):
        dr.temporal_resolution = "hour"
        super().__init__(
            dr=dr,
        )
        self.heatmap_aggregation_method = heatmap_aggregation_method
        self.log_info = log_info if log_info is not None else []
        self.range_info = range_info if range_info is not None else []

    def get_log(self):
        return self.log_info

    def get_range(self):
        return self.range_info
        both_dict = {"log": self.log_info,
                     "ranges": self.range_info}
        return both_dict

    def execute(self):
        if self.heatmap_aggregation_method == "mean":
            return self._get_mean_heatmap().compute()
        elif self.heatmap_aggregation_method == "max":
            return self._get_max_heatmap().compute()
        elif self.heatmap_aggregation_method == "min":
            return self._get_min_heatmap().compute()
        else:
            raise ValueError("Invalid heatmap_aggregation_method")

    def _get_mean_heatmap(self):
        num_yrs = 0
        num_mos = 0
        num_days = 0
        num_hrs = 0
        year_range, month_range, day_range, hour_range = get_whole_ranges_between(
            self.dr.start_datetime, self.dr.end_datetime
        )
        ds_year = []
        ds_month = []
        ds_day = []
        ds_hour = []
        year_hours = []
        month_hours = []
        day_hours = []
        hour_hours = []
        for start_year, end_year in year_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_year)
            temp_dr.end_datetime = str(end_year)
            temp_dr.temporal_resolution = "year"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_year = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_year.append(get_raster_year.execute())
            self.log_info.append(get_raster_year.get_log())
            yr_range = range(start_year.year, end_year.year + 1)
            num_yrs=(len(yr_range))
            print(f"num years: {num_yrs}\tstart: {start_year.year}, \tend: {end_year.year}")
            year_hours += [get_total_hours_in_year(y) for y in yr_range]

        for start_month, end_month in month_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_month)
            temp_dr.end_datetime = str(end_month)
            temp_dr.temporal_resolution = "month"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_month = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_month.append(get_raster_month.execute())
            self.log_info.append(get_raster_month.get_log())
            mo_range = iterate_months(start_month, end_month)
            num_mos=(len(list(mo_range)))
            print(f"num months: {num_mos}\tstart: {start_month}, \tend: {end_month}")
            month_hours += [get_total_hours_in_month(m) for m in iterate_months(start_month, end_month)]

        for start_day, end_day in day_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_day)
            temp_dr.end_datetime = str(end_day)
            temp_dr.temporal_resolution = "day"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_day = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_day.append(get_raster_day.execute())
            self.log_info.append(get_raster_day.get_log())
            da_range = range(number_of_days_inclusive(start_day, end_day))
            num_days=(len(da_range))
            print(f"num days: {num_yrs}\tstart: {start_day}, \tend: {end_day}")
            day_hours += [24 for _ in da_range]

        for start_hour, end_hour in hour_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_hour)
            temp_dr.end_datetime = str(end_hour)
            temp_dr.temporal_resolution = "hour"
            get_raster_hour = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_hour.append(get_raster_hour.execute())
            self.log_info.append(get_raster_hour.get_log())
            hr_range = range(number_of_hours_inclusive(start_hour, end_hour))
            num_hrs=(len(hr_range))
            print(f"num hours: {num_hrs}\tstart: {start_hour}, \tend: {end_hour}")
            hour_hours += [1 for _ in hr_range]

        xrds_concat = xr.concat(ds_year + ds_month + ds_day + ds_hour, dim="valid_time", join="outer")
        nd_array = xrds_concat[self.variable_short_name].to_numpy()
        weights = np.array(year_hours + month_hours + day_hours + hour_hours)
        total_hours = get_total_hours_between(self.dr.start_datetime, self.dr.end_datetime)
        weights = weights / total_hours
        average = np.average(nd_array, axis=0, weights=weights)
        res = xr.Dataset(
            {self.variable_short_name: (["latitude", "longitude"], average)},
            coords={"latitude": xrds_concat.latitude, "longitude": xrds_concat.longitude},
        )
        self.range_info.append({"year": num_yrs, "month": num_mos, "day": num_days, "hour": num_hrs})
        return res

    def _get_max_heatmap(self):
        num_yrs = 0
        num_mos = 0
        num_days = 0
        num_hrs = 0
        year_range, month_range, day_range, hour_range = get_whole_ranges_between(
            self.dr.start_datetime, self.dr.end_datetime
        )
        ds_year = []
        ds_month = []
        ds_day = []
        ds_hour = []
        for start_year, end_year in year_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_year)
            temp_dr.end_datetime = str(end_year)
            temp_dr.temporal_resolution = "year"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_year = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_year.append(get_raster_year.execute())
            self.log_info.append(get_raster_year.get_log())
            yr_range = range(start_year.year, end_year.year + 1)
            num_yrs=(len(yr_range))
            print(f"num years: {num_yrs}\tstart: {start_year.year}, \tend: {end_year.year}")

        for start_month, end_month in month_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_month)
            temp_dr.end_datetime = str(end_month)
            temp_dr.temporal_resolution = "month"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_month = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_month.append(get_raster_month.execute())
            self.log_info.append(get_raster_month.get_log())
            mo_range = iterate_months(start_month, end_month)
            num_mos=(len(list(mo_range)))
            print(f"\n\n*********\n\nNUM months: {num_mos}\tstart: {start_month}, \tend: {end_month}")

        for start_day, end_day in day_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_day)
            temp_dr.end_datetime = str(end_day)
            temp_dr.temporal_resolution = "day"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_day = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_day.append(get_raster_day.execute())
            self.log_info.append(get_raster_day.get_log())
            da_range = range(number_of_days_inclusive(start_day, end_day))
            num_days=(len(da_range))
            print(f"num days: {num_yrs}\tstart: {start_day}, \tend: {end_day}")

        for start_hour, end_hour in hour_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_hour)
            temp_dr.end_datetime = str(end_hour)
            temp_dr.temporal_resolution = "hour"
            get_raster_hour = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_hour.append(get_raster_hour.execute())
            self.log_info.append(get_raster_hour.get_log())
            hr_range = range(number_of_hours_inclusive(start_hour, end_hour))
            num_hrs=(len(hr_range))
            print(f"num hours: {num_hrs}\tstart: {start_hour}, \tend: {end_hour}")
            self.range_info.append({"year": num_yrs, "month": num_mos, "day": num_days, "hour": num_hrs})
        return xr.concat(ds_year + ds_month + ds_day + ds_hour, dim="valid_time", join="outer").max(dim="valid_time")

    def _get_min_heatmap(self):
        num_yrs = 0
        num_mos = 0
        num_days = 0
        num_hrs = 0
        year_range, month_range, day_range, hour_range = get_whole_ranges_between(
            self.dr.start_datetime, self.dr.end_datetime
        )
        ds_year = []
        ds_month = []
        ds_day = []
        ds_hour = []
        for start_year, end_year in year_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_year)
            temp_dr.end_datetime = str(end_year)
            temp_dr.temporal_resolution = "year"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_year = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_year.append(get_raster_year.execute())
            self.log_info.append(get_raster_year.get_log())
            yr_range = range(start_year.year, end_year.year + 1)
            num_yrs=(len(yr_range))
            print(f"num years: {num_yrs}\tstart: {start_year.year}, \tend: {end_year.year}")

        for start_month, end_month in month_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_month)
            temp_dr.end_datetime = str(end_month)
            temp_dr.temporal_resolution = "month"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_month = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_month.append(get_raster_month.execute())
            self.log_info.append(get_raster_month.get_log())
            mo_range = iterate_months(start_month, end_month)
            num_mos=(len(list(mo_range)))
            print(f"num months: {num_mos}\tstart: {start_month}, \tend: {end_month}")

        for start_day, end_day in day_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_day)
            temp_dr.end_datetime = str(end_day)
            temp_dr.temporal_resolution = "day"
            temp_dr.aggregation = self.heatmap_aggregation_method
            get_raster_day = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_day.append(get_raster_day.execute())
            self.log_info.append(get_raster_day.get_log())
            da_range = range(number_of_days_inclusive(start_day, end_day))
            num_days=(len(da_range))
            print(f"num days: {num_yrs}\tstart: {start_day}, \tend: {end_day}")

        for start_hour, end_hour in hour_range:
            temp_dr = self.dr.__copy__()
            temp_dr.start_datetime = str(start_hour)
            temp_dr.end_datetime = str(end_hour)
            temp_dr.temporal_resolution = "hour"
            get_raster_hour = GetRasterExecutor(
                dr=temp_dr,
            )

            ds_hour.append(get_raster_hour.execute())
            self.log_info.append(get_raster_hour.get_log())
            hr_range = range(number_of_hours_inclusive(start_hour, end_hour))
            num_hrs=(len(hr_range))
            print(f"num hours: {num_hrs}\tstart: {start_hour}, \tend: {end_hour}")
            self.range_info.append({"year": num_yrs, "month": num_mos, "day": num_days, "hour": num_hrs})
            
        # get min heatmap from ds_year, ds_month, ds_day, ds_hour
        return xr.concat(ds_year + ds_month + ds_day + ds_hour, dim="valid_time", join="outer").min(dim="valid_time")
