import json
import os
import logging
import pickle
import geopandas as gpd
import plotly.express as px
import plotly.graph_objs as go
from django.http import JsonResponse, FileResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_naive
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shapely.geometry import Polygon


from .serializers import *
from .iharp_query_processor import *


logger = logging.getLogger(__name__)
MSG_FORMAT = "[%(asctime)s %(name)s-%(levelname)s]: %(message)s"
LOG_DATE_FORMAT = "%d/%b/%Y %H:%M:%S"
logging.basicConfig(level=logging.INFO, format=MSG_FORMAT, datefmt=LOG_DATE_FORMAT)

metadata_fpath = "/Users/Maida/django-react-starter/backend/metadata.csv" # "/data/metadata_post.csv"  ### TODO: change to correct metadata file path


def format_datetime_string(dt_input):
    """
    Convert input datetime
    from 2023-01-01T00:00:00.000Z
    to 2023-01-01 00:00:00
    """
    dt = parse_datetime(dt_input)
    if dt and dt.tzinfo is not None:
        dt = make_naive(dt)
    dt_formatted = dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None
    assert dt_formatted is not None, "Invalid datetime format"
    return dt_formatted


def get_variable_short_name(variable):
    return long_short_name_dict.get(variable, variable)


@api_view(["POST"])
def get_raster_query(request):
    logger.info("Get Raster Query")
    serializer = GetRasterSeriazlier(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        time_resolution = request.data.get("temporalResolution")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        spatial_resolution = float(request.data.get("spatialResolution"))
        aggregation = request.data.get("aggregation")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = GetRasterExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            temporal_resolution=time_resolution,
            spatial_resolution=spatial_resolution,
            aggregation=aggregation,
            log_info=None,
        )
        ds = qe.execute()
        response = ds.__str__()

        return Response(response, status=201)

    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def get_raster_query_pickle(request):
    logger.info("Get Raster Query, Return Xarray")
    serializer = GetRasterSeriazlier(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        time_resolution = request.data.get("temporalResolution")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        spatial_resolution = float(request.data.get("spatialResolution"))
        aggregation = request.data.get("aggregation")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = GetRasterExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            temporal_resolution=time_resolution,
            spatial_resolution=spatial_resolution,
            aggregation=aggregation,
        )
        ds = qe.execute()

        return Response(pickle.dumps(ds), status=201)

    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def download_query(request):
    logger.info("Get Raster Query")
    serializer = GetRasterSeriazlier(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        time_resolution = request.data.get("temporalResolution")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        spatial_resolution = float(request.data.get("spatialResolution"))
        aggregation = request.data.get("aggregation")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = GetRasterExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            temporal_resolution=time_resolution,
            spatial_resolution=spatial_resolution,
            aggregation=aggregation,
        )
        ds = qe.execute()

        tmp_dir = "tmp/data"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        rid = serializer.data["id"]
        file_name = f"for_download_{rid}.nc"
        file_path = f"{tmp_dir}/{file_name}"
        ds.to_netcdf(file_path)

        if os.path.exists(file_path):

            # TODO: Dynamically Delete written files.

            # def cleanup_file():
            #     print("Attempted Cleanup")
            #     if os.path.exists(file_path):
            #         os.remove(file_path)
            #         print(f"Removed {file_path}")

            response = FileResponse(open(file_path, "rb"), as_attachment=True)

            # response.close_connection = cleanup_file
            response["Content-Disposition"] = f'attachment; filename="{file_name}"'
            return response
        else:
            return JsonResponse({"error": "File not found"}, status=404)

    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=400)


