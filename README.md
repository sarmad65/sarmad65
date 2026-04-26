CardioSense AI ❤️

CardioSense AI is a machine-learning powered clinical decision support web application designed for heart disease risk assessment. It leverages the Cleveland Heart Disease Dataset and an XGBoost Classifier to predict the probability of cardiovascular issues based on 13 clinical parameters.

🌟 Features
AI-Powered Predictions**: Uses a trained XGBoost model to classify patient risk (Low Risk vs. Elevated Risk).
Interactive Patient Profile**: A user-friendly sidebar to input patient demographics, clinical findings, and test results.
Dynamic Risk Assessment**: Displays the calculated probability of heart disease alongside visual indicators and a threshold analysis.
Feature Importance**: Visualizes the impact of each clinical parameter on the model's prediction using matplotlib.
Modern UI/UX**: Built with a sleek, responsive design featuring Dark/Light mode toggles, micro-animations, and a responsive layout using Streamlit.



 🛠️ Tech Stack
Frontend / UI**: [Streamlit](https://streamlit.io/)
Machine Learning**: [XGBoost](https://xgboost.readthedocs.io/), [scikit-learn](https://scikit-learn.org/)
Data Manipulation**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
Data Visualization**: [Matplotlib](https://matplotlib.org/)

 🩺 Clinical Features Used
The model evaluates the following 13 clinical features:
1. Age
2. Sex
3. Chest Pain Type
4. Resting Blood Pressure
5. Serum Cholesterol
6. Fasting Blood Sugar
7. Resting ECG Results
8. Maximum Heart Rate Achieved
9. Exercise Induced Angina
10. ST Depression (Oldpeak)
11. Slope of the Peak ST Segment
12. Number of Major Vessels Colored by Fluoroscopy
13. Thalassemia

 💻 How to Run Locally

If you want to test or modify this project on your own machine, follow these steps:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/cardiosense-ai.git
   cd cardiosense-ai
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```
⚠️ Medical Disclaimer
This tool is for **educational and research purposes only**. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified cardiologist.
