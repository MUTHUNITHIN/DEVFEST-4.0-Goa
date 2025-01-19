import streamlit as st
import pandas as pd
import pickle
from streamlit_extras.let_it_rain import rain  

# Load the trained model and label encoders
with open("gift_recommendation_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("label_encoders.pkl", "rb") as le_file:
    label_encoders = pickle.load(le_file)

# styling
st.markdown("""
<style>
    body {
        background-color: #F5F7FA;
        color: #3C403D;
        font-family: 'Comic Sans MS', sans-serif;  /* Fall back to sans-serif if Comic Sans is not available */
    }
    .stTitle {
        color: #FF5733;
        text-shadow: 2px 2px 5px #FFC300;
    }
    .stSuccess {
        color: #28a745;  /* Customize success message color */
        font-size: 20px; /* Adjust font size */
    }
</style>
""", unsafe_allow_html=True)

# Add animation at the top
rain(
    emoji="🎁",
    font_size=40,
    falling_speed=4,
    animation_length="infinite",
)

# Streamlit app title with emojis
st.title("🎉 Gift Recommendation App 🎁")

st.subheader("Tell us about the recipient to find the perfect gift! 🎀")
form = st.form("gift_details", clear_on_submit=True)

questions = [
    "What do you enjoy most?",
    "How do you prefer to relax?",
    "What's your favorite activity?",
    "Do you like trying new things?",
    "How do you prefer to spend weekends?",
    "What's your favorite type of movie?",
    "Do you enjoy outdoor activities?",
    "What's your go-to snack?",
    "How do you feel about pets?",
    "What's your favorite season?",
    "Do you prefer coffee or tea?",
    "How do you like to socialize?",
    "What's your favorite type of music?",
    "Do you enjoy reading?",
    "How do you feel about sports?",
    "What's your favorite cuisine?",
    "Do you like to travel?",
    "How do you prefer to learn?",
    "What's your favorite hobby?",
    "Do you enjoy cooking?",
    "How do you feel about art?",
    "What's your favorite game?",
    "Do you prefer city or nature?",
    "How do you feel about technology?",
    "What's your favorite way to exercise?"
]

optionsMap = {
    0: ["Traveling", "Reading", "Gaming", "Cooking"],
    1: ["Watching TV", "Reading", "Meditating", "Exercising"],
    2: ["Sports", "Arts & Crafts", "Gaming", "Cooking"],
    3: ["Yes", "No", "Sometimes", "Depends"],
    4: ["Relaxing at home", "Going out", "Hiking", "Shopping"],
    5: ["Action", "Comedy", "Drama", "Horror"],
    6: ["Yes", "No", "Sometimes", "Only with friends"],
    7: ["Chips", "Fruits", "Chocolate", "Nuts"],
    8: ["Love them", "Neutral", "Prefer not to have", "Allergic"],
    9: ["Summer", "Winter", "Spring", "Fall"],
    10: ["Coffee", "Tea", "Juice", "Water"],
    11: ["In person", "Online", "Both", "Rarely"],
    12: ["Pop", "Rock", "Classical", "Jazz"],
    13: ["Yes", "No", "Sometimes", "Only magazines"],
    14: ["Love it", "Neutral", "Not a fan", "Only some sports"],
    15: ["Italian", "Chinese", "Mexican", "Indian"],
    16: ["Yes", "No", "Sometimes", "Only for work"],
    17: ["Hands-on", "Visual", "Auditory", "Reading"],
    18: ["Crafting", "Sports", "Reading", "Gaming"],
    19: ["Yes", "No", "Sometimes", "Only for special occasions"],
    20: ["Running", "Yoga", "Weightlifting", "Swimming"],
    21: ["Modern", "Classical", "Abstract", "Street Art"],
    22: ["Board games", "Video games", "Outdoor games", "Card games"],
    23: ["City", "Nature", "Both", "Depends on mood"],
    24: ["Love it", "Neutral", "Not a fan", "Only for work"],  
}

answers = []
for i, question in enumerate(questions):
    answer = form.selectbox(f"**{question}**", options=optionsMap[i])
    answers.append(answer)

#  submit button
submitted = form.form_submit_button("🎯 Get Gift Recommendation")


if submitted:
    input_data = pd.DataFrame({f'Q{i+1}': [answer] for i, answer in enumerate(answers)})
    
    # encode 
    for column in input_data.columns:
        input_data[column] = label_encoders[column].transform(input_data[column])

    # Predict the gift \
    prediction = model.predict(input_data)
    gift_category = label_encoders['Gift Category'].inverse_transform(prediction)

    # Displays the recommended gift category with celebration
    st.success(f"🎁 Recommended gift category: **{gift_category[0]}** 🎉")
    st.balloons()  # Animation for success
