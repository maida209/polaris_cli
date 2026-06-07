# Data object class to represent a data object in the Polaris API
class DataObject:
    def __init__(
        self,
        name,
        dataset,
        variable,
        start_t,
        end_t,
        t_res,
        latitude_range,
        longitude_range,
        space_res,
        aggregation
    ):
        self.name = name
        self.dataset = dataset
        self.variable = variable
        self.start_t = start_t
        self.end_t = end_t
        self.t_res = t_res
        self.latitude_range = latitude_range
        self.longitude_range = longitude_range
        self.space_res = space_res
        self.aggregation = aggregation

    def __str__(self):
        return f"{self.name}: {self.variable} ({self.start_t} → {self.end_t})"