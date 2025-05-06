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
    
    # Validasi data: Pastikan data tidak kosong dan tidak semua NaN
    if X.shape[0] == 0:
        raise ValueError("Data fitur kosong. Pastikan data sudah diproses dan tersedia.")
    
    # Filter NaN sebelum split
    mask = ~X.isna().any(axis=1) & ~y.isna()
    X = X[mask]
    y = y[mask]

    # Cek lagi setelah filter
    if len(X) == 0:
        raise ValueError("Data setelah pembersihan fitur kosong. Tidak dapat melatih model.")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Pelatihan model
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)

    rf_model = RandomForestClassifier(random_state=42)
    rf_model.fit(X_train, y_train)

    return dt_model, rf_model, X_test, y_test

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    
    # Fix for undefined metrics warning - specify zero_division parameter
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    
    # Get unique classes from y_test to ensure we're using the right labels
    unique_classes = sorted(y_test.unique())
    cm = confusion_matrix(y_test, y_pred, labels=unique_classes)
    
    return report, cm, unique_classes

def plot_confusion_matrix(cm, model_name, class_labels=None):
    if class_labels is None:
        class_labels = ["Efektif", "Kurang Efektif", "Tidak Efektif"]
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="YlGnBu",
                xticklabels=class_labels,
                yticklabels=class_labels)
    plt.title(f"Confusion Matrix - {model_name}")
    plt.xlabel("Prediksi")
    plt.ylabel("Aktual")
    plt.tight_layout()
    return plt

def plot_feature_importance(model, feature_cols):
    # Sort importances and limit to top 20 features if there are too many
    importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
    if len(importances) > 20:
        importances = importances.head(20)
    
    plt.figure(figsize=(10, 8))  # Increased figure size
    
    # Fix for deprecation warning - use hue parameter instead of palette directly
    ax = sns.barplot(x=importances.values, y=importances.index, hue=importances.index, 
                    dodge=False, legend=False)
    
    plt.title("Feature Importance (Random Forest)")
    plt.xlabel("Kepentingan")
    
    # Make sure tight_layout has enough space
    plt.subplots_adjust(left=0.3)  # Add more space on the left for feature names
    return plt

def plot_decision_tree(model, feature_cols, class_names):
    # Limit the max_depth to make the tree more readable
    plt.figure(figsize=(20, 10))
    
    # If the tree is too complex, limit its depth for visualization
    max_depth = min(model.tree_.max_depth, 5)
    
    plot_tree(model, max_depth=max_depth, feature_names=feature_cols, 
              class_names=class_names, filled=True, rounded=True, fontsize=10)
    
    plt.title("Visualisasi Decision Tree (dibatasi untuk keterbacaan)")
    plt.tight_layout()
    return plt