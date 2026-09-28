# AquaPulse-OneHealth | Urban Freshwater 

> Urban Freshwater Telemetry & Vector Surveillance Platform

---

### Track 

* **Track 1: AI-Supported Assessment of Urban Aquatic Ecosystems**
AquaPulse OneHealth integrates multimodal artificial intelligence to evaluate stream health from citizen field notes, visual imagery, and physical-chemical measurements.
* **Track 2: Resilience Informatics for Public and Environmental Health**
The platform processes ecological indicators to quantify vector-borne disease risks and generate operational action plans for both municipal planners and local communities.

---

<img width="1313" height="618" alt="main" src="https://github.com/user-attachments/assets/20c7db35-c06f-4e5f-a915-37d8f59c9aaa" />

## Problem

Urban aquatic ecosystems suffer from fragmented data collection, non-point source pollution, and rapid vector-borne disease proliferation. Traditional laboratory sampling is costly, periodic, and slow to inform public health officials. Consequently, local governments lack actionable telemetry, while citizen scientists remain disconnected from municipal decision-making processes.

## Solution

AquaPulse OneHealth provides an end-to-end telemetry ingestion and diagnostic engine. It converts physical observations, bio-indicator counts (such as macroinvertebrates and mosquito larvae), chemical readings, and field photos into standardized health metrics.

Using a combined analytical approach—deterministic scoring models paired with multimodal LLM diagnostics—the platform produces immediate public health alerts, dual-tiered intervention strategies, and geospatial risk mapping.

### Target Users

* **Municipal Health & Environmental Officers:** Receive structured policy recommendations, pollution discharge warnings, and targeted intervention strategies.
* **Urban Planners & Hydrologists:** Monitor watershed integrity and spatial trends via live GIS mapping.
* **Citizen Scientists & Stream Stewards:** Submit field telemetry, verify site conditions using photo submissions, and track community engagement via points and leaderboards.

### Impact

* **Accelerated Hazard Detection:** Reduces the delay between field observations and municipal alerts from weeks to seconds.
* **Dual-Action Guidance:** Automatically generates distinct, actionable steps for city authorities (e.g., stormwater channel inspections) and citizens (e.g., removing standing water).
* **Data Standardization:** Aligns raw telemetry with One Health principles and FHIR-compatible data models for interoperability with broader public health software.

---

## Alignment with Evaluation Criteria

### 1. How Your Solution Aligns with OneAquaHealth
AquaPulse-OneHealth directly operationalizes the **OneAquaHealth** framework by linking urban aquatic ecosystem health with human public health and environmental resilience:
* **Holistic Interconnection:** It connects physical/chemical water quality (turbidity, pH) and ecological bio-indicators (macroinvertebrate populations) to vector disease risks (mosquito breeding) and human well-being metrics.
* **Dual-Tiered Actionability:** Translates complex ecological telemetry into immediate, complementary operational plans—policy-level interventions for municipal authorities and community-level mitigation steps for citizens.
* **Standards-Based Interoperability:** Implements HL7 FHIR-aligned data schemas to ensure ecological and vector telemetry can directly feed into broader healthcare and municipal health systems.

### 2. Innovation and Practical Value
* **Hybrid Diagnostic Engine:** Blends deterministic environmental scoring (WQI, EII, Vector Risk) with generative multimodal AI to deliver fast, reproducible, and context-aware risk evaluations.
* **Closing the Citizen-to-Government Gap:** Replaces slow, weeks-long laboratory workflows with instant, photo-verified field assessments powered by citizen scientists.
* **Gamified Community Engagement:** Features a built-in incentive system with points and leaderboards to maintain long-term user participation and high-density spatial data collection.
* **Actionable Spatial Intelligence:** Interactive GIS mapping transforms raw data points into actionable hotspot visualizations for rapid emergency and municipal planning.

