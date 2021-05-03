// called when the page loads for the first time
function initPage() {
    initClient();
    initChart("Humidity", "#7067cf");
}


function updateVariables(data) {}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one message, separated by blank spaces.
    // the order is: temperature, humidity, brightness
    var value = data.split(" ", 3)[1];
    var humidity = parseFloat(value).toPrecision(4);

    document.getElementById("hum-value").innerHTML = humidity + " %";
    updateChart(humidity);
}
