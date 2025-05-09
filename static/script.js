const BASE_URL = "https://5000-megwana-aethernet-klhkwxd5dy5.ws-eu118.gitpod.io"; // Update Flask API URL

let temperatureChart, humidityChart, tankLevelChart;

// Function to initialize charts
function createCharts() {
    const ctxTemp = document.getElementById("temperatureChart").getContext("2d");
    const ctxHumidity = document.getElementById("humidityChart").getContext("2d");
    const ctxTank = document.getElementById("tankLevelChart").getContext("2d");

    temperatureChart = new Chart(ctxTemp, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Temperature (°C)", data: [], borderColor: "#00ffee", fill: false }] },
        options: { responsive: true }
    });

    humidityChart = new Chart(ctxHumidity, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Humidity (%)", data: [], borderColor: "#A100FF", fill: false }] },
        options: { responsive: true }
    });

    tankLevelChart = new Chart(ctxTank, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Tank Level (%)", data: [], borderColor: "#39FF14", fill: false }] },
        options: { responsive: true }
    });
}

// Function to fetch and update data
function fetchSensorData() {
    fetch(`${BASE_URL}/api/sensor-data`)  // Use API route for JSON data
        .then(response => response.json())
        .then(data => {
            let currentTime = new Date().toLocaleTimeString();

            // ✅ Update UI Text Elements
            document.getElementById("temperature").innerText = `${data.temperature} °C`;
            document.getElementById("humidity").innerText = `${data.humidity} %`;
            document.getElementById("rainfall").innerText = data.rainfall ? "Yes" : "No";
            document.getElementById("tankLevel").innerText = `${data.tank_level} %`;
            document.getElementById("hvacLoad").innerText = `${data.hvac_load} %`;
            document.getElementById("decision").innerText = data.system_decision;

            // ✅ Update Graphs
            temperatureChart.data.labels.push(currentTime);
            temperatureChart.data.datasets[0].data.push(data.temperature);
            temperatureChart.update();

            humidityChart.data.labels.push(currentTime);
            humidityChart.data.datasets[0].data.push(data.humidity);
            humidityChart.update();

            tankLevelChart.data.labels.push(currentTime);
            tankLevelChart.data.datasets[0].data.push(data.tank_level);
            tankLevelChart.update();
        })
        .catch(error => console.error("Error fetching data:", error));
}

function overrideDecision(action) {
    fetch(`${BASE_URL}/api/override?decision=${action}`, { method: "GET" })
        .then(response => response.json())
        .then(data => {
            alert(`System Override: ${data.new_decision}`);
            document.getElementById("decision").innerText = data.new_decision; // ✅ Update UI
        })
        .catch(error => console.error("Error overriding decision:", error));
}

// Initialize Charts and Set Refresh Interval
document.addEventListener("DOMContentLoaded", () => {
    createCharts();
    setInterval(fetchSensorData, 5000); // Updates data every 5 seconds
});

