# Signature Verification System — React + Flask + TensorFlow

This project adds a React frontend to your existing signature verification model.

## Architecture

React frontend
    |
    | POST /predict (multipart/form-data)
    v
Flask backend
    |
    | OpenCV grayscale + resize 128x128
    v
TensorFlow/Keras model
    |
    v
Genuine / Forged + confidence

## 1. Put your model in the backend

Copy your existing:

signature_model.keras

to:

backend/model/signature_model.keras

Your supplied Flask code already uses this model and preprocesses images as grayscale 128x128. The new backend keeps that behavior.

## 2. Start the Flask backend

Open a terminal:

    cd backend

Create/activate a virtual environment if desired, then:

    pip install -r requirements.txt

Start:

    python app.py

Backend:
http://127.0.0.1:5000

Test:
http://127.0.0.1:5000/health

You should see:

    {"model_loaded": true, "status": "ok"}

## 3. Start the React frontend

Open a second terminal:

    cd frontend
    npm install
    npm run dev

Vite will show a local URL, normally:

http://localhost:5173

Open that URL in your browser.

## 4. Optional API URL

If Flask runs somewhere else, create:

frontend/.env

with:

    VITE_API_URL=http://YOUR_HOST:5000

Then restart Vite.

## Important model/class mapping

Your training code uses `flow_from_directory()` with folders named `forged` and `genuine`. Keras normally assigns class indices alphabetically:

    forged  -> 0
    genuine -> 1

The backend therefore uses:

    CLASS_NAMES = ["forged", "genuine"]

This should be verified against the `Class Indices` printed by your training script if your dataset folder names differ.

## Notes about the supplied files

- `app.py` is the Flask server and uses `signature_model.keras`.
- `train.py` contains two training sections; the later section trains the CNN model and saves `signature_model.keras`.
- `test.py` currently loads a different LSTM model (`lstm_signature_model.h5`) and has a different class order. It is not used by this React application.
- `utils.py` is a separate console pattern-printing script and is not part of signature verification.

## Production improvements

Before deployment, add authentication if required, stronger file validation, unique upload filenames, HTTPS, rate limiting, and remove Flask debug mode.









# Signature Verification System

Final-year-project version containing:

- User registration
- User login
- JWT authentication
- Role-based administration
- Signature verification
- TensorFlow model integration
- SQLite database
- Verification history
- Analytics dashboard
- Confidence statistics
- Genuine/Forged statistics
- PDF verification reports
- Admin dashboard
- User management
- Verification monitoring

## Backend

```bash
cd backend

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python app.py