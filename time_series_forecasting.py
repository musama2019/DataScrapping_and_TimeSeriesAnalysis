# -*- coding: utf-8 -*-
"""Time_series_forecasting.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1p9fdJXMj18p2H4rSvN_rEpFXXoslRJH8
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV


data=pd.read_csv('/content/output2.csv')
df = pd.DataFrame(data)

# Pivot the DataFrame to create a new column for each unique sensor ID
df = df.pivot(index="ts", columns="sensor_id", values="value")
df.reset_index(inplace=True)
df = df.rename(columns={
    '04fcb5ca-2eb9-4d97-b142-6320264aa440': 'sensor_1',
    '83b4e224-54fd-4020-8167-c6132230bf9b': 'sensor_2'
})

df.set_index('ts', inplace=True)

# Display the pivoted DataFrame
df.head()

df = df.dropna()
df.tail()
df.shape

test_split=round(len(df)*0.20)
df_for_training=df[:-60]
df_for_testing=df[-60:]
print(df_for_training.shape)
print(df_for_testing.shape)
df_for_training.to_csv("training_data.csv", index=False)
df_for_testing.to_csv("testing_data.csv", index=False)

scaler = MinMaxScaler(feature_range=(0,1))
df_for_training[['sensor_1', 'sensor_2']] = scaler.fit_transform(df_for_training[['sensor_1', 'sensor_2']])
df_for_testing[['sensor_1', 'sensor_2']] = scaler.fit_transform(df_for_testing[['sensor_1', 'sensor_2']])
df_for_training

def createXY(dataset, n_past):
    dataX = []
    dataY = []
    for i in range(n_past, len(dataset)):
        dataX.append(dataset[i - n_past:i])  # Only access the rows
        dataY.append(dataset[i, 0])  # Access the first column
    return np.array(dataX), np.array(dataY)

# Example usage
trainX, trainY = createXY(df_for_training.values, 30)
testX, testY = createXY(df_for_testing.values, 30)

print("trainX Shape-- ",trainX.shape)
print("trainY Shape-- ",trainY.shape)

print("testX Shape-- ",testX.shape)
print("testY Shape-- ",testY.shape)

print("trainX[0]-- \n",trainX[0])
print("trainY[0]-- ",trainY[0])

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import numpy as np

# Define your custom Keras model
def build_model(optimizer):
    grid_model = Sequential()
    grid_model.add(LSTM(4,input_shape=(30,2)))
    grid_model.add(Dense(1))
    grid_model.compile(loss = 'mse',optimizer = 'adam')
    return grid_model


# Create the model
model = build_model('adam')

# Fit the model on your training data
model.fit(trainX, trainY, epochs=10, batch_size=16, verbose=1, validation_data=(testX, testY))

# Evaluate the model on your test data
loss = model.evaluate(testX, testY)
print(f"Test Loss: {loss}")

model.save('time_series_model.h5')

# Load the trained model
loaded_model = tf.keras.models.load_model('time_series_model.h5')

# Make predictions
predictions = model.predict(testX)

# Reshape and inverse transform the predictions
prediction_copies_array = np.repeat(predictions, 2, axis=-1)
pred = scaler.inverse_transform(np.reshape(prediction_copies_array, (len(predictions), 2)))

# Reshape and inverse transform the original values
original_copies_array = np.repeat(testY, 2, axis=-1)
original = scaler.inverse_transform(np.reshape(original_copies_array, (len(testY), 2)))

# Print the predicted and original values for both columns
print("Predicted Values:")
print(pred)

print("\nOriginal Values:")
print(original)

plt.figure(figsize=(12, 6))
# Assuming df_for_testing contains your testing data with 120 rows
# If you have 90 predictions, use the first 90 rows of the testing data for plotting
plt.plot(df_for_testing.index[:30], original[:, 0], label="Sensor 1 - Original", marker='o', markersize=3)
plt.plot(df_for_testing.index[:30], original[:, 1], label="Sensor 2 - Original", marker='o', markersize=3)
plt.plot(df_for_testing.index[:30], pred[:, 0], label="Sensor 1 - Predicted", linestyle='dashed')
plt.plot(df_for_testing.index[:30], pred[:, 1], label="Sensor 2 - Predicted", linestyle='dashed')
plt.xlabel("Timestamp")
plt.ylabel("Sensor Values")
plt.xticks(rotation=90)  # Rotate x-axis labels vertically
plt.legend()
plt.title("Original vs. Predicted Sensor Values")
plt.show()