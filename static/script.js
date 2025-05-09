let temperatureChart, humidityChart, tankLevelChart;

function createCharts() {
    const ctxTemp = document.getElementById("temperatureChart").getContext("2d");
    const ctxHumidity = document.getElementById("humidityChart").getContext("2d");
    const ctxTank = document.getElementById("tankLevelChart").getContext("2d");

    temperatureChart = new Chart(ctxTemp, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Temperature (°C)", data: [], borderColor: "#00ffee", fill: false }] },
        options: { 
            responsive: true,
            maintainAspectRatio: false // Allows chart to stretch to fill container
        }
    });

    humidityChart = new Chart(ctxHumidity, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Humidity (%)", data: [], borderColor: "#A100FF", fill: false }] },
        options: { 
            responsive: true,
            maintainAspectRatio: false
        }
    });

    tankLevelChart = new Chart(ctxTank, {
        type: "line",
        data: { labels: [], datasets: [{ label: "Tank Level (%)", data: [], borderColor: "#39FF14", fill: false }] },
        options: { 
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

    // Function to fetch and update data
    function fetchSensorData() {
        fetch(`${BASE_URL}/api/sensor-data`) // Use API route for JSON data
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
                // ✅ Show Visual Confirmation
                const overrideMessage = document.getElementById("overrideMessage");
                overrideMessage.innerText = `Override Applied: ${data.new_decision}`;
                overrideMessage.style.opacity = "1"; // Make it visible
                overrideMessage.style.transform = "scale(1)"; // Animate visibility

                // ✅ Update Decision Box
                document.getElementById("decision").innerText = data.new_decision;

                // ✅ Hide Message After 5 Seconds
                setTimeout(() => {
                    overrideMessage.style.opacity = "0"; 
                    overrideMessage.style.transform = "scale(0.9)";
                }, 5000);
            })
            .catch(error => console.error("Error overriding decision:", error));
    }

    const thresholdForm = document.getElementById("thresholdForm");

    if (thresholdForm) {
        thresholdForm.addEventListener("submit", function (event) {
            event.preventDefault();  // ✅ Stops default form submission

            const humidityThreshold = document.getElementById("humidityThreshold").value;
            const temperatureThreshold = document.getElementById("temperatureThreshold").value;

            fetch(`${BASE_URL}/api/set-thresholds`, {  // ✅ Sends user-defined thresholds to Flask API
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ humidity: humidityThreshold, temperature: temperatureThreshold })
            })
            .then(response => response.json())
            .then(data => {
                const saveMessage = document.getElementById("saveMessage");

                if (saveMessage) {  // ✅ Ensures feedback message exists
                    saveMessage.style.opacity = "1";  // ✅ Shows confirmation
                    setTimeout(() => saveMessage.style.opacity = "0", 3000);  // ✅ Hides after 3 seconds
                }
            })
            .catch(error => console.error("Error saving thresholds:", error));
        });
    }
        
    // Initialize Charts and Set Refresh Interval
    document.addEventListener("DOMContentLoaded", () => {
        createCharts();
        setInterval(fetchSensorData, 5000); // Updates data every 5 seconds
    });