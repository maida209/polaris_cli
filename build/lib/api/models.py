from django.db import models


TEMPORAL_CHOICES = [
    ("hour", "hour"),
    ("day", "day"),
    ("month", "month"),
    ("year", "year"),
]

AGG_CHOICES = [
    ("min", "min"),
    ("max", "max"),
    ("mean", "mean"),
]

REQUEST_CHOICES = [
    ("get_raster", "get_raster"),
    ("timeseries", "timeseries"),
    ("heatmap", "heatmap"),
    ("find_time", "find_time"),
    ("find_area", "find_area"),
]

VARIABLE_CHOICES = [
    ("2m_temperature", "2m_temperature"),
    ("snow_depth", "snow_depth"),
    ("snowfall", "snowfall"),
    ("snowmelt", "snowmelt"),
    ("surface_pressure", "surface_pressure"),
    ("sea_surface_temperature", "sea_surface_temperature"),
    ("total_precipitation", "total_precipitation"),
    ("temperature_of_snow_layer", "temperature_of_snow_layer"),
    ("ice_temperature_layer_1", "ice_temperature_layer_1"),
    ("ice_temperature_layer_2", "ice_temperature_layer_2"),
    ("ice_temperature_layer_3", "ice_temperature_layer_3"),
    ("ice_temperature_layer_4", "ice_temperature_layer_4"),
]

FILTER_PREDICATE_CHOICES = [
    (">", ">"),
    ("<", "<"),
    (">=", ">="),
    ("<=", "<="),
    ("=", "="),
    ("!=", "!="),
]


class GetRasterQueryModel(models.Model):
    requestType = models.CharField(max_length=15, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    temporalResolution = models.CharField(max_length=10, choices=TEMPORAL_CHOICES)
    north = models.DecimalField(max_digits=25, decimal_places=20)
    east = models.DecimalField(max_digits=25, decimal_places=20)
    south = models.DecimalField(max_digits=25, decimal_places=20)
    west = models.DecimalField(max_digits=25, decimal_places=20)
    spatialResolution = models.DecimalField(max_digits=3, decimal_places=2)
    aggregation = models.CharField(max_length=10, choices=AGG_CHOICES)
    log_info = models.JSONField(default=list, blank=True)


class HeatmapQueryModel(models.Model):
    requestType = models.CharField(max_length=15, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    north = models.DecimalField(max_digits=25, decimal_places=20)
    east = models.DecimalField(max_digits=25, decimal_places=20)
    south = models.DecimalField(max_digits=25, decimal_places=20)
    west = models.DecimalField(max_digits=25, decimal_places=20)
    spatialResolution = models.DecimalField(max_digits=3, decimal_places=2)
    aggregation = models.CharField(max_length=10, choices=AGG_CHOICES)
    log_info = models.JSONField(default=list, blank=True)
    range_info = models.JSONField(default=list, blank=True)


class TimeseriesQueryModel(models.Model):
    requestType = models.CharField(max_length=15, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    temporalResolution = models.CharField(max_length=10, choices=TEMPORAL_CHOICES)
    north = models.DecimalField(max_digits=25, decimal_places=20)
    east = models.DecimalField(max_digits=25, decimal_places=20)
    south = models.DecimalField(max_digits=25, decimal_places=20)
    west = models.DecimalField(max_digits=25, decimal_places=20)
    aggregation = models.CharField(max_length=10, choices=AGG_CHOICES)
    log_info = models.JSONField(default=list, blank=True)


class FindAreaModel(models.Model):
    requestType = models.CharField(max_length=15, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    north = models.DecimalField(max_digits=25, decimal_places=20)
    east = models.DecimalField(max_digits=25, decimal_places=20)
    south = models.DecimalField(max_digits=25, decimal_places=20)
    west = models.DecimalField(max_digits=25, decimal_places=20)
    spatialResolution = models.DecimalField(max_digits=3, decimal_places=2)
    aggregation = models.CharField(max_length=10, choices=AGG_CHOICES)
    filterPredicate = models.CharField(max_length=2, choices=FILTER_PREDICATE_CHOICES)
    filterValue = models.FloatField()


class FindTimeModel(models.Model):
    requestType = models.CharField(max_length=15, choices=REQUEST_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    variable = models.CharField(max_length=50, choices=VARIABLE_CHOICES)
    startDateTime = models.DateTimeField()
    endDateTime = models.DateTimeField()
    temporalResolution = models.CharField(max_length=10, choices=TEMPORAL_CHOICES)
    north = models.DecimalField(max_digits=25, decimal_places=20)
    east = models.DecimalField(max_digits=25, decimal_places=20)
    south = models.DecimalField(max_digits=25, decimal_places=20)
    west = models.DecimalField(max_digits=25, decimal_places=20)
    aggregation = models.CharField(max_length=10, choices=AGG_CHOICES)
    filterPredicate = models.CharField(max_length=2, choices=FILTER_PREDICATE_CHOICES, null=True)
    filterValue = models.FloatField(null=True)
