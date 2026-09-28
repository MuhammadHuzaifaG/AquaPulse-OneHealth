let mapInstance = null;

document.addEventListener("DOMContentLoaded", () => {
    // Live slider value synchronization
    const bindSlider = (id, valId) => {
        const el = document.getElementById(id);
        const valEl = document.getElementById(valId);
        if (el && valEl) {
            el.addEventListener("input", (e) => { valEl.textContent = e.target.value; });
        }
    };
    bindSlider("water_clarity", "clarity-val");
    bindSlider("water_flow", "flow-val");
    bindSlider("garbage_presence", "garbage-val");
    bindSlider("vegetation_cover", "veg-val");

    loadLeaderboard();

    // Form submission handler
    const form = document.getElementById("assessment-form");
    if (form) {
        form.addEventListener("submit", async (e) => {
            e.preventDefault();
            
            const btn = document.getElementById("submit-btn");
            const loading = document.getElementById("loading");
            btn.disabled = true;
            loading.classList.remove("hidden");
            document.getElementById("results-section").classList.add("hidden");

            let imageBase64 = null;
            const fileInput = document.getElementById("image-upload");
            if (fileInput.files && fileInput.files.length > 0) {
                imageBase64 = await toBase64(fileInput.files[0]);
            }

            const payload = {
                citizen_username: document.getElementById("username").value,
                stream_name: document.getElementById("stream_name").value,
                latitude: 40.2033,
                longitude: -8.4103,
                water_clarity: parseInt(document.getElementById("water_clarity").value),
                water_flow: parseInt(document.getElementById("water_flow").value),
                odor_type: document.getElementById("odor_type").value,
                garbage_presence: parseInt(document.getElementById("garbage_presence").value),
                vegetation_cover: parseInt(document.getElementById("vegetation_cover").value),
                ph_level: parseFloat(document.getElementById("ph_level").value),
                dissolved_oxygen_mg_l: parseFloat(document.getElementById("dissolved_oxygen").value),
                water_temp_celsius: 18.5,
                recent_rainfall_hours: 12,
                discharge_pipe_nearby: document.getElementById("discharge_pipe").checked,
                mayfly_nymph_count: 2,
                mosquito_larvae_count: parseInt(document.getElementById("mosquito_larvae").value),
                user_notes: "Field submission via AquaPulse UI",
                image_base64: imageBase64
            };

            try {
                const res = await fetch("/api/v1/assessments", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });
                
                if (!res.ok) throw new Error("Server error during assessment processing.");
                
                const data = await res.json();
                displayResults(data);
                loadLeaderboard();
                updateHeader(data.points_earned, data.badge_unlocked);

            } catch (err) {
                alert("Failed to submit assessment. Check console for details.");
                console.error(err);
            } finally {
                btn.disabled = false;
                loading.classList.add("hidden");
            }
        });
    }
});

// Tab Navigation Controller
function switchTab(tabId, btnElement) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.add('hidden'));
    document.querySelectorAll('.nav-pill').forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabId).classList.remove('hidden');
    btnElement.classList.add('active');

    // Initialize GIS map when switching to map tab
    if (tabId === 'map-tab' && !mapInstance) {
        setTimeout(initMap, 200);
    }
}

// Initialize Leaflet Map for Scale & Architecture Demonstration
function initMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    mapInstance = L.map('map').setView([40.2033, -8.4103], 13);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(mapInstance);

    // Sample telemetry marker
    L.marker([40.2033, -8.4103]).addTo(mapInstance)
        .bindPopup("<b>Mondego Tributary Sector 3</b><br>WQI: 82.4/100<br>Status: Monitored & Verified")
        .openPopup();
}

function displayResults(data) {
    const resultsSec = document.getElementById("results-section");
    resultsSec.classList.remove("hidden");

    document.getElementById("res-wqi").textContent = `${data.water_quality_index}/100`;
    document.getElementById("res-eii").textContent = `${data.ecological_integrity_index}/100`;
    document.getElementById("res-risk").textContent = `${data.vector_risk_score}/100`;
    document.getElementById("res-wellbeing").textContent = `${data.human_wellbeing_impact_score}/100`;
    
    document.getElementById("res-diagnostic").textContent = data.ai_diagnostic_report;

    const banner = document.getElementById("health-warning-banner");
    if (data.public_health_warning && data.public_health_warning !== "No immediate public health hazard detected.") {
        banner.classList.remove("hidden");
        document.getElementById("warning-text").textContent = data.public_health_warning;
    } else {
        banner.classList.add("hidden");
    }

    const municipalList = document.getElementById("res-municipal-actions");
    municipalList.innerHTML = "";
    data.municipal_action_plan.forEach(action => {
        municipalList.innerHTML += `<li>${action}</li>`;
    });

    const citizenList = document.getElementById("res-citizen-actions");
    citizenList.innerHTML = "";
    data.citizen_action_plan.forEach(action => {
        citizenList.innerHTML += `<li>${action}</li>`;
    });

    resultsSec.scrollIntoView({ behavior: 'smooth' });
}

function updateHeader(points, badge) {
    const ptsEl = document.getElementById("user-points");
    const currentPts = parseInt(ptsEl.textContent) || 0;
    ptsEl.textContent = `${currentPts + points} pts`;
    if (badge) document.getElementById("user-badge").textContent = badge;
}

async function loadLeaderboard() {
    try {
        const res = await fetch("/api/v1/leaderboard");
        const data = await res.json();
        const list = document.getElementById("leaderboard");
        if (!list) return;
        list.innerHTML = "";
        data.forEach(user => {
            list.innerHTML += `<li>
                <span><strong>${user.username}</strong> <span class="badge" style="font-size:0.75rem; margin-left:8px;">${user.badge}</span></span>
                <span style="font-weight:bold; color:var(--primary);">${user.points} pts</span>
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