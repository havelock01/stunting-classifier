import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def train_models(df, feature_cols, label_col="label_efektivitas"):
    X = df[feature_cols]
    y = df[label_col]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)

    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(X_train, y_train)

    return dt_model, rf_model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred, labels=["Efektif", "Kurang Efektif", "Tidak Efektif"])
    return report, cm

def plot_confusion_matrix(cm, model_name):
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu",
                xticklabels=["Efektif", "Kurang Efektif", "Tidak Efektif"],
                yticklabels=["Efektif", "Kurang Efektif", "Tidak Efektif"])
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Prediksi")
    plt.ylabel("Aktual")
    plt.tight_layout()
    return plt

def plot_feature_importance(model, feature_cols):
    importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    plt.figure(figsize=(7, 5))
    sns.barplot(x=importances, y=importances.index, palette="viridis")
    plt.title("Feature Importance (Random Forest)")
    plt.xlabel("Kepentingan")
    plt.tight_layout()
    return plt

def plot_decision_tree(model, feature_cols, class_names):
    plt.figure(figsize=(20, 8))
    plot_tree(model, feature_names=feature_cols, class_names=class_names,
              filled=True, rounded=True, fontsize=10)
    plt.title("Visualisasi Decision Tree")
    plt.tight_layout()
    return plt