@api_view(["POST"])
def timeseries_query(request):
    logger.info("Time Series Query")
    serializer = TimeSeriesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        time_resolution = request.data.get("temporalResolution")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        aggregation = request.data.get("aggregation")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = TimeseriesExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            temporal_resolution=time_resolution,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            aggregation=aggregation,
            time_series_aggregation_method=aggregation,
            log_info=None,
        )
        ts = qe.execute()

        short_variable = get_variable_short_name(variable)
        fig = go.Figure([go.Scatter(x=ts["time"], y=ts[short_variable])])
        json_fig = fig.to_json()
        json_data = json.loads(json_fig)

        log_info = qe.log_info[0]
        # print(f"[View] log_info = qe.log_info being sent to frontend: {log_info}")

        response_data = {
            "figure": json_data,
            "log": log_info
        }
        return JsonResponse(response_data, status=201)

    logger.error("Invalid data: %s", serializer.errors)
    return JsonResponse({"error": "Invalid data"}, status=400)


@api_view(["POST"])
def heatmap_query(request):
    logger.info("Heatmap Query")
    serializer = HeatmapSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        spatial_resolution = float(request.data.get("spatialResolution"))
        aggregation = request.data.get("aggregation")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = HeatmapExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            spatial_resolution=spatial_resolution,
            aggregation=aggregation,
            heatmap_aggregation_method=aggregation,
            log_info=None,
            range_info=None,
        )
        hm = qe.execute()

        var_short_name = get_variable_short_name(variable)
        fig = go.Figure(data=go.Heatmap(x=hm["longitude"], y=hm["latitude"], z=hm[var_short_name], colorscale="RdBu_r"))
        fig.update_traces(hovertemplate=f"lon: %{{x}}<br>lat: %{{y}}<br>{var_short_name}: %{{z}}<extra></extra>")
        fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1), xaxis=dict(constrain="domain"))
        json_fig = fig.to_json()
        json_data = json.loads(json_fig)

        log_info = qe.log_info[0]
        # print(f"[View] log_info = qe.log_info being sent to frontend: {log_info}")

        range_info = qe.range_info[0]

        response_data = {
            "figure": json_data,
            "log": log_info,
            "range": range_info,
        }
        return JsonResponse(response_data, status=201)

    logger.error("Invalid data: %s", serializer.errors)
    return JsonResponse({"error": "Invalid data"}, status=400)


@api_view(["POST"])
def find_time_query(request):
    logger.info("Find Time Query")
    serializer = FindTimeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        time_resolution = request.data.get("temporalResolution")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        aggregation = request.data.get("aggregation")

        filter_predicate = request.data.get("filterPredicate")
        filter_value = request.data.get("filterValue")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = FindTimeExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            temporal_resolution=time_resolution,
            aggregation=aggregation,
            time_series_aggregation_method=aggregation,
            filter_predicate=filter_predicate,
            filter_value=float(filter_value),
        )
        ft = qe.execute()

        var_short_name = get_variable_short_name(variable)
        # color_map = {True: "#005AB5", False: "#DC3220"}
        # fig = go.Figure(
        #     [
        #         go.Scatter(
        #             x=ft["time"],
        #             y=ft[var_short_name],
        #             mode="lines+markers",
        #             marker=dict(size=12, color=[color_map[i] for i in ft[var_short_name].values]),
        #             line=dict(color="lightgray"),
        #         )
        #     ]
        # )
        color_map = {True: "#005AB5", False: "#DC3220"}

        true_mask = ft[var_short_name] == True
        false_mask = ft[var_short_name] == False

        fig = go.Figure([
            go.Scatter(
                x=ft["time"][true_mask],
                y=ft[var_short_name][true_mask],
                mode="markers",
                marker=dict(size=12, color=color_map[True]),
                name="True"   # <-- legend label
            ),
            go.Scatter(
                x=ft["time"][false_mask],
                y=ft[var_short_name][false_mask],
                mode="markers",
                marker=dict(size=12, color=color_map[False]),
                name="False"  # <-- legend label
            )
        ])
        fig.update_layout(showlegend=True)
        json_fig = fig.to_json()
        json_data = json.loads(json_fig)

        return JsonResponse(json_data, status=201)

    logger.error("Invalid data: %s", serializer.errors)
    return JsonResponse({"error": "Invalid data"}, status=400)


