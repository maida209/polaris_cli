from .query_executor import QueryExecutor
from .query_executor_heatmap import HeatmapExecutor

from .utils.const import DataRange


class FindAreaExecutor(QueryExecutor):
    def __init__(
        self,
        dr: DataRange,
        heatmap_aggregation_method: str,  # e.g., "mean", "max", "min"
        filter_predicate: str,  # e.g., ">", "<", "==", "!=", ">=", "<="
        filter_value: float,
    ):
        dr.temporal_resolution = "hour"
        super().__init__(
            dr=dr,
        )
        self.heatmap_aggregation_method = heatmap_aggregation_method
        self.filter_predicate = filter_predicate
        self.filter_value = filter_value

    def execute(self):
        return self._execute_baseline()

    def _execute_baseline(self):
        heatmap_executor = HeatmapExecutor(
            dr=self.dr,
            heatmap_aggregation_method=self.heatmap_aggregation_method,
        )
        hm = heatmap_executor.execute()
        if self.filter_predicate == ">":
            res = hm.where(hm > self.filter_value, drop=False)
        elif self.filter_predicate == "<":
            res = hm.where(hm < self.filter_value, drop=False)
        elif self.filter_predicate == "==":
            res = hm.where(hm == self.filter_value, drop=False)
        elif self.filter_predicate == "!=":
            res = hm.where(hm != self.filter_value, drop=False)
        elif self.filter_predicate == ">=":
            res = hm.where(hm >= self.filter_value, drop=False)
        elif self.filter_predicate == "<=":
            res = hm.where(hm <= self.filter_value, drop=False)
        else:
            raise ValueError("Invalid filter_predicate")
        res = res.fillna(False)
        res = res.astype(bool)
        return res
