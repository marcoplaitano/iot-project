// called when the page loads for the first time
function initPage() {
    initClient();
    initChart("Humidity", "#7067cf");
}


function setInputBoxes() {
    return;
}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one JSON object
    var obj = JSON.parse(data);
    var humidity = parseFloat(obj["humidity"]).toPrecision(4);
    document.getElementById("hum-value").innerHTML = humidity + " %";
    updateChart(humidity);
}
