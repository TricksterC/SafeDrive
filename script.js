let speedDisplay = document.getElementById("speedValue");
let road = document.getElementById("road");

// Initial speed settings
let speed = 100; // Default speed is 100 km/h
let shutEyeActive = false;

// WebSocket connection to Flask server
const socket = io.connect("http://127.0.0.1:5000");

// Listen for drowsiness alerts from the server
socket.on("drowsiness_alert", (data) => {
    console.log("Received drowsiness_alert:", data); // Debug log
    if (data.status === "SHUT_EYE") {
        shutEyeActive = true; // Drowsiness detected
    } else {
        shutEyeActive = false; // Drowsiness not detected
    }
    console.log("shutEyeActive:", shutEyeActive); // Debug log
});

// Function to update speed display and adjust lane speed
function updateSpeed() {
    if (shutEyeActive) {
        speed = 70; // Slow down to 70 km/h when drowsiness is detected
        speedDisplay.style.color = "red"; // Change text color to red when slowing
    } else {
        speed = 100; // Reset speed to 100 km/h when no drowsiness is detected
        speedDisplay.style.color = "green"; // Change text color to green when normal
    }

    speedDisplay.textContent = `Speed: ${speed} km/h`; // Update speed display
    setTimeout(updateSpeed, 1000); // Repeat every 1 second
}

// Function to create lane markings for road simulation
function createLaneMarkings() {
    for (let i = 0; i < 10; i++) {
        let lane = document.createElement("div");
        lane.className = "lane";
        lane.style.top = i * 60 + "px";
        road.appendChild(lane);
    }
}

// Function to move the lanes based on speed
function moveLanes() {
    let lanes = document.querySelectorAll(".lane");
    lanes.forEach(lane => {
        let currentTop = parseInt(lane.style.top);
        currentTop += speed / 50; // Adjust lane speed based on car speed
        if (currentTop > window.innerHeight) {
            currentTop = -30; // Reset lane position when it goes off-screen
        }
        lane.style.top = currentTop + "px";
    });
    requestAnimationFrame(moveLanes); // Continuously update lane movement
}

// Initialize everything
createLaneMarkings(); // Create lane markings
updateSpeed(); // Start updating speed
moveLanes(); // Start moving lanes