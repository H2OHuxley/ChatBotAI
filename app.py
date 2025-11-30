# app.py
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load .env variables
load_dotenv()

AIMLAPI_API_KEY = os.getenv("AIMLAPI_API_KEY")

if not AIMLAPI_API_KEY:
    raise RuntimeError("AIMLAPI_API_KEY is not set in .env!")

# Configure OpenAI-compatible client for AIMLAPI
client = OpenAI(
    api_key=AIMLAPI_API_KEY,
    base_url="https://router.requesty.ai/v1",
)

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = (data or {}).get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Message is empty."}), 400

    try:
        completion = client.chat.completions.create(
        model="openai/gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI chatbot for a school project.",
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            temperature=0.7,
            max_tokens=256,
        )

        reply_text = completion.choices[0].message.content.strip()
        return jsonify({"reply": reply_text})

    except Exception as e:
        print("Error calling AIMLAPI:", e)
        return jsonify({"error": "Failed to get response from AIMLAPI."}), 500


if __name__ == "__main__":
    app.run(debug=True)
