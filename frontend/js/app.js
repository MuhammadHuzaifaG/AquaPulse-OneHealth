document.addEventListener("DOMContentLoaded", () => {
    
    // Sync slider values to text for Track 1 UX
    const bindSlider = (id, valId) => {
        const el = document.getElementById(id);
        const valEl = document.getElementById(valId);
        el.addEventListener("input", (e) => { valEl.textContent = e.target.value; });
    };
    bindSlider("water_clarity", "clarity-val");
    bindSlider("vegetation_cover", "veg-val");

    loadLeaderboard();

    document.getElementById("assessment-form").addEventListener("submit", async (e) => {
        e.preventDefault();
        
        const btn = document.getElementById("submit-btn");
        const loading = document.getElementById("loading");
        btn.disabled = true;
        loading.classList.remove("hidden");

        let imageBase64 = null;
        const fileInput = document.getElementById("image-upload");
        if (fileInput.files.length > 0) {
            imageBase64 = await toBase64(fileInput.files[0]);
        }

        const payload = {
            citizen_username: document.getElementById("username").value,
            stream_name: document.getElementById("stream_name").value,
            latitude: 40.2033, // Default hardcoded for hackathon demo
            longitude: -8.4103,
            water_clarity: parseInt(document.getElementById("water_clarity").value),
            water_flow: 3, // Defaults for form brevity
            odor_level: 3,
            garbage_presence: 3,
            vegetation_cover: parseInt(document.getElementById("vegetation_cover").value),
            mosquito_larvae_count: 0,
            image_base64: imageBase64
        };

        try {
            const res = await fetch("/api/v1/assessments", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            displayResults(data);
            loadLeaderboard(); // Refresh leaderboard
            updateHeader(data.points_earned, data.badge_unlocked);

        } catch (err) {
            alert("Error submitting assessment.");
            console.error(err);
        } finally {
            btn.disabled = false;
            loading.classList.add("hidden");
        }
    });
});

function displayResults(data) {
    document.getElementById("results-section").classList.remove("hidden");
    document.getElementById("res-wqi").textContent = `${data.water_quality_index}/100`;
    document.getElementById("res-risk").textContent = `${data.vector_risk_score}/100`;
    document.getElementById("res-story").textContent = data.ai_story;
    
    const actionList = document.getElementById("res-actions");
    actionList.innerHTML = "";
    data.recommended_actions.forEach(action => {
        const li = document.createElement("li");
        li.textContent = action;
        actionList.appendChild(li);
    });
}

function updateHeader(points, badge) {
    const ptsEl = document.getElementById("user-points");
    const currentPts = parseInt(ptsEl.textContent) || 0;
    ptsEl.textContent = `${currentPts + points} pts`;
    if(badge) document.getElementById("user-badge").textContent = badge;
}

async function loadLeaderboard() {
    try {
        const res = await fetch("/api/v1/leaderboard");
        const data = await res.json();
        const list = document.getElementById("leaderboard");
        list.innerHTML = "";
        data.forEach(user => {
            list.innerHTML += `<li>
                <span><strong>${user.username}</strong> (${user.badge})</span>
                <span>${user.points} pts</span>
            </li>`;
        });
    } catch (err) {
        console.error("Failed to load leaderboard", err);
    }
}

const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = error => reject(error);
});