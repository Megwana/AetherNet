function fetchSensorData() {
    fetch("http://127.0.0.1:5000/sensor-data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("temperature").innerText = data.temperature;
            document.getElementById("humidity").innerText = data.humidity;
            document.getElementById("rainfall").innerText = data.rainfall ? "Yes" : "No";
            document.getElementById("tankLevel").innerText = data.tank_level;
            document.getElementById("decision").innerText = data.system_decision;
        })
        .catch(error => console.error("Error fetching data:", error));
}

// Auto-refresh data every 5 seconds
setInterval(fetchSensorData, 5000);
fetchSensorData();
