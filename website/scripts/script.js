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
    inputBoxes = document.getElementsByClassName("input-box");
    for (var i = 0; i < inputBoxes.length; i++)
        inputBoxes[i].value = "";
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
    mqttClient.subscribe("iot/data/#");
    // asks for the current state of the devices if no data has been received yet
    devices = ["fan", "sunshield", "led"];
    devices.forEach(device => {
        deviceState = sessionStorage.getItem(device);
        if (deviceState == null)
            publish("iot/commands/" + device, "get-state");
        else
            updateDeviceState(device, deviceState);
    });
}


function onDisconnect(responseObject) {
    if (responseObject.errorCode !== 0)
        alert("lost connection to broker! Please reload page");
}


function onMessageReceived(message) {
    if (message.destinationName == "iot/data/variables")
        updateVariables(message.payloadString);
    else if (message.destinationName == "iot/data/sensors")
        updateSensorsData(message.payloadString);
    else {
        device = message.destinationName.substr(9);
        updateDeviceState(device, message.payloadString);
    }
}


function publish(topic, data, retain = false, qos = 0) {
    message = new Paho.MQTT.Message(data);
    message.destinationName = topic;
    message.retained = retain;
    message.qos = qos;
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


function updateDeviceState(device, data) {
    element = document.getElementById(device + "-state");
    if (element != null)
        element.innerHTML = data;
    sessionStorage.setItem(device, data);
}


// called whenever the user modifies the value of the input box.
// this function checks wether the "update value" button should be
// disabled based on the input value
function toggleButton(inputBox) {
    string = inputBox.value;
    value = parseFloat(string);
    buttonId = inputBox.id.substr(6);
    button = document.getElementById(buttonId);

    if (string.length == 0 || value == null) {
        button.className = "inactive-btn";
        button.disabled = true;
    }
    else if (value < parseFloat(inputBox.min) || value > parseFloat(inputBox.max)) {
        button.className = "inactive-btn";
        button.disabled = true;
    }
    else {
        button.className = "active-btn";
        button.disabled = false;
    }
}


// when one of the variables is updated, the client sends a mqtt message with
// retain set to true so that the device will always receive the updated values
// when it connects to the broker.
function sendVariables(button) {
    newValue = parseFloat(document.getElementById("input-" + button.id).value);
    if (newValue == null)
        return;

    if (button.id == "max-temp")
        VARIABLES[MAX_TEMP] = newValue;
    else if (button.id == "min-temp")
        VARIABLES[MIN_TEMP] = newValue;
    else if (button.id == "cover-time")
        VARIABLES[COVER_TIME] = newValue;
    else if (button.id == "uncover-time")
        VARIABLES[UNCOVER_TIME] = newValue;

    // creates a message containing all 4 variables separated by a space
    var message = "";
    for (var i = 0; i < VARIABLES.length; i++)
        message += VARIABLES[i] + " ";

    publish("iot/commands/variables", message, true, 0);
}
