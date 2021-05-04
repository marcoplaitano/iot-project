var VARIABLES = [0.0, 0.0, 0, 0];
// position in the array
const MAX_TEMP = 0;
const MIN_TEMP = 1;
const COVER_TIME = 2;
const UNCOVER_TIME = 3;

var FAN_STATE = "not working";
var SUNSHIELD_STATE = "not covering";
var LED_STATE = "off";

var mqttClient;

var chart;
// maximum amount of values to display on the chart at any given time.
// 16 values taken every 2 seconds means I can show from 30 seconds ago to now
const CHART_MAX_VALUES = 16;



function clearInput() {
    // clears all the input boxes
    var inputBoxes = document.getElementsByClassName("input-box");
    for (var i = 0; i < inputBoxes.length; i++)
        inputBoxes[i].value = "";

    // disables the buttons for the client can not send empty strings
    var buttons = document.getElementsByClassName("btn");
    for (var i = 0; i < buttons.length; i++)
        buttons[i].disabled = true;
}


function initClient() {
    // creates the mqtt client and connects it to the broker's websocket, unencrypted port 8080
    mqttClient = new Paho.MQTT.Client("test.mosquitto.org", 8080, "iotMarcoWeb");
    mqttClient.onConnectionLost = onDisconnect;
    mqttClient.onMessageArrived = onMessageReceived;
    mqttClient.connect({
        onSuccess: onConnect,
        keepAliveInterval: 0,
    });
}


function initChart(chartLabel, chartColor, min = 0, max = 100) {
    chart = new Chart(document.getElementById("chart"), {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: chartLabel,
                backgroundColor: chartColor,
                borderColor: chartColor,
                data: [],
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    suggestedMin: min,
                    suggestedMax: max
                }
            }
        }
    });
}


function onConnect() {
    console.log("CONNECTED");
    mqttClient.subscribe("iot-marco/data/#");
    // asks for the variables' current values
    publish("iot-marco/commands/get-variables");
    // asks for the current state of the devices
    publish("iot-marco/commands/get-devices");
}


function onDisconnect(response) {
    if (response.errorCode !== 0) {
        console.log("DISCONNECTED WITH ERROR:", response.errorMessage);
        alert("Lost connection to broker! Please reload page.");
    }
}


function onMessageReceived(message) {
    var topic = message.destinationName;
    var payload = message.payloadString;

    if (topic == "iot-marco/data/variables")
        updateVariables(payload);
    else if (topic == "iot-marco/data/sensors")
        updateSensorsData(payload);
    else if (topic == "iot-marco/data/devices")
        setDevicesInitialState(payload);
    else {
        var device = topic.substr(15);
        updateDeviceState(device, payload);
    }
}


function publish(topic, data = "", retain = false) {
    var message = new Paho.MQTT.Message(data.toString());
    message.destinationName = topic;
    message.retained = retain;
    message.qos = 0;
    mqttClient.send(message);
}


function updateChart(newValue) {
    // pushes the new value to the chart's data array
    chart.data.labels.push("now");
    chart.data.datasets[0].data.push(newValue);
    // all the other values have to update their labels based on the amount of time
    // that has passed since they have been added to the chart
    for (var i = chart.data.labels.length - 1; i > 0; i--)
        chart.data.labels[chart.data.labels.length - i - 1] = (i * 2).toString() + " sec";
    chart.update();

    // the oldest value is deleted from the chart
    if (chart.data.datasets[0].data.length > CHART_MAX_VALUES) {
        chart.data.datasets[0].data.shift();
        chart.data.labels.shift();
        chart.update();
    }
}


function updateVariables(data) {
    // the client receives the 4 variables in a JSON object.
    var obj = JSON.parse(data);

    // updates the values
    VARIABLES[MAX_TEMP] = parseFloat(obj["max temp"]);
    VARIABLES[MIN_TEMP] = parseFloat(obj["min temp"]);
    VARIABLES[COVER_TIME] = parseInt(obj["cover time"]);
    VARIABLES[UNCOVER_TIME] = parseInt(obj["uncover time"]);

    // to update placeholders and min/max values
    setInputBoxes();
}


// called when the webpage asks for the initial state of the devices
// and the control board responds with a message
function setDevicesInitialState(data) {
    // the message received is in the form of a JSON object
    var obj = JSON.parse(data);

    updateDeviceState("fan", obj['fan']);
    updateDeviceState("sunshield", obj['sunshield']);
    updateDeviceState("led", obj['led']);
}


// sets the new state for the given device in the HTML document
function updateDeviceState(device, newState) {
    var element = document.getElementById(device + "-state");
    if (element != null)
        element.innerHTML = newState;
}


// called whenever the user modifies the value of an input box. This function checks
// wether the "update value" button should be disabled based on the input
function toggleButton(inputBox) {
    var string = inputBox.value;
    var value = parseFloat(string);
    var buttonId = "btn-" + inputBox.id.substr(6);
    var button = document.getElementById(buttonId);

    if (string.length == 0 || value == null)
        button.disabled = true;
    else if (value < parseFloat(inputBox.min) || value > parseFloat(inputBox.max))
        button.disabled = true;
    else
        button.disabled = false;
}


// called when the user modifies the value of a variable in one of the input boxes.
// The page sends an update command to the esp32
function sendVariables(button) {
    // if the button has id "btn-max-temp" then the input box's id is "input-max-temp"
    var inputBoxId = "input-" + button.id.substr(4);

    var newValue = parseFloat(document.getElementById(inputBoxId).value).toPrecision(4);
    if (isNaN(newValue) || newValue == null)
        return;

    clearInput();

    if (button.id == "btn-max-temp")
        VARIABLES[MAX_TEMP] = newValue;
    else if (button.id == "btn-min-temp")
        VARIABLES[MIN_TEMP] = newValue;
    else if (button.id == "btn-cover-time")
        VARIABLES[COVER_TIME] = parseInt(newValue);
    else if (button.id == "btn-uncover-time")
        VARIABLES[UNCOVER_TIME] = parseInt(newValue);

    // creates a message containing all 4 variables in the form of a JSON object
    var obj = {
        "max temp": VARIABLES[MAX_TEMP],
        "min temp": VARIABLES[MIN_TEMP],
        "cover time": VARIABLES[COVER_TIME],
        "uncover time": VARIABLES[UNCOVER_TIME]
    }
    var message = JSON.stringify(obj);

    // the message is retained so that the esp32 will always start with
    // the updated values when it boots up and connects to the broker. Moreover,
    // the esp32 always responds to a "set-variables" command with an "ACK" message.
    // This means that the webpage too will always receive the newest values when started.
    publish("iot-marco/commands/set-variables", message, true);
}
