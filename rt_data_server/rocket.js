var rocketHeightChart = dc.lineChart("#rocket-height-line-chart")
var rocketAirPressureChart = dc.lineChart("#rocket-air-pressure-line-chart")
var rocketHumidityChart = dc.lineChart("#rocket-humidity-line-chart")
var rocketTemperatureChart = dc.lineChart("#rocket-temperature-line-chart")
var connection = new WebSocket('ws://localhost:8001/websocket')


function isOpen(ws) {
    return ws.readyState === ws.OPEN
}

waitChain()

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
}

function resetRecording() {
    resetData(1, [timeDim, heightDim, airPressureDim, humidityDim, temperatureDim]);
}

function saveRecording() {
    getCSV()
}

var data1 = [
    {Time: 0, Height: 0, AirPressure: 0, Humidity: 0, Temperature: 0}
];
// set crossfilter with first dataset
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
connection.onmessage = function(event) {
    var newData = JSON.parse(event.data);
    var updateObject =[{
        "Time": newData.Time,
        "Height": newData.Height,
        "AirPressure": newData.AirPressure,
        "Humidity": newData.Humidity,
        "Temperature": newData.Temperature
    }]
    //resetData(1, [timeDim, heightDim, airPressureDim, humidityDim, temperatureDim]);
    xfilter.add(updateObject);
    dc.redrawAll();
}

function getCSV() {
const items = dc
const replacer = (key, value) => value === null ? '' : value // specify how you want to handle null values here
const header = Object.keys(items[0])
const csv = [
    header.join(','), // header row first
    ...items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','))
    ].join('\r\n')

console.log(csv)
var encodedUri = encodeURI(csv);
window.open(encodedUri);
}