// called when the page loads for the first time
function initPage() {
    clearInput();
    initClient();
    initChart("Brightness", "#1b998b", 0, 4000);
}


function setInputBoxes() {
    var inputCoverTime = document.getElementById("input-cover-time");
    var inputUncoverTime = document.getElementById("input-uncover-time");

    // sets the placeholders to the current values
    inputCoverTime.placeholder   = COVER_TIME.toString();
    inputUncoverTime.placeholder = UNCOVER_TIME.toString();
}


function updateSensorsData(data) {
    // the client receives the 3 sensors' values in one JSON object
    var obj = JSON.parse(data);
    var brightness = parseInt(obj["brightness"]);
    document.getElementById("light-value").innerHTML = brightness;
    updateChart(brightness);
}
