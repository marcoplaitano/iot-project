// called when the page loads for the first time
function initPage() {
    clearInput();
    initClient();
    initChart("Temperature", "#ef6461", 15, 40);
}


function updateVariables(data) {
    // the client receives the 4 variables in one message, separated by blank spaces.
    // the order is: MAX_TEMP, MIN_TEMP, COVER_TIME, UNCOVER_TIME
    // the message is retained so that every time this client connects to the broker,
    // it receives these values
    values = data.split(" ", 4);

    // updates the values
    for (var i = 0; i < values.length; i++)
        VARIABLES[i] = values[i];

    // the input boxes let the user change the value of these variables
    inputBoxes = document.getElementsByClassName("input-box");
    // the MAX_TEMP input must be at least MIN_TEMP + 0.10
    inputBoxes[MAX_TEMP].min = parseFloat(VARIABLES[MIN_TEMP]) + 0.10;
    // the MIN_TEMP input must be at most MAX_TEMP - 0.10
    inputBoxes[MIN_TEMP].max = parseFloat(VARIABLES[MAX_TEMP]) - 0.10;
    // sets the placeholders to the current values
    inputBoxes[MAX_TEMP].placeholder = parseFloat(VARIABLES[MAX_TEMP]);
    inputBoxes[MIN_TEMP].placeholder = parseFloat(VARIABLES[MIN_TEMP]);
}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one message, separated by blank spaces.
    // the order is: temperature, humidity, brightness
    var value = data.split(" ", 3)[0];
    var temperature = parseFloat(value).toPrecision(4);
    document.getElementById("temp-value").innerHTML = temperature + " °C";
    updateChart(temperature);
}
