# -*- coding: utf-8 -*-
"""CPC251_Project_Part2_Cancer5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12mSoqzlFY9r8lPTRx-oqLBOKbR5c6pz1
"""

# Commented out IPython magic to ensure Python compatibility.
# %config Completer.use_jedi=False # comment if not needed

#Import pandas library
import pandas as pd

#Import numpy library
import numpy as np

import sklearn
print(sklearn.__version__)

# Reading the dataset in a dataframe
df = pd.read_csv('/content/cancer_dataset.csv')
df

# Print unique values of the target columns of the dataset
for target in ['Hinselmann', 'Schiller', 'Citology', 'Biopsy']:
    print(f"Unique values in {target}: {df[target].unique()}")

# This is to determine whether this dataset is classification or regression problem

# Display the first 10 rows of the dataset
df.head(10)

# Display all the information of the dataset
df.describe()

# Display all the columns of the dataset
df1 = pd.DataFrame(df.columns)
df1.columns = ['features']
df1

# Check for non-numeric values
non_numeric_columns = df.columns[df.apply(lambda col: pd.to_numeric(col, errors='coerce').isna().any())]

print("Non-numeric columns:", non_numeric_columns)

columns_to_drop = ['STDs: Time since first diagnosis', 'STDs: Time since last diagnosis']

# Drop the specified columns
df.drop(columns=columns_to_drop, inplace=True)
df

# If you have '?' values, replace them with NaN first and then drop rows with NaN
df.replace('?', np.nan, inplace=True)
df

#Check the number of null in the dataset
df.apply(lambda x: sum(x.isnull()),axis=0)

# List of columns with missing boolean values
bool_columns = [
    'Smokes',
    'Hormonal Contraceptives',
    'IUD',
    'STDs',
    'STDs:condylomatosis',
    'STDs:cervical condylomatosis',
    'STDs:vaginal condylomatosis',
    'STDs:vulvo-perineal condylomatosis',
    'STDs:syphilis',
    'STDs:pelvic inflammatory disease',
    'STDs:genital herpes',
    'STDs:molluscum contagiosum',
    'STDs:AIDS',
    'STDs:HIV',
    'STDs:Hepatitis B',
    'STDs:HPV'
]


# Impute bool columns with mode
for column in bool_columns:
    mode_value = df[column].mode()[0]
    df[column].fillna(mode_value, inplace=True)

# Verify that there are no NaN values left in the boolean columns
print(df[bool_columns].isna().sum())

# List of columns with missing numeric values
numeric_columns = [
    'Number of sexual partners',
    'First sexual intercourse',
    'Num of pregnancies',
    'Smokes (years)',
    'STDs (number)',
    'Hormonal Contraceptives (years)',
    'IUD (years)',
    'Smokes (packs/year)',
]

# Convert columns to numeric (errors='coerce' converts non-numeric values to NaN)
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Impute numeric columns with mean
for column in numeric_columns:
    df[column].fillna(df[column].mean(), inplace=True)

# Verify that there are no NaN values left in the numeric columns
print(df[numeric_columns].isna().sum())

#Check the number of null in the dataset
df.apply(lambda x: sum(x.isnull()),axis=0)

"""#### Split the dataset
Split the dataset into training, validation and test sets.
"""

from sklearn.model_selection import train_test_split

# Split the dataset into features (X) and target variable (y)
X = df.drop(columns=['Biopsy', 'Hinselmann', 'Schiller', 'Citology'])
y = df[['Biopsy', 'Hinselmann', 'Schiller', 'Citology']]

# Split the dataset into training and test sets (80% training, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Split the training set into training and validation sets (70% training, 10% validation)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.125, random_state=42) # 10% of 80% = 8% of total data

# Display the sizes of the resulting sets
print("Training Set Size:", len(X_train))
print("Validation Set Size:", len(X_val))
print("Test Set Size:", len(X_test))

# Print the shape of each data

print("Shape of X_train: ", X_train.shape)
print("Shape of y_train: ", y_train.shape)
print("Shape of X_validation: ", X_val.shape)
print("Shape of y_validation: ", y_val.shape)
print("Shape of X_test: ", X_test.shape)
print("Shape of y_test: ", y_test.shape)

# Show the first 5 rows of X_train set

X_train.head(5)

# Show the first 5 rows of X_val set

X_val.head(5)

# Show the first 5 rows of X_test set

X_test.head(5)

"""#### Data preprocessing
Perform data preprocessing such as normalization, standardization, label encoding etc.
______________________________________________________________________________________
**Description:** We scaled the features to standardize the cleaned data using the StandardScaler from Scikit-learn. We fitted the scaler on the training data and transformed the training data to ensure that the model is trained on standardized features. We then used the same scaler (fitted on the training data) to transform the validation and test sets.
"""

from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform the training data
X_train_scaled = scaler.fit_transform(X_train)

