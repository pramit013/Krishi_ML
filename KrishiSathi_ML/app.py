from flask import Flask, request, jsonify
import joblib
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from intent_classifier import classifier

load_dotenv()

app = Flask(__name__)

# =========================
# LOAD ML MODEL
# =========================

try:
    model = joblib.load("crop_model.pkl")
    print("✅ Crop model loaded successfully!")
except:
    model = None
    print("❌ Crop model not found")

# =========================
# API KEYS
# ─────────────────────────
# HOW TO SET YOUR KEYS:
#   1. In your project folder, create a file called   .env
#   2. Open it with Notepad and write exactly:
#
#        OPENWEATHER_API_KEY=b4fbfd9f53ab7aa8dd75f4de17869f84
#        GEMINI_API_KEY=AIzaSyA6O-Pi8VUJ0oXvcsOoNhBPUTW5_Htqvck
#
#   3. Save the file. That's it!
#   4. Never share or upload the .env file to GitHub.
#
# Get OpenWeather key : https://home.openweathermap.org/api_keys
# Get Gemini key      : https://aistudio.google.com/app/apikey
# =========================

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY")

# Quick startup check so you know immediately if keys are missing
if not OPENWEATHER_API_KEY:
    print("⚠️  WARNING: OPENWEATHER_API_KEY not found in .env")
if not GEMINI_API_KEY:
    print("⚠️  WARNING: GEMINI_API_KEY not found in .env")

# =========================
# WEATHER FUNCTION
# =========================

def get_weather(lat, lon):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric"
        )
        response = requests.get(url, timeout=10)
        data = response.json()

        if "main" not in data:
            print("Weather API error:", data)
            return None, None, None

        temperature = data["main"]["temp"]
        humidity    = data["main"]["humidity"]
        rainfall    = 0

        if "rain" in data:
            rainfall = data["rain"].get("1h", 0)

        return temperature, humidity, rainfall

    except Exception as e:
        print("Weather error:", e)
        return None, None, None

# =========================
# WEATHER RISK
# =========================

def analyze_weather_risk(temp, humidity, rainfall):
    alerts = []

    if temp is None:
        return ["WEATHER_DATA_UNAVAILABLE"]

    if rainfall > 5:
        alerts.append("HIGH_RAIN_RISK")

    if temp > 38:
        alerts.append("HEAT_STRESS_RISK")

    if rainfall > 1:
        alerts.append("SPRAY_UNSAFE")

    if rainfall < 0.5 and temp > 30:
        alerts.append("IRRIGATION_REQUIRED")

    return alerts

# =========================
# LOCATION VALIDATION
# =========================

def validate_coordinates(lat, lon):
    try:
        lat = float(lat)
        lon = float(lon)
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return True, lat, lon
        return False, None, None
    except:
        return False, None, None

# =========================
# GEMINI FUNCTION
# =========================

def ask_gemini(prompt):
    try:
        if not GEMINI_API_KEY:
            print("❌ Gemini API key missing")
            return None

        url = (
            "https://generativelanguage.googleapis.com"
            "/v1beta/models/gemini-2.0-flash:generateContent"
        )

        # ✅ CORRECT: using the variable GEMINI_API_KEY, not the raw key value
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }

        body = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=body,
            timeout=30
        )

        result = response.json()

        print("Gemini raw response:", result)

        if "candidates" in result:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return text

        if "error" in result:
            print("❌ Gemini API error:", result["error"])
            return None

        return None

    except Exception as e:
        print("Gemini exception:", e)
        return None

# =========================
# SAFE FALLBACK MESSAGES
# =========================

FALLBACK_MESSAGES = {
    "bn": "এই মুহূর্তে উত্তর দেওয়া সম্ভব হচ্ছে না। একটু পরে আবার চেষ্টা করুন।",
    "hi": "अभी उत्तर देना संभव नहीं है। कृपया थोड़ी देर बाद प्रयास करें।",
    "en": "Unable to get a response right now. Please try again shortly.",
}

OUT_OF_SCOPE_MESSAGES = {
    "bn": "কৃষি সাথী শুধুমাত্র কৃষি সম্পর্কিত প্রশ্নের উত্তর দেয়।",
    "hi": "कृषि साथी केवल खेती से जुड़े प्रश्नों का उत्तर देता है।",
    "en": "Krishi Sathi answers only farming and agriculture questions.",
}

def get_fallback(language):
    return FALLBACK_MESSAGES.get(language, FALLBACK_MESSAGES["en"])

def get_oos_message(language):
    return OUT_OF_SCOPE_MESSAGES.get(language, OUT_OF_SCOPE_MESSAGES["en"])

# =========================
# CROP PREDICTION API
# =========================

