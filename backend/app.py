# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
sales_revenue_forecaster_api = Flask("SuperKart Sales Revenue Forecaster")

# Load the trained machine learning model
model = joblib.load("sales_revenue_forecasting_model.joblib")

# Define a route for the home page (GET request)
@sales_revenue_forecaster_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Revenue Forecaster API!"

# Define an endpoint for single property prediction (POST request)
@sales_revenue_forecaster_api.post('/v1/sales')
def forecast_sales_revenue():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing product details and returns
    the predicted sales revenue as a JSON response.
    """
    # Get the JSON data from the request body
    product_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'weight': product_data['product_weight'],
        'sugar': product_data['product_sugar_content, ['low_sugar', 'regular, 'no_sugar']],
        'product_mrp': product_data['product_mrp'],
        'store_size': product_data['store_size'],
        'store_location_city_type': product_data['store_location_city_type, ['tier_1', 'tier_2', 'tier_3]],
        'store_type': product_data['store_type',['departmental_store', 'supermarket_type_1', 'supermarket_type_2', 'food_mart']],
        'pid_char': product_data['product_id_char (e.g., fd)', ['fd', 'nc', 'dr']],
        'age': product_data['store_age_years'],
        'cat': product_data['product_type_category', ['perishables', 'non_perishables']]
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make forecast (get log_sales_revenue)
    forecasted_log_sales_revenue = model.predict(input_data)[0]

    # Calculate actual sales revenue
    forecasted_sales_revenue = np.exp(forecasted_log_sales_revenue)

    # Convert predicted_sales_revenue to Python float
    forecasted_sales_revenue = round(float(forecasted_sales_revenue), 2)
    # The conversion above is needed as we convert the model prediction (log sales revenue) to actual sales revenue using np.exp, which returns predictions as NumPy float32 values.
    # When we send this value directly within a JSON response, Flask's jsonify function encounters a datatype error

    # Return the actual sales revenue
    return jsonify({'Forecasted Sales Revenue (in dollars)': predicted_sales_revenue})


# Define an endpoint for batch prediction (POST request)
@sales_revenue_forecaster_api.post('/v1/salesbatch')
def forecast_sales_revenue():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV file containing property details for multiple properties
    and returns the predicted rental prices as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all products in the DataFrame (get log_prices)
    forecasted_log_sales = model.forecast(input_data).tolist()

    # Calculate actual sales
    forecasted_sales = [round(float(np.exp(log_sales)), 2) for log_sales in forecasted_log_sales]

    # Create a dictionary of forecasts with product IDs as keys
    product_ids = input_data['id'].tolist()  # Assuming 'id' is the product ID column
    output_dict = dict(zip(product_ids, forecasted_sales))  # Use actual prices

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if _name_ == '_main_':
    sales_revenue_forecaster_api.run(debug=True)

# Load the serialized machine learning model
model = joblib.load('backend_files/superkart_model.joblib')

@app.route('/v1/predict', methods=['POST'])
def predict():
    data = request.get_json()
    df = pd.DataFrame([data])
    prediction = model.predict(df)[0]
    return jsonify({'prediction': float(prediction)})

@app.route('/v1/predictbatch', methods=['POST'])
def predict_batch():
    file = request.files['file']
    df = pd.read_csv(file)
    predictions = model.predict(df)
    return jsonify({str(i): float(pred) for i, pred in enumerate(predictions)})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