### 3. Effective Use of Data, Technology, AI, APIs, & Standards
* **Multimodal Visual AI (Google Gemini 2.5 Flash):** Analyzes user-submitted field photos in real time to verify self-reported turbidity, stream degradation, and discharge presence against field notes.
* **Vector Risk Predictive ML (Hugging Face Service):** Utilizes specialized machine learning microservices to infer vector-borne disease transmission potential from bio-indicator counts.
* **Robust Enterprise Stack (FastAPI & Pydantic v2):** Implements an asynchronous, highly scalable Python backend using Pydantic v2 for strict data validation and instant API responsiveness.
* **Geospatial & Interoperability Standards:** Leverages **Leaflet.js** and **OpenStreetMap APIs** for frontend GIS rendering, alongside **HL7 FHIR R4 schemas** for standardizing environmental health records.

---

## Key Results & Capabilities

* **Deterministic Index Computation:** Calculates Water Quality Index (WQI), Ecological Integrity Index (EII), Vector Disease Risk Score, and Human Wellbeing Impact.
* **Multimodal Image Verification:** Decodes field photographs via Gemini Vision to cross-verify reported turbidity, vegetation, and discharge source presence.
* **Geospatial GIS Tracking:** Maps telemetry collection points on an interactive layer to highlight disease risk hotspots and stream degradation zones.
* **Community Incentive System:** Tracks user submissions, awards points, and calculates steward ranks to maintain high engagement in citizen science programs.

---

## Tech Stack

* **Backend:** Python 3.12, FastAPI, Pydantic v2, Uvicorn
* **AI Engine:** Google GenAI (Gemini API)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (ES6+)
* **Geospatial Visualization:** Leaflet.js, OpenStreetMap API
* **Data Standards:** JSON, FHIR alignment

---

<img width="1257" height="640" alt="result" src="https://github.com/user-attachments/assets/0ec98ac9-0ff9-4297-a21c-61b429e75fbf" />

## Prerequisites

Ensure the following tools are installed on your environment before setup:

* **Python:** Version 3.10 or higher
* **Package Manager:** `pip`
* **API Access:** Active Google Gemini API key
* **Hugging Face API Key**

---

<img width="1306" height="402" alt="leader" src="https://github.com/user-attachments/assets/92110b54-ba9a-42de-9dde-7b6adce52d0f" />

## Local Setup Instructions

### 1. Clone the Repository

```bash
# then
cd aquapulse-onehealth

```

### 2. Configure Virtual Environment

On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate

```

On Windows (Command Prompt):

```cmd
python -m venv venv
venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Set Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

```

### 5. Run the Application

```bash
python main.py

```

Alternatively, run with Uvicorn directly:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

```

### 6. Access the Application

Open your browser and navigate to:

* **Web Platform:** `[http://127.0.0.1:8000](http://127.0.0.1:8000)`
* **API Documentation (Swagger UI):** `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)`

---

## Project Structure

```
aquapulse-onehealth/
│
├── .env                         # Environment variables
├── requirements.txt             # Upgraded dependencies
├── config.py                    # App and DB configuration
├── main.py                      # FastAPI application core
├── Dckerfile
├── docker-compose.yaml
│
├── database/                    # Real-world Persistence Layer
│   ├── __init__.py
│   ├── engine.py                # Database connection & sessions
│   └── models.py                # SQLAlchemy ORM Models (Users, Assessments)
│
├── schemas/                     # Data Validation (Pydantic)
│   ├── __init__.py
│   ├── fhir_schemas.py          # HL7 FHIR R4 standard models (Track 7)
│   └── assessment_schemas.py    # Request/Response schemas
│
├── services/                    # Business Logic & AI
│   ├── gemini_service.py        # Gemini 2.5 Flash Vision & UX 
│   ├── huggingface_service.py   # Vector risk predictions
│   └── onehealth_engine.py      # Ecological analytics
│
├── routes/                      # API Endpoints
│   ├── api_v1.py                # REST endpoints
│   └── fhir_router.py           # Healthcare interoperability
│
└── frontend/                    # Structured UI Assets
    ├── index.html               
    ├── css/styles.css           
    └── js/app.js
```
