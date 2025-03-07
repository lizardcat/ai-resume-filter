from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import pickle  # Save model for reuse

# Simulated training dataset (past resumes and hiring decisions)
training_resumes = [
    "Experienced Python developer with Django and REST APIs",
    "Entry-level data analyst, proficient in Excel and SQL",
    "Cloud engineer with AWS and Terraform",
    "Frontend developer skilled in React and JavaScript"
]
labels = [1, 0, 1, 0]  # 1 = Hired, 0 = Rejected

# Convert resumes into numerical vectors
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(training_resumes)

# Train an AI model (Random Forest)
model = RandomForestClassifier()
model.fit(X_train, labels)

# Save model & vectorizer
with open("resume_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