@app.route("/predict", methods=["POST"])
def predict_crop():
    try:
        if model is None:
            return jsonify({"error": "Crop model not loaded"}), 500

        data = request.get_json()

        valid, lat, lon = validate_coordinates(
            data.get("latitude"),
            data.get("longitude")
        )

        if not valid:
            return jsonify({"error": "Invalid location"}), 400

        temperature, humidity, rainfall = get_weather(lat, lon)
        alerts = analyze_weather_risk(temperature, humidity, rainfall)

        sample = pd.DataFrame(
            [[temperature, humidity, rainfall]],
            columns=["temperature", "humidity", "rainfall"]
        )

        probabilities  = model.predict_proba(sample)[0]
        crops          = model.classes_
        crop_prob_list = sorted(
            zip(crops, probabilities), key=lambda x: x[1], reverse=True
        )

        top3 = [
            {"name": crop, "confidence": round(prob * 100, 2)}
            for crop, prob in crop_prob_list[:3]
        ]

        return jsonify({
            "weather": {
                "temperature": temperature,
                "humidity":    humidity,
                "rainfall":    rainfall
            },
            "risk_alerts":       alerts,
            "recommended_crops": top3
        })

    except Exception as e:
        print(e)
        return jsonify({"error": "Prediction failed"}), 500

# =========================
# CHATBOT AGENT
# =========================

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data  = request.get_json()
        query = data.get("query", "").strip()
        lat   = data.get("latitude")
        lon   = data.get("longitude")

        # ── Step 1: classify intent ──
        clf_result = classifier.classify(query)
        intent     = clf_result["intent"]
        language   = clf_result["language"]

        print(f"Intent: {intent} | Language: {language} | Query: {query}")

        # ── Step 2: reject out-of-scope immediately ──
        if intent == "OUT_OF_SCOPE":
            return jsonify({
                "response": get_oos_message(language),
                "intent":   intent,
                "language": language
            })

        # ── Step 3: get weather if location provided ──
        valid, lat, lon = validate_coordinates(lat, lon)

        if valid:
            temperature, humidity, rainfall = get_weather(lat, lon)
            alerts = analyze_weather_risk(temperature, humidity, rainfall)

            if model is not None and temperature is not None:
                sample = pd.DataFrame(
                    [[temperature, humidity, rainfall]],
                    columns=["temperature", "humidity", "rainfall"]
                )
                probabilities  = model.predict_proba(sample)[0]
                crops          = model.classes_
                crop_prob_list = sorted(
                    zip(crops, probabilities), key=lambda x: x[1], reverse=True
                )
                top3 = [
                    crop_prob_list[0][0],
                    crop_prob_list[1][0],
                    crop_prob_list[2][0]
                ]
            else:
                top3 = []
        else:
            temperature = "unknown"
            humidity    = "unknown"
            rainfall    = "unknown"
            alerts      = []
            top3        = []

        # ── Step 4: build Gemini prompt (kept short to save token quota) ──
        prompt = f"""
You are Krishi Sathi, an agricultural assistant for farmers.
Weather: Temp={temperature}C, Humidity={humidity}%, Rainfall={rainfall}mm
Alerts: {alerts}
Top crops: {top3}
Farmer question: {query}

Rules:
- Reply in the SAME language as the farmer's question.
- Answer only farming, crop, irrigation, fertilizer, pesticide, harvest questions.
- Keep answer simple, short (3 to 5 lines), farmer-friendly.
- If SPRAY_UNSAFE or HIGH_RAIN_RISK in alerts, warn against spraying.
- If IRRIGATION_REQUIRED in alerts, suggest irrigation.
- Never guess pesticide dosage. Say: consult local agriculture office.
- If question is not about agriculture, reply exactly: OUT_OF_SCOPE
"""

        # ── Step 5: call Gemini ──
        answer = ask_gemini(prompt)

        print("Gemini answer:", answer)

        # ── Step 6: handle Gemini failure ──
        if not answer:
            return jsonify({
                "response": get_fallback(language),
                "intent":   intent,
                "language": language
            })

        # ── Step 7: if Gemini says OUT_OF_SCOPE, return polite message ──
        if "OUT_OF_SCOPE" in answer.upper():
            return jsonify({
                "response": get_oos_message(language),
                "intent":   "OUT_OF_SCOPE",
                "language": language
            })

        return jsonify({
            "response": answer,
            "intent":   intent,
            "language": language
        })

    except Exception as e:
        print("Chatbot error:", e)
        return jsonify({"error": "Chatbot failed"}), 500

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    print("🌾 Krishi Sathi Backend Running")
    print("✔  /predict")
    print("✔  /chatbot")
    app.run(debug=True, host="0.0.0.0", port=5000)