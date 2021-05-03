// called when the page loads for the first time
function initPage() {
    clearInput();
    initClient();
    initChart("Brightness", "#1b998b", 0, 4000);
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
    // sets the placeholders to the current values
    inputBoxes[0].placeholder = parseFloat(VARIABLES[COVER_TIME]);
    inputBoxes[1].placeholder = parseFloat(VARIABLES[UNCOVER_TIME]);
}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one message, separated by blank spaces.
    // the order is: temperature, humidity, brightness
    var value = data.split(" ", 3)[2];
    var brightness = parseInt(value);
    document.getElementById("light-value").innerHTML = brightness;
    updateChart(brightness);
}
