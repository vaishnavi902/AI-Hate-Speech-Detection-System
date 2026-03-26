import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load data
data = pd.read_csv("data.csv")

X = data["text"]
y = data["label"]

# Convert text to numbers
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vec, y)

# Prediction function
def predict_text(text):
    text_vec = vectorizer.transform([text])
    result = model.predict(text_vec)[0]

    if result == 1:
        return "Hate Speech Detected"
    else:
        return "Not Hate Speech"