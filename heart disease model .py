import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("heart_disease_new.csv")

df = df[df['dataset'] == 'Cleveland'].copy()
print(f"Total rows in Cleveland: {len(df)}")

df['target'] = (df['num'] > 0).astype(int)

features = ['age','sex','cp','trestbps','chol','fbs','restecg','thalch','exang','oldpeak','slope','ca','thal']
df = df[features + ['target']]

df['sex'] = df['sex'].map({'Male': 1, 'Female': 0})
df['fbs'] = df['fbs'].astype(bool).astype(int)
df['exang'] = df['exang'].astype(bool).astype(int)

df['cp'] = df['cp'].map({'typical angina': 0, 'atypical angina': 1, 'non-anginal': 2, 'asymptomatic': 3})
df['restecg'] = df['restecg'].map({'normal': 0, 'lv hypertrophy': 1, 'st-t abnormality': 2})
df['slope'] = df['slope'].map({'upsloping': 1, 'flat': 2, 'downsloping': 3})
df['thal'] = df['thal'].map({'normal': 3, 'fixed defect': 6, 'reversable defect': 7})

df.replace(['', '?'], np.nan, inplace=True)
imputer = SimpleImputer(strategy='median')
df[features] = imputer.fit_transform(df[features])

X = df[features].astype(float)
y = df['target']

model = XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.85,
    colsample_bytree=0.85,
    scale_pos_weight=1.1,
    random_state=42,
    eval_metric='aucpr'
)

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
print(f"10-FOLD CV Accuracy: {scores.mean()*100:.2f}% ± {scores.std()*100:.2f}%")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model.fit(X_train, y_train)

pred = model.predict(X_test)
print(f"\nTest Accuracy: {accuracy_score(y_test, pred)*100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, pred))

print("\n=== Threshold Tuning ===")
y_proba = model.predict_proba(X_test)[:, 1]

for thresh in [0.45, 0.50, 0.55, 0.60, 0.65, 0.70]:
    y_pred_thresh = (y_proba >= thresh).astype(int)
    print(f"\nThreshold = {thresh:.2f}")
    print(classification_report(y_test, y_pred_thresh))

importances = model.feature_importances_
feat_imp = pd.Series(importances, index=features).sort_values(ascending=False)

plt.figure(figsize=(10, 6))
feat_imp.plot(kind='bar')
plt.title('Feature Importance - XGBoost')
plt.ylabel('Importance Score')
plt.tight_layout()
plt.show()

joblib.dump(model, 'heart_model.pkl')
print("\nModel saved successfully as 'heart_model.pkl'")
joblib.dump(imputer, 'imputer.pkl')
print("Imputer saved as 'imputer.pkl'")