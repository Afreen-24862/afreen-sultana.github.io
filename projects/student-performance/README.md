# Student Performance Prediction

Predicts whether a student will pass (final grade G3 ≥ 10/20) and flags at-risk students.

| Step | File | What it does |
|---|---|---|
| 1 | `load_data.py` | Load the UCI dataset, profile the target |
| 2 | `preprocess.py` | Target, binary + one-hot encoding, remove G3 (no leakage) |
| 3 | `eda.py` | Correlations, pass rate by failures and study time |
| 4 | `train.py` | Baseline, Logistic Regression, Decision Tree, Random Forest; 5-fold CV; with and without term grades |
| 5 | `evaluate.py` | Classification report, confusion matrix, feature importance |
| 6 | `predict.py` | Probability of passing + risk label for new students |

Data: [UCI Student Performance](https://archive.ics.uci.edu/dataset/320/student+performance) (Cortez & Silva, 2008), maths course, 395 students.
