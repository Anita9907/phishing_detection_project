# Phishing URL Detector (Python + Machine Learning)

This is an original educational project that trains a character-level TF-IDF + Logistic Regression model on labelled URL examples and provides a small Flask website.

## 1. Requirements
- Python 3.10 or newer
- Internet access to download the dataset and install Python packages
- VS Code or another editor (optional)

## 2. Create a virtual environment (recommended)

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install packages
```bash
pip install -r requirements.txt
```

## 4. Download the dataset
Open this public dataset repository:
https://github.com/RajaMuhammadAwais/phishing-url-dataset

Download `phishing_url_dataset.csv`. Create a folder called `data` inside this project and put the CSV in it, so the path is:
`data/phishing_url_dataset.csv`

The dataset page describes the columns as `URL` and `Label`, with 1 = legitimate and 0 = phishing. Check the file's columns and labels before training.

## 5. Train the model
```bash
python train_model.py
```
This splits the data into training and test sets, trains the model, prints evaluation metrics, and saves `phishing_model.joblib`.

## 6. Start the website
```bash
python app.py
```
Open the local address printed in the terminal, usually:
http://127.0.0.1:5000

## How it works
1. `TfidfVectorizer` converts URL character patterns into numerical features.
2. `LogisticRegression` learns patterns associated with the dataset labels.
3. The trained pipeline is saved with Joblib.
4. Flask accepts a URL and displays the model's classification.

## Important limitations
- It uses URL text only; it does not inspect the live page, certificates, redirects, or site reputation.
- Dataset quality and age affect results.
- Accuracy on the test split does not guarantee real-world accuracy.
- Never use the result as the only basis for trusting a website.
- Only test with URLs you are permitted to analyse; do not open suspicious URLs just to test them.

## Dataset credit
The project dataset is credited to the dataset authors and source repository:
https://github.com/RajaMuhammadAwais/phishing-url-dataset
Please review the dataset's own license and citation instructions before redistribution.
