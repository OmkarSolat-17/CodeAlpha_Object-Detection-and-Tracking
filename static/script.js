
const confidence = document.getElementById("confidence");
const confidenceValue = document.getElementById("confidenceValue");

const trackerButtons = document.querySelectorAll("[data-tracker]");
const trailsToggle = document.getElementById("trails");
const resetBtn = document.getElementById("resetBtn");

let selectedTracker = "bytetrack.yaml";

async function updateSettings(data) {
    try {
        await fetch("/settings", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });
    } catch (error) {
        console.error("Settings update failed:", error);
    }
}

confidence.addEventListener("input", () => {
    confidenceValue.textContent = confidence.value + "%";
});

confidence.addEventListener("change", () => {
    updateSettings({
        confidence: Number(confidence.value) / 100
    });
});

trackerButtons.forEach(button => {
    button.addEventListener("click", () => {
        trackerButtons.forEach(btn => btn.classList.remove("selected"));
        button.classList.add("selected");

        selectedTracker = button.dataset.tracker;

        document.getElementById("trackerLabel").textContent =
            selectedTracker === "bytetrack.yaml" ? "ByteTrack" : "BoT-SORT";

        updateSettings({ tracker: selectedTracker });
    });
});

trailsToggle.addEventListener("change", () => {
    updateSettings({ trails: trailsToggle.checked });
});

resetBtn.addEventListener("click", async () => {
    await fetch("/reset", { method: "POST" });
});

async function refreshStats() {
    try {
        const response = await fetch("/stats");
        const data = await response.json();

        document.getElementById("objects").textContent = data.objects;
        document.getElementById("tracks").textContent = data.unique_tracks;
        document.getElementById("fps").textContent = data.fps;
        document.getElementById("status").textContent = data.status;

        const classContainer = document.getElementById("classes");
        classContainer.innerHTML = "";

        const classes = Object.entries(data.classes || {});

        if (classes.length === 0) {
            classContainer.innerHTML =
                '<span class="class-chip">No objects detected</span>';
        } else {
            classes.forEach(([name, count]) => {
                const chip = document.createElement("span");
                chip.className = "class-chip";
                chip.textContent = `${name} (${count})`;
                classContainer.appendChild(chip);
            });
        }

    } catch (error) {
        document.getElementById("status").textContent = "CONNECTION ERROR";
    }
}

setInterval(refreshStats, 1000);
refreshStats();
