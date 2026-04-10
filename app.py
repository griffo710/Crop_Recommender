from flask import Flask, render_template, flash, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.predictor import CropPredictor
from services.validator import InputValidator
from forms import CropPredictionForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'wendos~123'
limiter = (
    Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])
)

# Load the model
model = CropPredictor('crop_model.pkl')

# Validator instance
validator = InputValidator()


# Web route for form submission and prediction.
@app.route("/", methods=['POST', 'GET'])
@limiter.limit('2 per second', error_message='You have exceeded the limit of 2 predictions per second. Please try again later.')
def predict():
    """
    - This route handles both GET and POST requests for crop prediction.
    - On GET request, it renders the form for input. On POST request, it validates the input data,
    performs the prediction using the model, and returns the results along with any warnings.

    The process includes:
    1. Rendering the form for user input on GET request.
    2. Validating the input data on POST request using the InputValidator class.
    3. If validation fails, it flashes error messages and re-renders the form.
    4. If validation succeeds, it uses the CropPredictor model to predict the best crops based on the input data.
    5. It formats the prediction results and flashes any agricultural warnings before rendering the results on
        the same page.

    
    """
    form = CropPredictionForm()
    if form.validate_on_submit():
        clean_data = {
            "N": form.N.data,
            "P": form.P.data,
            "K": form.K.data,
            "temperature": form.temperature.data,
            "humidity": form.humidity.data,
            "ph": form.ph.data,
            "rainfall": form.rainfall.data
        }

        errors, warnings, clean_data = validator.validate(clean_data)
        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template('index.html', form=form)
        
        result = model.predict(clean_data)
        result_text = (
            f"Best Crop: {result[0][0]} ({result[0][1]*100:.2f}%)<br>"
            f"Second Option: {result[1][0]} ({result[1][1]*100:.2f}%)<br>"
            f"Third Option: {result[2][0]} ({result[2][1]*100:.2f}%)"
        )

        for warning in warnings:
            flash(warning, "warning")

        flash('Prediction successful!', 'success')
        return render_template('index.html', prediction_text=result_text, form=form)

    return render_template('index.html', form=form)



# API endpoint for external predictions.
@app.route("/api/recommend", methods=['POST'])
def recommend():
    """
    - This API endpoint handles POST requests for crop recommendation.
    - It expects a JSON payload containing the input features for prediction.
    The process includes:
    1. Receiving the JSON payload and extracting the input features.
    2. Validating the input data using the InputValidator class.
    3. If validation fails, it returns a JSON response with error messages and a 400 status code.
    4. If validation succeeds, it uses the CropPredictor model to predict the best crops based on the input data.
    5. It formats the prediction results and any agricultural warnings into a JSON response and 
       returns it with a 200 status code.

    """
    # Requesting the data.
    data = request.get_json()
    print("Received data:", data)  # Debugging statement to check incoming data

    if data is None:
        return jsonify({
        "success": False,
        "data": None,
        "errors": ["No data provided"],
        "warnings": []
    }), 400
    
   
    # Validating the data
    errors, warnings, clean_data = validator.validate(data)
    if errors:
        return jsonify({
        "success": False,
        "data": None,
        "errors": errors,
        "warnings": warnings
    }), 400

    

    print("Input data for prediction:", clean_data)  # Debugging statement

    predictions = model.predict(clean_data)
    prediction_results = [
        {"Best crop": predictions[0][0], "confidence": round(predictions[0][1] * 100, 2)},
        {"Second option": predictions[1][0], "confidence": round(predictions[1][1] * 100, 2)},
        {"Third option": predictions[2][0], "confidence": round(predictions[2][1] * 100, 2)}
    ]
    response = {
        "success": True,
        "data": prediction_results,
        "errors": [],
        "warnings": warnings
    }
        
    return jsonify(response), 200



if __name__ == '__main__':
    app.run(debug=True)