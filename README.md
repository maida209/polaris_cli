# PolarIS API

1. [Introduction](#polaris-interactive-and-scalable-polar-science)
2. [Set Up](#set-up)
3. [Queries](#queries)
4. [IMPLEMENTATION General Tasks](#general-tasks)
5. [IMPLEMENTATION Code Outline](#code-outline)

## PolarIS: Interactive and Scalable Polar science

PolarIS is a data infrastructure that:

1. Stores data for polar scientists to query.
2. Pre-processes the data to speed up the supported queries.
3. Obtains data needed for queries from remote repositores. 
4. Automatically updates the data in storage to serve users.
<!-- 5. Integrates data from different datasets. Integrating may include regridding, upsampling, downsampling, etc.. -->

**How it works:**

You can establish a connection to the PolarIS data server from your local computer. While this connection is active, you can access and query the data stored in PolarIS.

If PolarIS does not have the data needed to answer a given query, PolarIS will obtain the data from the remote repository, and answer the query when all the data is available.

## Set-up

1. Install PolarIS

        pip install polar-is


    **<span style="color:blue">IMPLEMENTATION NOTES:</span>**
    * <span style="color:blue">This should download all dependencies and polari-is code from the Python Package Index (PyPI)</span>
    * <span style="color:blue">This will be implemented at the end when we make the code a package </span>


2. *Optional:* Create a file in your home directory that defines the directory you want your query results to download to, and save the email you want polar-is to send data notifications to. If this file does not exist:
    * Results will be downloaded to the directory polar-is is running in
    * No notifications will be sent when data is downloaded.
    

    **<span style="color:blue">IMPLEMENTATION NOTES:</span>** 
    * <span style="color:blue">Maybe it can work similarly to or be a `.` file like `.cdsapi`</span>


3. Connect to PolarIS

    In a terminal window, run:

            polar-is -activate


    **<span style="color:blue">IMPLEMENTATION NOTES:</span>**
    * <span style="color:blue">Command that starts a connection between user and server, similar to how you start a client terminal to run PostgreSQL. The command text does not have to be the command above.</span>
    * <span style="color:blue">Use `gRPC` for this communication.</span>


4. Run queries

    You can run the [supported queries](#queries) in the terminal window. Some queries will print out the result in the terminal. Data downloads or plots will be sent to the directory specified in (step 2) or in the current directory.


5. Close connection

        quit()

    or some other call

## Queries

In the terminal session, you can perform the following queries:

1. [Available Data](#available_data)
2. [Data Object](#data_object)
3. [Plot](#plot) Supported plots (defined in section): timeseries, heatmap, find area, find time
4. [Get Data](#get_data)


### avaliable_data

<table class="tg"><thead>
  <tr>
    <th class="tg-7ryv" colspan="3">available_data(dataset=<span style="font-style:italic">None</span>, variable=<span style="font-style:italic">None</span>)</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-zci2">Description</td>
    <td class="tg-0lax" colspan="2">Prints a list of the data currently in storage that match the filters given as parameters.<br>If no parameters are given, all the data currently in storage will be printed.</td>
  </tr>
  <tr>
    <td class="tg-zci2">Parameters</td>
    <td class="tg-0lax" colspan="2">dataset [list]: the dataset(s) of interest.<br>variable [list]: the variable(s) of interest.</td>
  </tr>
  <tr>
    <td class="tg-zci2">Output</td>
    <td class="tg-0lax" colspan="2">None. Text listing available data will print in the terminal window.</td>
  </tr>
</tbody>
</table>


   **<span style="color:blue"> IMPLEMENTATION NOTES:</span>**
   * <span style="color:blue">Get the available data from the `metadata.csv` file.</span>
   * <span style="color:blue">Filter out `metadata.csv` info by the given parameters.</span>
   * <span style="color:blue">Print-out should be in table or other readable format (e.g., not just comma separated text), sorted by: dataset, then variable, time, temporal resolution, minimum latitude, minimum longitude, spatial resolution, and aggregation.</span>
   * <span style="color:blue">`available_data()` can be a different call.</span>

**Example:**

`available_data(variable=[2m_temperature])`

**Returns:** 

| Dataset 	| Variable       	| Time      	| ...                    	| Spatial Resolution| Aggregation    	|
|---------	|----------------	|-----------	|------------------------	|------------------	|----------------	|
| CARRA   	| 2m_temperature   	| 2015-2022 	| ...                   	| 2.5km squared   	| mean           	|
| ERA5    	| 2m temperature 	| 2010-2020 	| ...                   	| 0.5 degrees      	| mean          	|
| ERA5    	| 2m_temperature  	| 2022-2022     | ...                    	| 1 degrees      	| ...            	|

### data_object

<table class="tg"><thead>
  <tr>
    <th class="tg-7ryv" colspan="3">data_object(*)</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-zci2">Description</td>
    <td class="tg-0lax" colspan="2">Makes an object `DataObject` that keeps a certain data parameter subset. <br>This object can be passed to queries in lieu of typing out data parameters multiple times.</td>
  </tr>
  <tr>
    <td class="tg-zci2">Parameters</td>
    <td class="tg-0lax" colspan="2">name [string] name of data object.<br>dataset [string]<br>variable [string]<br>start_t [string] time in YYYY-MM-DD HH:mm format<br>end_t [string] time in YYYY-MM-DD HH:mm format<br>t_res [string] Options: finest, hour, day, month, year<br>latitude_range [tuple] (minimum latitude value, maximum latitude value)<br>longitude_range [tuple] (minimum longitude value, maximum longitude value)<br>space_res [float]<br>aggregation [string] Options: mean, minimum, maximum</td>
  </tr>
  <tr>
    <td class="tg-zci2">Output</td>
    <td class="tg-0lax" colspan="2">`DataObject` will be saved under the given name.</td>
  </tr>
</tbody></table>

   **<span style="color:blue"> IMPLEMENTATION NOTES:</span>**
   * <span style="color:blue">Can be implemented however, but need to keep this object available for the whole session.</span>
   * <span style="color:blue">Need to make it readable to the functions as input (can make a parser function or save it so it is the same as the function inputs, whatever works).</span>

### plot

<table class="tg"><thead>
  <tr>
    <th class="tg-7ryv" colspan="3">plot(data=DataObject, type=<span style="font-style:italic">timeseries</span>, args*)</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-zci2">Description</td>
    <td class="tg-0lax" colspan="2">Plots the requested plot of the data specified by the data object. Returns the plot image to the local computer.</td>
  </tr>
  <tr>
    <td class="tg-zci2">Parameters</td>
    <td class="tg-0lax" colspan="2">data [DataObject] data specificatons<br>type [string] Options: timeseries, heatmap, find_time, find_area<br><br>Required for find_time and find_area type plots: <br>filter [string] Options: =, &lt;, &gt;, !=<br>value [float] Value to compare data to using filter</td>
  </tr>
  <tr>
    <td class="tg-zci2">Output</td>
    <td class="tg-0lax" colspan="2">Plot image will be saved in the current directory or directory specified in (step 2)</td>
  </tr>
</tbody>
</table>

**timeseries** plots the values of the data at each time point aggregated over all the spatial region.

**heatmap** plots the values of the data at each region aggregated over all time.

**find time** plots the time points in the dataset whose (aggregate) values satisfy the filter $\phi$ for value $V$. For example, let $x$ be temperature values, $\phi$ be $>$ and $V=265.4$ $x \phi V$ would be all the time points in the data where the temperature values are greater than 265.4K.

**find area** similar to the `find time` plot, it plots the regions in the dataset whose (aggregate) values satisfy the given filter and value.

   **<span style="color:blue"> IMPLEMENTATION NOTES:</span>**
   * <span style="color:blue">All the plots are already implemented in `django-react-starter/backend/api/iharp_query_processor/src`. This function should call those functions and send the png of the plot to the local computer.</span>
   * <span style="color:blue">How the backend for the interface currently sends this plot information to the frontend: `django-react-starter/backend/api/views.py`</span>

| **Plots**                                                                          	| **Main** 	| **Complete** 	|
|-----------------------------------------------------------------------------------	|----------	|--------------	|
| Main wrapper: calls the correct plot function                                         |          	|               |
| Function: timeseries                                                              	|          	|              	|
| Function: heatmap                                                                 	|          	|              	|
| Function: find time                                                               	|          	|              	|
| Function: find area                                                               	|          	|              	|

### get_data

<table class="tg"><thead>
  <tr>
    <th class="tg-7ryv" colspan="3">get_data(data=DataObject)</th>
  </tr></thead>
<tbody>
  <tr>
    <td class="tg-zci2">Description</td>
    <td class="tg-0lax" colspan="2">Downloads the requested data from the server to the local computer.</td>
  </tr>
  <tr>
    <td class="tg-zci2">Parameters</td>
    <td class="tg-0lax" colspan="2">data [DataObject] data specificatons</td>
  </tr>
  <tr>
    <td class="tg-zci2">Output</td>
    <td class="tg-0lax" colspan="2">Data will be saved in the current directory or directory specified in (step 2)</td>
  </tr>
</tbody>
</table>

   **<span style="color:blue"> IMPLEMENTATION NOTES:</span>**
   * <span style="color:blue">If the data is not available, print a message in terminal saying the data will be downloaded, send request to repository, and email user (if email provided) when the data is downloaded.</span>

## <span style="color:blue">General Tasks:</span>

<span style="color:blue">These tasks kind of touch multiple components. If you implement one of them, try to make it modular so others can use your code to do the same. E.g., if you write a function to print something out to the terminal, it would be good for others to be able to use it too.</span>


| **Task**                                                                          	| **Main** 	| **Complete** 	|
|-----------------------------------------------------------------------------------	|----------	|--------------	|
| Package functionality: keep track of all query logs, fine-grained query run stats 	|          	|              	|
| Package functionality: connect query monitor to polaris                           	|          	|              	|
| Package functionality: multiple users                                             	|          	|              	|
| Progress print statements: "data is plotting", "plot downloaded", errors, logs etc..  |          	|              	|
| Set limits: max request size/data download size                                   	|          	|              	|
| Data download updates: send email to say data is ready                            	|          	|              	|
| Return functions: raster of data, plot image, plot values                         	|          	|              	|
| Security: make users a code/key they need for our server to accept and start their session.                         	|          	|              	|

## <span style="color:blue">Code Outline</span>

<span style="color:blue">We are basically building another `frontend` for the PolarIS `backend`. Instead of the website, users start a session in their terminal and then send their queries from there. The package needs to let users connect to PolarIS, but the main additions to the code should be in the new folder: `django-react-starter/backend/terminal_api`.</span>

<span style="color:blue">The package code should have this structure:</span>

        polaris_api/
        ├── LICENSE
        ├── pyproject.toml
        ├── README.md
        ├── src/
        │   └── polar-is/
        │       ├── __init__.py
        │       └── utils.py
        │       └── <other scripts>.py
        └── tests/          <-- directory to put unit tests, etc. of functions
