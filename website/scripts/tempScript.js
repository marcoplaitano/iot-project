// called when the page loads for the first time
function initPage() {
    clearInput();
    initClient();
    initChart("Temperature", "#ef6461", 15, 40);
}


function setInputBoxes() {
    var inputMaxTemp = document.getElementById("input-max-temp");
    var inputMinTemp = document.getElementById("input-min-temp");

    // the MAX_TEMP input must be at least MIN_TEMP + 0.10
    inputMaxTemp.min = parseFloat(VARIABLES[MIN_TEMP] + 0.10).toPrecision(4).toString();
    // the MIN_TEMP input must be at most MAX_TEMP - 0.10
    inputMinTemp.max = parseFloat(VARIABLES[MAX_TEMP] - 0.10).toPrecision(4).toString();

    // sets the placeholders to the current values
    inputMaxTemp.placeholder = VARIABLES[MAX_TEMP].toPrecision(4);
    inputMinTemp.placeholder = VARIABLES[MIN_TEMP].toPrecision(4);
}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one JSON object
    var obj = JSON.parse(data);
    var temperature = parseFloat(obj["temperature"]).toPrecision(4);
    document.getElementById("temp-value").innerHTML = temperature + " °C";
    updateChart(temperature);
}