# Transform the validation and test data using the scaler fitted on the training data
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# Display the sizes of the resulting sets (Optional)
print("Scaled Training Set Size:", X_train_scaled.shape)
print("Scaled Validation Set Size:", X_val_scaled.shape)
print("Scaled Test Set Size:", X_test_scaled.shape)

"""#### Data modeling
Build two (2) predictive models to predict the target variable of the dataset. One of the
predictive models must be either Neural Network or Fuzzy Logic System.

**(a) Fuzzy Logic System**
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

!pip install scikit-fuzzy

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Define input variables
age = ctrl.Antecedent(np.arange(0, 101, 1), 'age')
hpv = ctrl.Antecedent(np.arange(0, 2, 1), 'hpv')  # 0 for negative, 1 for positive

# Define output variables (your four targets)
hinselmann = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'hinselmann')
schiller = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'schiller')
citology = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'citology')
biopsy = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'biopsy')

# Age membership functions
age['young'] = fuzz.trimf(age.universe, [0, 0, 30])
age['middle'] = fuzz.trimf(age.universe, [25, 45, 65])
age['old'] = fuzz.trimf(age.universe, [60, 100, 100])

# HPV membership functions
hpv['negative'] = fuzz.trimf(hpv.universe, [0, 0, 0])
hpv['positive'] = fuzz.trimf(hpv.universe, [1, 1, 1])

# Output membership functions
for output in [hinselmann, schiller, citology, biopsy]:
    output['low'] = fuzz.trimf(output.universe, [0, 0, 0.5])
    output['medium'] = fuzz.trimf(output.universe, [0.25, 0.5, 0.75])
    output['high'] = fuzz.trimf(output.universe, [0.5, 1, 1])

# Visualize membership functions
age.view()
hpv.view()
hinselmann.view()
schiller.view()
citology.view()
biopsy.view()
plt.show()

# Define fuzzy rules
rule1 = ctrl.Rule(age['young'] & hpv['negative'],
                  (hinselmann['low'], schiller['low'], citology['low'], biopsy['low']))
rule2 = ctrl.Rule(age['young'] & hpv['positive'],
                  (hinselmann['medium'], schiller['medium'], citology['medium'], biopsy['medium']))
rule3 = ctrl.Rule(age['middle'] & hpv['negative'],
                  (hinselmann['low'], schiller['low'], citology['low'], biopsy['low']))
rule4 = ctrl.Rule(age['middle'] & hpv['positive'],
                  (hinselmann['high'], schiller['high'], citology['high'], biopsy['high']))
rule5 = ctrl.Rule(age['old'] & hpv['negative'],
                  (hinselmann['medium'], schiller['medium'], citology['medium'], biopsy['medium']))
rule6 = ctrl.Rule(age['old'] & hpv['positive'],
                  (hinselmann['high'], schiller['high'], citology['high'], biopsy['high']))

# Create control system
cancer_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
cancer_simulation = ctrl.ControlSystemSimulation(cancer_ctrl)

def test_system(age_val, hpv_val):
    cancer_simulation.input['age'] = age_val
    cancer_simulation.input['hpv'] = hpv_val

    cancer_simulation.compute()

    print(f"For Age: {age_val}, HPV: {'Positive' if hpv_val else 'Negative'}")
    print(f"Hinselmann: {cancer_simulation.output['hinselmann']:.2f}")
    print(f"Schiller: {cancer_simulation.output['schiller']:.2f}")
    print(f"Citology: {cancer_simulation.output['citology']:.2f}")
    print(f"Biopsy: {cancer_simulation.output['biopsy']:.2f}")
    print()

    # Visualize the results
    hinselmann.view(sim=cancer_simulation)
    schiller.view(sim=cancer_simulation)
    citology.view(sim=cancer_simulation)
    biopsy.view(sim=cancer_simulation)
    plt.show()

# Test cases
test_system(25, 0)  # Young age, HPV negative
test_system(25, 1)  # Young age, HPV positive
test_system(40, 0)  # Middle age, HPV negative
test_system(40, 1)  # Middle age, HPV positive
test_system(70, 0)  # Old age, HPV negative
test_system(70, 1)  # Old age, HPV positive

"""**(b) Neural Network**"""

# Define the model architecture
model = Sequential()

# Input layer and first hidden layer with 128 neurons and ReLU activation
model.add(Dense(128, input_dim=X_train.shape[1], activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Dropout layer to prevent overfitting

# Second hidden layer with 64 neurons and ReLU activation
model.add(Dense(64, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Dropout layer to prevent overfitting

# Third hidden layer with 32 neurons and ReLU activation
model.add(Dense(32, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Dropout layer to prevent overfitting

# Fourth hidden layer with 16 neurons and ReLU activation
model.add(Dense(16, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))  # Dropout layer to prevent overfitting

# Output layer with 4 neuron and sigmoid activation (for binary classification)
model.add(Dense(4, activation='sigmoid'))

# Compile the model with Adam optimizer and a learning rate scheduler
initial_learning_rate = 0.001
lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
    initial_learning_rate, decay_steps=10000, decay_rate=0.9, staircase=True
)
optimizer = tf.keras.optimizers.Adam(learning_rate=lr_schedule)

model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

# Print the model summary
model.summary()

# Train the model
history = model.fit(
    X_train_scaled, #Training features
    y_train, # Training labels
    epochs=100, #Number of epochs
    batch_size=32, # Batch size
    validation_data=(X_val_scaled, y_val), #Validation deatures and labels
)

from matplotlib import pyplot as plt

loss_train = history.history['loss']
loss_val = history.history['val_loss']

# Plot training and validation loss
plt.figure(figsize=(10, 6))
plt.plot(loss_train, label='Train Loss', color='blue')
plt.plot(loss_val, label='Validation Loss', color='orange')

# Adding labels and title
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

# Show plot
plt.grid(True)
plt.show()

from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Define early stopping and model checkpoint callbacks
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True,
    verbose = 1
)

model_checkpoint = ModelCheckpoint(
    'best_model.h5',
    monitor='val_loss',
    save_best_only=True,
    mode='min',
    verbose=1
)

# Train the model with callbacks
history = model.fit(
    X_train_scaled, y_train,
    epochs=100,
    batch_size=32,
    validation_data=(X_val_scaled, y_val),
    callbacks=[early_stopping, model_checkpoint]  # Include callbacks here
)

loss_train = history.history['loss']
loss_val = history.history['val_loss']

# Plot training and validation loss
plt.figure(figsize=(10, 6))
plt.plot(loss_train, label='Train Loss', color='blue')
plt.plot(loss_val, label='Validation Loss', color='orange')

# Adding labels and title
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()

# Show plot
plt.grid(True)
plt.show()

"""#### Evaluate the models
Perform a comparison between the predictive models. <br>
Report the accuracy, recall, precision and F1-score measures as well as the confusion matrix if it is a classification problem. <br>
Report the R2 score, mean squared error and mean absolute error if it is a regression problem.
"""

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

def fuzzy_to_binary(value):
    return 1 if value >= 0.5 else 0

def predict(age_val, hpv_val):
    cancer_simulation.input['age'] = age_val
    cancer_simulation.input['hpv'] = int(hpv_val)  # Convert bool to int (0 or 1)
    cancer_simulation.compute()
    return [
        fuzzy_to_binary(cancer_simulation.output['hinselmann']),
        fuzzy_to_binary(cancer_simulation.output['schiller']),
        fuzzy_to_binary(cancer_simulation.output['citology']),
        fuzzy_to_binary(cancer_simulation.output['biopsy'])
    ]

# Make predictions
y_pred = []
for _, row in X_test.iterrows():
    y_pred.append(predict(row['Age'], row['STDs:HPV']))

y_pred = np.array(y_pred)
y_true = y_test.values

# Generate reports for each target
targets = ['Hinselmann', 'Schiller', 'Citology', 'Biopsy']

for i, target in enumerate(targets):
    print(f"\nMetrics for {target}:")
    print(classification_report(y_true[:, i], y_pred[:, i]))
    print("Confusion Matrix:")
    print(confusion_matrix(y_true[:, i], y_pred[:, i]))
    print(f"Accuracy Score: {accuracy_score(y_true[:, i], y_pred[:, i])}")

from tensorflow.keras.models import load_model
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np
import pandas as pd

# Load the best model
best_model = load_model('best_model.h5')

# Ensure that X_test and y_test are numpy arrays of appropriate types
X_test = X_test.astype(np.float32)
y_test = y_test.astype(np.int32)

# Evaluate the model on test data
test_loss, test_accuracy = best_model.evaluate(X_test, y_test, verbose=1)
print(f"Test Loss: {test_loss}")
print(f"Test Accuracy: {test_accuracy}")

# Make predictions on the test set
y_pred_proba = best_model.predict(X_test)

# Convert predictions to binary values (0 or 1) based on a threshold of 0.5
y_pred_binary = (y_pred_proba > 0.5).astype(int)

# Ensure y_test is a DataFrame and check column names
if isinstance(y_test, pd.DataFrame):
    print("y_test columns:", y_test.columns)
else:
    raise ValueError("y_test is not a DataFrame")

# Generate classification reports and confusion matrices for each target
targets = ['Hinselmann', 'Schiller', 'Citology', 'Biopsy']

for i, target in enumerate(targets):
    if target in y_test.columns:
        print(f'\nClassification Report for {target}:')
        print(classification_report(y_test[target], y_pred_binary[:, i]))

        print(f'\nConfusion Matrix for {target}:')
        print(confusion_matrix(y_test[target], y_pred_binary[:, i]))
    else:
        print(f"Column {target} is not present in y_test")

# Calculate and print overall accuracy score
overall_accuracy = accuracy_score(
    np.concatenate([y_test[target].values.reshape(-1, 1) for target in targets], axis=1),
    np.concatenate([y_pred_binary[:, i].reshape(-1, 1) for i in range(len(targets))], axis=1)
)
print(f"\nOverall Accuracy Score: {overall_accuracy}")