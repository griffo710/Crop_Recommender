# Crop Recommendation System API

## 📌 Description

The Crop Recommendation System is a machine learning--powered API that
helps farmers and agricultural stakeholders determine the most suitable
crop to plant based on soil and environmental conditions.

The system validates input data, provides warnings for abnormal
conditions, and returns intelligent crop recommendations.

## 🚀 Key Features

- Input validation (missing fields, wrong data types)
- Warning system (extreme soil or weather conditions)
- Machine learning--based crop prediction
- REST API support (JSON-based requests)
- CLI testing using curl
- Automated testing with pytest
- CI-ready structure for GitHub integration
- Optional UI for non-technical users (farmers)

## 🛠️ Technologies Used

- Python
- Flask
- Scikit-learn
- NumPy / Pandas
- Pytest
- GitHub Actions (optional)

## 📦 Installation Requirements

### Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

### Setup Instructions

```bash
git clone https://github.com/your-username/crop-recommender.git
cd crop-recommender

python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

## ▶️ Running the Application

```bash
python app.py
```

The API will run on: http://127.0.0.1:5000

## 📡 API Usage

### Endpoint

POST /api/recommend

### Example Request

```bash
curl -X POST http://127.0.0.1:5000/api/recommend \
-H "Content-Type: application/json" \
-d '{
  "N": 90,
  "P": 40,
  "K": 90,
  "temperature": 25,
  "humidity": 80,
  "ph": 6.5,
  "rainfall": 200
}'
```

### Example Response

```json
{
  "data": [
    {
      "Best crop": "jute",
      "confidence": 30.0
    },
    {
      "Second option": "rice",
      "confidence": 29.0
    },
    {
      "Third option": "papaya",
      "confidence": 17.0
    }
  ],
  "errors": [],
  "success": true,
  "warnings": []
}
```

## ⚙️ Configuration Options

- Modify validation rules in `services/validator.py`
- Adjust model or retrain in `models/`
- Update API logic in `app.py`

## 🧪 Running Tests

```bash
python -m pytest
```

### Test Coverage Includes:

- API success responses
- Missing input handling
- Warning generation
- Unexpected key detection
- Valid input validation

## 📂 Project Structure

    crop-recommender/
    ├── app.py
    ├── EDA.ipynb
    ├── forms.py
    ├── crop_recommendation.csv
    ├── services/
    │   └── validator.py
    |   └── predictor.py
    ├── static
    ├── templates
    ├── models/
    ├── tests/
    │   └── test_app.py
    ├── requirements.txt
    ├── README.md
    ├── .gitignore
    └── .github/workflows/

## ⚠️ Troubleshooting

### Common Issues

1.  Module not found → install requirements\
2.  API returns 500 → check logs and JSON format\
3.  Validation errors → ensure all fields are present\
4.  Warnings not showing → check validator return logic

## 🤝 Contributing

- Fork repository\
- Create branch\
- Add changes + tests\
- Submit PR

## 📜 License

MIT License
