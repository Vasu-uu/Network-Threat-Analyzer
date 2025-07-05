import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from utils.feature_extraction import extract_features_from_df


DATA_PATH = "UNSW_NB15 Training.csv"  
MODEL_PATH = "model/rf_model.pkl"
CHUNK_SIZE = 100000
POSSIBLE_LABELS = ['label', 'Label', 'class', 'Class', 'attack_cat']

def find_label_column(columns):
    for col in POSSIBLE_LABELS:
        if col in columns:
            return col
    raise ValueError(f"Could not find any known label column in: {columns}")

features_list = []
labels_list = []

print("[INFO] Reading and extracting features from CSV...")


for i, chunk in enumerate(pd.read_csv(DATA_PATH, chunksize=CHUNK_SIZE, low_memory=False)):
    print(f"[INFO] Processing chunk {i+1}...")
    chunk.columns = chunk.columns.str.strip()
    
    try:
        label_col = find_label_column(chunk.columns)
    except ValueError as e:
        print(f"[SKIPPED] Chunk {i+1}: {e}")
        continue

    try:
        X_chunk, _ = extract_features_from_df(chunk)
        y_chunk = chunk[label_col].loc[X_chunk.index]

        
        y_chunk = y_chunk.apply(lambda x: 0 if str(x).lower() in ['normal', 'benign', '0'] else 1)

        features_list.append(X_chunk)
        labels_list.append(y_chunk)
    except Exception as e:
        print(f"[SKIPPED] Chunk {i+1}: {e}")
        continue


if not features_list:
    raise ValueError("No valid data chunks found.")

X = pd.concat(features_list, ignore_index=True)
y = pd.concat(labels_list, ignore_index=True)

print(f"[INFO] Training on {X.shape[0]} rows and {X.shape[1]} features.")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)


y_pred = clf.predict(X_test)

print("\n[INFO] Classification Report:")
print(classification_report(y_test, y_pred))

print("[INFO] Confusion Matrix:")
labels = sorted(y.unique())
cm = confusion_matrix(y_test, y_pred, labels=labels)

header = "Predicted →" + "".join([f"{label:>12}" for label in labels])
print(f"{'Actual ↓':<12}{header}")
for i, row in enumerate(cm):
    print(f"{labels[i]:<12}" + "".join([f"{val:>12}" for val in row]))

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
joblib.dump(clf, MODEL_PATH)
print(f"\n[INFO] Model saved to {MODEL_PATH}")
