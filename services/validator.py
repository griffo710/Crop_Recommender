class InputValidator:
    """"
    This class is responsible for validating the input data for crop prediction. 
    It checks for the presence of required features, ensures they are of the correct type, 
    and validates that they fall within acceptable ranges. 
    Additionally, it provides agricultural warnings based on certain conditions of the input data.
    """

    def validate(self, features):

        """
        Validates the input features for crop prediction.
        Parameters:
            features (dict): A dictionary containing the input features for prediction.
        Returns:
            errors (list): A list of error messages if validation fails.
            warnings (list): A list of warning messages based on agricultural conditions.

        The validation process includes:
        1. Checking for the presence of all required features. If some are missing, an error message is generated to 
           avoid issues especialy when range validations are performed on missing data returing a 500 internal server error.
        2. Ensuring that all features can be converted to floats.   
        3. Validating that the features fall within specified ranges.
        4. Providing agricultural warnings based on certain conditions of the input data.
        """

        errors = []
        warnings = []
        clean_data = {}

        # Verifying that all columns are present and are numbers
        expected_keys = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        for key in expected_keys: # Checking keys.
            if key not in features:
                errors.append(f"{key} is required") # Missing key error message.

            else:

                try: # Type casting each key into a float and raising an error if it fails.
                    clean_data[key] = float(features[key]) # storing into cleaned data.

                except (ValueError, TypeError):
                    errors.append(f"{key} is supposed to be a valid number.")

        # Returning errors if there are any type or missing key issues before performing range checks.
        if errors:
            return errors, warnings, None

        for n_key in features.keys(): # checking for unexpected keys in the input data and raising an error if found.
            if n_key not in expected_keys:
                warnings.append(f"Unexpected key: {n_key} ignored in prediction.")

        
        # Value extraction for range checks  
        N = clean_data["N"]
        P = clean_data["P"]
        K = clean_data["K"]
        temperature = clean_data["temperature"]
        humidity = clean_data["humidity"]
        ph = clean_data["ph"]
        rainfall = clean_data["rainfall"]


        # Range checks
        if not (0 <= N <= 140):
            errors.append("Nitrogen must be between 0 and 140")

        if not (5 <= P <= 145):
            errors.append("Phosphorus must be between 5 and 145")

        if not (5 <= K <= 205):
            errors.append("Potassium must be between 5 and 205")

        if not (10 <= temperature <= 45):
            errors.append("Temperature must be between 10°C and 45°C")

        if not (20 <= humidity <= 100):
            errors.append("Humidity must be between 20% and 100%")

        if not (0 <= ph <= 14):
            errors.append("pH must be between 0 and 14")

        if not (20 <= rainfall <= 400):
            errors.append("Rainfall must be between 20mm and 400mm")

        # Agricultural warnings
        if ph < 4.5:
            warnings.append("Soil is extremely acidic. Most crops will struggle.")

        if ph > 8.5:
            warnings.append("Soil is highly alkaline. Crop growth may be limited.")

        if rainfall < 40:
            warnings.append("Rainfall is very low. Irrigation may be required.")

        if temperature > 38:
            warnings.append("Temperature is very high. Heat stress may affect crops.")

        return errors, warnings, clean_data
