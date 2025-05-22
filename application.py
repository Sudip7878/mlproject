from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

@app.route('/')
def home():
    # Just render form with no prediction initially
    return render_template('home.html', results=None)

@app.route('/predictdata', methods=['POST'])
def predict_datapoint():
    try:
        # Collect form data
        gender = request.form.get('gender')
        race_ethnicity = request.form.get('ethnicity')
        parental_level_of_education = request.form.get('parental_level_of_education')
        lunch = request.form.get('lunch')
        test_preparation_course = request.form.get('test_preparation_course')
        reading_score = float(request.form.get('reading_score'))
        writing_score = float(request.form.get('writing_score'))

        # Create CustomData object
        data = CustomData(
            gender=gender,
            race_ethnicity=race_ethnicity,
            parental_level_of_education=parental_level_of_education,
            lunch=lunch,
            test_preparation_course=test_preparation_course,
            reading_score=reading_score,
            writing_score=writing_score
        )

        pred_df = data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)

        # results is usually a list or numpy array; take first value for display
        prediction = results[0]

        # Render template with prediction result
        return render_template('home.html', results=prediction)

    except Exception as e:
        # Handle error gracefully, you can log e or display error
        return f"Error occurred: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
