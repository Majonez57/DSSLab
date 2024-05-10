import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.model_selection import KFold, GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
from joblib import dump, load
import seaborn as sns
import pickle

RSEED = 57
MODELN = '_mlp'

scaler = StandardScaler()
pca = PCA(n_components=0.98)

def preproc(split=0.3):

    datapath = 'constructedData/binPunches_window_5.csv'
    df = pd.read_csv(datapath)
    
    y = df['Punch']
    Xs = df.drop(['Punch'], axis=1)
    
    print("DATA SHAPE BEFORE PROCESSING: ", df.shape)

    smote = SMOTE()
    Xs, y = smote.fit_resample(Xs, y)

    # Train Test Split
    Xs_train, Xs_test, y_train, y_test = train_test_split(Xs, y, test_size=split, random_state=RSEED)

    # 0 mean normalization

    Xs_train = scaler.fit_transform(Xs_train)

    # PCA!
    Xs_train = pca.fit_transform(Xs_train)

    dump(pca,f'pkls/pca_tr{MODELN}.bin', compress=True)
    dump(scaler, f'pkls/stdscl_tr{MODELN}.bin', compress=True)

    print("AFTER PCA: ", Xs_train.shape)

    final_df = pd.DataFrame()
    for i in range(1, Xs_train.shape[1]+1):
        final_df[f'PCA_{i}'] = Xs_train[:,i-1]
    
    Xs_train = final_df
    Xs_test = pca.transform(scaler.transform(Xs_test))

    return (Xs_train, Xs_test, y_train, y_test)


Xs_train, Xs_test, y_train, y_test = preproc()

print(y_train)
print(y_train.value_counts())

mlp_model = MLPClassifier(random_state=RSEED, max_iter=1000)

# Parameter Grid
param_grid = {
    'hidden_layer_sizes': [(10, 4), (4, 6, 4), (4, 6), (4, 10)],
    'activation': ['relu', 'tanh'],
    'solver': ['adam'],
    'alpha': [0.0001, 0.001],
    'learning_rate_init': [0.001, 0.01],
}

# Cross validation!
kf = KFold(n_splits=8, shuffle=True, random_state=RSEED)

# Initialize GridSearchCV with K-Fold Cross-Validation
grid_search = GridSearchCV(mlp_model, param_grid, cv=kf, scoring='accuracy', n_jobs=-1, verbose=1)

grid_search.fit(Xs_train, y_train.values.ravel())

best_params = grid_search.best_params_

print(best_params)

best_lr_model = grid_search.best_estimator_

# Print mean cross-validated score of the best_estimator
print("Mean CV accuracy of the best model: {:.2f}".format(grid_search.best_score_))

# Predict on the test set using the best model
y_pred_new = best_lr_model.predict(Xs_test)

# Print classification report
print("\nClassification Report (Test Set):\n", classification_report(y_test.values.ravel(), y_pred_new))

filename =f'pkls/finalized_model{MODELN}.bin'

dump(best_lr_model, filename, compress=True)

# Plot the Confusion Matrix for the test set
cm_new = confusion_matrix(y_test, y_pred_new)
plt.figure(figsize=(10, 7))
sns.heatmap(cm_new, annot=True, fmt='g', cmap='Blues')
plt.title('Confusion Matrix for the Test Set')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.show()