@api_view(["POST"])
def find_area_query(request):
    logger.info("Find Area Query")
    serializer = FindAreaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        logger.info(request.data)

        variable = request.data.get("variable")
        start_datetime = request.data.get("startDateTime")
        end_datetime = request.data.get("endDateTime")
        north = round(float(request.data.get("north")), 3)
        south = round(float(request.data.get("south")), 3)
        east = round(float(request.data.get("east")), 3)
        west = round(float(request.data.get("west")), 3)
        spatial_resolution = float(request.data.get("spatialResolution"))
        aggregation = request.data.get("aggregation")
        filter_predicate = request.data.get("filterPredicate")
        filter_value = request.data.get("filterValue")

        formatted_start = format_datetime_string(start_datetime)
        formatted_end = format_datetime_string(end_datetime)

        qe = FindAreaExecutor(
            metadata=metadata_fpath,
            variable=variable,
            start_datetime=formatted_start,
            end_datetime=formatted_end,
            min_lat=south,
            max_lat=north,
            min_lon=west,
            max_lon=east,
            spatial_resolution=spatial_resolution,
            aggregation=aggregation,
            heatmap_aggregation_method=aggregation,
            filter_predicate=filter_predicate,
            filter_value=float(filter_value),
        )
        fa = qe.execute()

        fa_low = fa
        # fa_low = fa.isel(latitude=slice(0, len(fa["latitude"]), 4), longitude=slice(0, len(fa["longitude"]), 4))
        df = fa_low.to_dataframe().reset_index()
        df["latitude"] = df["latitude"] - 0.5
        df["longitude"] = df["longitude"] - 0.5
        df["latitude2"] = df["latitude"] + 1
        df["longitude2"] = df["longitude"] + 1
        gdf = gpd.GeoDataFrame(
            df,
            geometry=[
                Polygon([(x, y), (x, y2), (x2, y2), (x2, y)])
                for x, y, x2, y2 in zip(df["longitude"], df["latitude"], df["longitude2"], df["latitude2"])
            ],
        )
        var_short_name = get_variable_short_name(variable)
        color_mapping = {True: "#005AB5", False: "#DC3220"}
        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.geometry,
            locations=gdf.index,
            hover_data={var_short_name: ":.2f", "latitude": ":.3f", "longitude": ":.3f"},
            color=var_short_name,
            center={"lat": gdf["latitude"].mean(), "lon": gdf["longitude"].mean()},
            opacity=0.5,
            zoom=1,
            color_discrete_map=color_mapping,
        )

        fig.update_traces(
            hovertemplate=(
                "Lat: %{customdata[1]:.3f}<br>"
                + "Lon: %{customdata[2]:.3f}<br>"
                + f"{var_short_name}: %{{customdata[0]}}<br>"
                + "<extra></extra>"
            )
        )

        fig.update_traces(marker_line_width=0)
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_bounds_east=east,
            mapbox_bounds_north=north,
            mapbox_bounds_west=west,
            mapbox_bounds_south=south,
            mapbox_layers=[
                {
                    "below": "traces",
                    "sourcetype": "raster",
                    "sourceattribution": "United States Geological Survey",
                    "source": [
                        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                    ],
                }
            ],
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            showlegend=True,
            legend=dict(
                font=dict(size=11),
                x=1,  # Adjust the x position (0 to 1, 1 is far right)
                y=0.9,  # Adjust the y position (0 to 1, 1 is top)
                xanchor="right",  # Anchors the legend's x position
                yanchor="top",  # Anchors the legend's y position
            ),
        )

        json_fig = fig.to_json()
        json_data = json.loads(json_fig)

        return JsonResponse(json_data, status=201)

    logger.error("Invalid data: %s", serializer.errors)
    return JsonResponse({"error": "Invalid data"}, status=400)
