import streamlit as st
import pandas as pd
from huggingface_hub import hf_hub_download
import joblib

# Download and load the model
model_path = hf_hub_download(repo_id="chinnsf/packageprediction", filename="best_model_v1.joblib")
model = joblib.load(model_path)

# Streamlit UI for Tourism Package Prediction
st.title("Tourism Package Prediction App")
st.write("""
This application predicts whether a customer will purchase the Wellness Tourism Package based on their details and interaction data.
Please enter the customer details below to get a prediction.
""")

# User input for features
st.header("Customer Details")

col1, col2 = st.columns(2)
with col1:
    Age = st.number_input("Age", min_value=18, max_value=100, value=30, step=1)
    NumberOfPersonVisiting = st.number_input("Number of Persons Visiting", min_value=0, max_value=10, value=1, step=1)
    PreferredPropertyStar = st.selectbox("Preferred Property Star", [3, 4, 5])
    NumberOfTrips = st.number_input("Number of Trips Annually", min_value=0, max_value=50, value=5, step=1)
    Passport = st.selectbox("Has Passport?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    OwnCar = st.selectbox("Owns Car?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
    NumberOfChildrenVisiting = st.number_input("Number of Children Visiting", min_value=0, max_value=5, value=0, step=1)

with col2:
    MonthlyIncome = st.number_input("Monthly Income", min_value=0, max_value=200000, value=50000, step=1000)
    PitchSatisfactionScore = st.slider("Pitch Satisfaction Score", min_value=1, max_value=5, value=3)
    NumberOfFollowups = st.number_input("Number of Followups", min_value=0, max_value=10, value=2, step=1)
    DurationOfPitch = st.number_input("Duration of Pitch (minutes)", min_value=0, max_value=120, value=20, step=1)
    TypeofContact = st.selectbox("Type of Contact", ["Company Invited", "Self Inquiry"])
    CityTier = st.selectbox("City Tier", [1, 2, 3])
    Occupation = st.selectbox("Occupation", ["Salaried", "Freelancer", "Small Business", "Large Business", "Student", "Housewife"])
    Gender = st.selectbox("Gender", ["Male", "Female"])
    MaritalStatus = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
    Designation = st.selectbox("Designation", ["Executive", "Manager", "Senior Manager", "AVP", "VP", "President", "CEO"])
    ProductPitched = st.selectbox("Product Pitched", ["Basic", "Standard", "Deluxe", "Super Deluxe", "King", "Luxury"])


# Assemble input into DataFrame
input_data = pd.DataFrame([{
    'Age': Age,
    'NumberOfPersonVisiting': NumberOfPersonVisiting,
    'PreferredPropertyStar': PreferredPropertyStar,
    'NumberOfTrips': NumberOfTrips,
    'Passport': Passport,
    'OwnCar': OwnCar,
    'NumberOfChildrenVisiting': NumberOfChildrenVisiting,
    'MonthlyIncome': MonthlyIncome,
    'PitchSatisfactionScore': PitchSatisfactionScore,
    'NumberOfFollowups': NumberOfFollowups,
    'DurationOfPitch': DurationOfPitch,
    'TypeofContact': TypeofContact,
    'CityTier': CityTier,
    'Occupation': Occupation,
    'Gender': Gender,
    'MaritalStatus': MaritalStatus,
    'Designation': Designation,
    'ProductPitched': ProductPitched
}])

if st.button("Predict Purchase"):
    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[:, 1][0] # Probability of positive class
    result = "WILL purchase" if prediction == 1 else "WILL NOT purchase"
    st.subheader("Prediction Result:")
    st.success(f"The model predicts the customer **{result}** the Wellness Tourism Package (Probability: {prediction_proba:.2f})")
