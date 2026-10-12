import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

DATA_PATH = os.path.join("data", "phishing_url_dataset.csv")
MODEL_PATH = "phishing_model.joblib"

def main():
    if not os.path.exists(DATA_PATH):
        print("Dataset not found.")
        print("Download phishing_url_dataset.csv from:")
        print("https://github.com/RajaMuhammadAwais/phishing-url-dataset")
        print("Create a folder named 'data' and put the CSV inside it.")
        return

    df = pd.read_csv(DATA_PATH)
    df.columns = [str(c).strip() for c in df.columns]

    if not {"URL", "Label"}.issubset(df.columns):
        raise ValueError(
            "Expected columns named URL and Label. "
            f"Columns found: {list(df.columns)}"
        )

    df = df[["URL", "Label"]].dropna().drop_duplicates(subset=["URL"])
    df["URL"] = df["URL"].astype(str).str.strip()
    df = df[df["URL"] != ""]

    # Dataset labels: 1 = legitimate, 0 = phishing.
    df["target"] = df["Label"].map({0: "Phishing", 1: "Legitimate"})
    df = df.dropna(subset=["target"])

    if df["target"].nunique() < 2:
        raise ValueError("Dataset must contain both phishing and legitimate examples.")

    X_train, X_test, y_train, y_test = train_test_split(
        df["URL"],
        df["target"],
        test_size=0.2,
        random_state=42,
        stratify=df["target"]
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(analyzer="char", ngram_range=(3, 5), min_df=2)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
    ])

    print(f"Training on {len(X_train):,} URLs...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("\nEvaluation on held-out test data")
    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("\nClassification report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("Confusion matrix (label order shown by sklearn):")
    print(confusion_matrix(y_test, predictions))

    joblib.dump(model, MODEL_PATH)
    print(f"\nSaved trained model to: {MODEL_PATH}")
    print("You can now run: python app.py")

if __name__ == "__main__":
    main()
