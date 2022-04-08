var rocketHeightChart = dc.lineChart("#rocket-height-line-chart")
var rocketAirPressureChart = dc.lineChart("#rocket-air-pressure-line-chart")
var rocketHumidityChart = dc.lineChart("#rocket-humidity-line-chart")
var rocketTemperatureChart = dc.lineChart("#rocket-temperature-line-chart")
var connection = new WebSocket('ws://localhost:8001/websocket')

var currentData = '{"rocketData":[{"Time": 0,"Height": 0,"AirPressure": 0,"Humidity": 0,"Temperature": 0,"Latitude": 0,"Longitude": 0}]}';

var Latitude
var Longitude

//Returns if webSocket connection is open
function isOpen(ws) {
    return ws.readyState === ws.OPEN
}

waitChain()

//TODO Doesn't work right, is supposed to update to Open Green once webSocket connects
function waitChain() {
    var msg = {
        wait: "true"
    }
    if (!isOpen(connection)) {
        console.log("Socket is Closed!")
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Closed 🔴';
        return;
    }
    else {
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Open 🟢';
    }
    connection.send(JSON.stringify(msg));
}

//Sends json over webSocket to websocket_server.py which initiates the tornado loop
function startRecording() {
    var msg = {
        run: "true",
        date: Date.now()
    }
    if (!isOpen(connection)) {
        console.log("Socket is Closed!")
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Closed 🔴';
        return;
    }
    else {
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Open 🟢';
    }
    connection.send(JSON.stringify(msg));
}

//TODO Doesn't work correctly
function stopRecording() {
    var msg = {
        run: "false",
        date: Date.now()
    }
    if (!isOpen(connection)) {
        console.log("Socket is Closed!")
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Closed 🔴';
        return;
    }
    else {
        document.getElementById('websocket-status').innerHTML
            = 'Socket Status: Open 🟢';
    }
    connection.send(JSON.stringify(msg));
    document.getElementById('googleMaps').innerHTML = 'https://www.google.com/maps/@' + Latitude + ',' + Longitude;
}

//resets chart data by calling the resetData() function and then reinitializes the csv json data to it's
//initial state
function resetRecording() {
    resetData(1, [timeDim, heightDim, airPressureDim, humidityDim, temperatureDim]);
    currentData = '{"rocketData":[{"Time": 0,"Height": 0,"AirPressure": 0,"Humidity": 0,"Temperature": 0,"Latitude": 0,"Longitude": 0}]}';
}

//this is here to make it easier to add more things to this function if needed
function saveRecording() {
    getCSV()
}

//initial json graph variable
var data1 = [
    {Time: 0, Height: 0, AirPressure: 0, Humidity: 0, Temperature: 0}
];

// set crossfilter with first dataset; time
var xfilter = crossfilter(data1),
    timeDim  = xfilter.dimension(function(d) {return +d.Time;}),
    heightDim = xfilter.dimension(function(d) {return +d.Height;})
    airPressureDim = xfilter.dimension(function(d) {return +d.AirPressure;})
    humidityDim = xfilter.dimension(function(d) {return +d.Humidity;})
    temperatureDim = xfilter.dimension(function(d) {return +d.Temperature;})

    heightPerTime = timeDim.group().reduceSum(function(d) {return +d.Height;});
    airPressurePerTime = timeDim.group().reduceSum(function(d) {return +d.AirPressure;});
    humidityPerTime = timeDim.group().reduceSum(function(d) {return +d.Humidity;});
    temperaturePerTime = timeDim.group().reduceSum(function(d) {return +d.Temperature;});

