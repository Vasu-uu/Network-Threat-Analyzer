from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import joblib
from utils.feature_extraction import extract_features_from_df
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model = joblib.load('model/rf_model.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(file)
        features, meta = extract_features_from_df(df)
        predictions = model.predict(features)
        meta['Prediction'] = ['Malicious' if p != 0 else 'Safe' for p in predictions]
        return jsonify({'success': True, 'data': meta.to_dict(orient='records')})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        records = data.get('records', [])
        if not records:
            return jsonify({'error': 'No data provided'}), 400

        df = pd.DataFrame(records)
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name='predicted_results.csv'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
