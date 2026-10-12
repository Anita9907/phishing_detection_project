from flask import Flask, render_template, request
import os
import joblib

app = Flask(__name__)
MODEL_PATH = "phishing_model.joblib"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

def normalize_url(url):
    url = (url or "").strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    checked_url = ""
    error = None

    if request.method == "POST":
        checked_url = normalize_url(request.form.get("url", ""))

        if not checked_url:
            error = "Please enter a website URL."
        elif not model:
            error = "The ML model is missing. First run: python train_model.py"
        else:
            prediction = model.predict([checked_url])[0]
            if prediction == "Phishing":
                result = {
                    "label": "Possible phishing URL",
                    "kind": "danger",
                    "detail": "The model found patterns similar to phishing URLs. Do not enter passwords or payment details."
                }
            else:
                result = {
                    "label": "Likely legitimate URL",
                    "kind": "safe",
                    "detail": "The model classified this URL as likely legitimate, but this does NOT guarantee the site is safe."
                }

    return render_template("index.html", result=result, checked_url=checked_url, error=error)

if __name__ == "__main__":
    app.run(debug=True)