//creates and sets the graph properties
function render_plots(){
    rocketHeightChart
        .width(425)
        .height(385)
        .x(d3.scaleLinear().range(d3.schemeCategory10))
        .y(d3.scaleLinear().domain([0, 1500]))
        .brushOn(false)
        .xAxisLabel("Time (s)")
        .yAxisLabel("Height (ft)")
        .dimension(timeDim)
        .group(heightPerTime)
        .elasticX(true)
        .elasticY(true)
        .xAxis().ticks(10)
    rocketAirPressureChart      
        .width(425)
        .height(385)
        .x(d3.scaleLinear().range(d3.schemeCategory10))
        .y(d3.scaleLinear())
        .brushOn(false)
        .xAxisLabel("Time (s)")
        .yAxisLabel("Air Pressure (n/m^2)")
        .dimension(timeDim)
        .group(airPressurePerTime)
        .elasticX(true)
        .elasticY(true)        
    rocketHumidityChart
        .width(425)
        .height(385)
        .x(d3.scaleLinear().range(d3.schemeCategory10))
        .y(d3.scaleLinear())
        .brushOn(false)
        .xAxisLabel("Time (s)")
        .yAxisLabel("Humidity (g/cm^3)")
        .dimension(timeDim)
        .group(humidityPerTime)
        .elasticX(true)
        .elasticY(true)
    rocketTemperatureChart
        .width(425)
        .height(385)
        .x(d3.scaleLinear().range(d3.schemeCategory10))
        .y(d3.scaleLinear())
        .brushOn(false)
        .xAxisLabel("Time (s)")
        .yAxisLabel("Temperature (C°)")
        .dimension(timeDim)
        .group(temperaturePerTime)
        .elasticX(true)
        .elasticY(true) 
    dc.renderAll();
}
render_plots();

// data reset function (adapted)
// I don't know what ndx is for or means; is currently not used
function resetData(ndx, dimensions) {
    var rocketHeightFilters = rocketHeightChart.filters();
    var rocketAirPressureFilters = rocketAirPressureChart.filters();
    var rocketHumidityFilters = rocketHumidityChart.filters();
    var rocketTemperatureFilters = rocketTemperatureChart.filters();

    rocketHeightChart.filter(null);
    rocketAirPressureChart.filter(null);
    rocketHumidityChart.filter(null);
    rocketTemperatureChart.filter(null);

    xfilter.remove();

    rocketHeightChart.filter([rocketHeightFilters]);
    rocketAirPressureChart.filter([rocketAirPressureFilters])
    rocketHumidityChart.filter([rocketHumidityFilters])
    rocketTemperatureChart.filter([rocketTemperatureFilters])
}

//updates the js object for the graphs with data that is sent from the webSocket
connection.onmessage = function(event) {
    var newData = JSON.parse(event.data);
    var updateObject =[{
        "Time": newData.Time,
        "Height": newData.Height,
        "AirPressure": newData.AirPressure,
        "Humidity": newData.Humidity,
        "Temperature": newData.Temperature,
    }]

    var objCurrentData = JSON.parse(currentData);
    objCurrentData['rocketData'].push({"Time": newData.Time, "Height": newData.Height, "AirPressure": newData.AirPressure, "Humidity": newData.Humidity, "Temperature": newData.Temperature, "Latitude": newData.Latitude, "Longitude": newData.Longitude});
    currentData = JSON.stringify(objCurrentData);
    Latitude = newData.Latitude
    Longitude = newData.Longitude
    document.getElementById("lat-gps").innerHTML = newData.Latitude;
    document.getElementById("long-gps").innerHTML = newData.Longitude;

    //resetData(1, [timeDim, heightDim, airPressureDim, humidityDim, temperatureDim]);
    xfilter.add(updateObject);
    dc.redrawAll();
}

//Parses the currentData as a js object then converts the object to a csv json formatted then calls getFormattedTime() and sets that
//as the download file name
function getCSV() {
    const items = JSON.parse(currentData).rocketData
    const replacer = (key, value) => value === null ? '' : value // specify how you want to handle null values here
    const header = Object.keys(items[0])
    const csv = [
      header.join(','), // header row first
      ...items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
    ].join('\r\n')
    
    var downloadLink = document.createElement("a");
    var blob = new Blob(["\ufeff", csv]);
    var url = URL.createObjectURL(blob);
    downloadLink.href = url;
    downloadLink.download = getFormattedTime() +'.csv';
    
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

//Gets time and date as: 2022-3-1-13-17-29
function getFormattedTime() {
    var today = new Date();
    var y = today.getFullYear();
    // JavaScript months are 0-based.
    var m = today.getMonth() + 1;
    var d = today.getDate();
    var h = today.getHours();
    var mi = today.getMinutes();
    var s = today.getSeconds();
    return y + "-" + m + "-" + d + "-" + h + "-" + mi + "-" + s;
}