from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

LANGUAGES = [
    ("Auto Detect", "auto"), ("English", "en"), ("Telugu", "te"),
    ("Hindi", "hi"), ("Tamil", "ta"), ("Spanish", "es"),
    ("French", "fr"), ("German", "de"), ("Arabic", "ar"),
    ("Chinese (Simplified)", "zh"), ("Japanese", "ja"),
    ("Korean", "ko"), ("Russian", "ru"), ("Portuguese", "pt"),
    ("Italian", "it"), ("Dutch", "nl"), ("Turkish", "tr"),
    ("Bengali", "bn"), ("Gujarati", "gu"), ("Kannada", "kn"),
    ("Malayalam", "ml"), ("Marathi", "mr"), ("Punjabi", "pa"),
    ("Urdu", "ur"),
]

@app.route("/")
def home():
    return render_template("index.html", languages=LANGUAGES)

@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    text = data.get("text", "").strip()
    src  = data.get("src", "en")
    tgt  = data.get("tgt", "te")

    if not text:
        return jsonify({"error": "Text is empty!"}), 400

    if src == tgt and src != "auto":
        return jsonify({"error": "Source and target language are the same!"}), 400

    lang_pair = f"{'en' if src == 'auto' else src}|{tgt}"
    url = "https://api.mymemory.translated.net/get"
    params = {"q": text, "langpair": lang_pair}

    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        if result["responseStatus"] == 200:
            translated = result["responseData"]["translatedText"]
            return jsonify({"translation": translated})
        else:
            return jsonify({"error": "Translation failed"}), 500
    except requests.exceptions.Timeout:
        return jsonify({"error": "Server did not respond"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)