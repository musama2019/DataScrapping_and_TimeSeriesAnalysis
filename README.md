**Time Series Forecasting of Sensor Values**

This project focuses on forecasting sensor values using time series data. Two types of sensors were simulated, and their values were generated and stored in ScyllaDB for approximately 40 minutes, with updates occurring every second. The data was then extracted from ScyllaDB using the copy_data_script.py file and saved as training.csv. Following this, the data underwent preprocessing and was used to train an LSTM model in time_series_forecasting.py. The trained model was utilized to generate data for the next two minutes, which was compared with the true data stored in testing.csv.

**Key Components:**

**Data Generation:** Simulated sensor values of two types were generated and stored in ScyllaDB for a duration of 40 minutes, with updates occurring every second.

**Data Extraction:** The copy_data_script.py file was used to extract data from ScyllaDB and save it as training.csv, preparing it for further processing and modeling.

**Preprocessing:** The data underwent preprocessing steps to clean and prepare it for training the LSTM model, ensuring optimal performance.

**Model Training:** The time_series_forecasting.py script trains an LSTM model using the preprocessed data to forecast sensor values for future time intervals.

**Model Evaluation**: The generated forecasts are compared with true data stored in testing.csv to evaluate the accuracy and effectiveness of the trained model.

**Usage:**

-Run copy_data_script.py to extract data from ScyllaDB and save it as training.csv.
-Execute time_series_forecasting.py to preprocess the data using appropriate techniques, ensuring it is suitable for training.
-Execute time_series_forecasting.py to train the LSTM model and generate forecasts for future time intervals.
-Compare the generated forecasts with the true data stored in testing.csv for evaluation purposes.
