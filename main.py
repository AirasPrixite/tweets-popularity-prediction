import streamlit as st
from joblib import load
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np

# Load the trained Random Forest and Logistic Regression models
rf_model = load("random_forest_model.joblib")
lr_model = load("logistic_regression_model.joblib")

# Initialize OpenAI API client
client = OpenAI(api_key="Enter API Key Here")

# Initialize the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def analyze_tweet_with_gpt(tweet):
    prompt = f"""
Analyze the following tweet in terms of engagement potential, ensuring the tweet length is within 280 characters. 
Structure the response with bullet points and **bold heading** for each element:

\n

- **Emotional Language**: Analyze if the tweet uses engaging, emotional language. \n
- **Call-to-Action**: Check if there's a clear call-to-action to drive interaction. \n
- **Hashtags**: Evaluate hashtags' relevance. Suggest improvements if any hashtags are present, or add 2-3 relevant hashtags if missing. \n
- **Mentions**: Confirm if relevant accounts are tagged to increase visibility. \n
- **Visual Prompt**: Indicate if the tweet includes or implies a visual element. \n
- **Conciseness**: Confirm if it's concise and within 280 characters.\n
- **Question**: See if it includes a question to boost replies. \n
- **Positive Sentiment**: Confirm if the tone is positive and inviting. \n
- **Storytelling**: Analyze if there's a quick stoiry or relatable experience.\n

For each item, note if it is "Present" or "Missing," then conclude with an overall "High" or "Low" engagement potential rating. If "Low," provide improvement suggestions. Also add a rephrased verion of the tweet where you provide a rephrased tweet that can garner high attention. 
Add a heading called "REPHRASED TWEET" and add the tweet in there
Tweet:
"{tweet}"
"{tweet}"
    """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a social media engagement expert."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def preprocess_input(tweet_text, additional_features):
    tweet_embedding = embedding_model.encode(tweet_text).reshape(1, -1)
    return np.hstack((tweet_embedding, np.array(additional_features).reshape(1, -1)))

def predict_engagement_rf(tweet_text, additional_features):
    X_input = preprocess_input(tweet_text, additional_features)
    prediction = rf_model.predict(X_input)[0]
    return "High Engagement" if prediction == 1 else "Potentially Low Engagement"

def predict_engagement_lr(tweet_text, additional_features):
    X_input = preprocess_input(tweet_text, additional_features)
    prediction = lr_model.predict(X_input)[0]
    return "High Engagement" if prediction == 1 else "Potentially Low Engagement"

# Streamlit app with enhanced UI
st.set_page_config(page_title="Tweet Engagement Analyzer", page_icon="🐦", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1DA1F2;'>Tweet Engagement Analyzer 🐦</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: grey;'>Enter a tweet below to analyze its potential for high engagement</h4>", unsafe_allow_html=True)

st.write("---")
tweet = st.text_area("Your Tweet:", max_chars=280, help="Enter up to 280 characters.")
st.markdown(f"<p style='text-align: right;'>Characters: {len(tweet)}/280</p>", unsafe_allow_html=True)

# Feature placeholders (replace with actual feature values or gather them dynamically if needed)
additional_features = [0, 0, 0, 0, len(tweet), 0]  # Adjust as necessary for the tweet characteristics

if st.button("Analyze Engagement Potential"):
    if len(tweet) > 280:
        st.error("🚨 Tweet exceeds the 280-character limit. Please shorten it.")
    elif len(tweet) == 0:
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing with GPT-4, Random Forest, and Logistic Regression..."):
            # Get predictions from both models
            rf_prediction = predict_engagement_rf(tweet, additional_features)
            lr_prediction = predict_engagement_lr(tweet, additional_features)
            
            # Get GPT-4 analysis and recommendation
            gpt_analysis = analyze_tweet_with_gpt(tweet)

        # Display the results in Streamlit
        st.write("---")
        st.subheader("📊 Engagement Predictions")
        
        # Display GPT-4 Analysis as Primary Result
        st.subheader("GPT-4 Engagement Analysis & Recommendations")
        st.markdown(
            "<div style='border: 2px solid #1DA1F2; padding: 15px; border-radius: 10px; background-color: #f0f8ff;'>"
            f"{gpt_analysis}</div>",
            unsafe_allow_html=True
        )
        
        # Display a summarizing message based on ML model predictions
        st.markdown("### Random Forest and Logistic Regression Analysis")
        if rf_prediction == "Potentially Low Engagement" and lr_prediction == "Potentially Low Engagement":
            st.info("Our initial analysis suggests that this tweet might not perform optimally based on Random Forest and Logistic Regression models. However, consider GPT-4's recommendations to enhance engagement!")
        else:
            st.info("Both Random Forest and Logistic Regression models predict positive engagement potential. Follow GPT-4's recommendations to maximize impact!")

        st.success("Analysis Complete!")

# Tips and guidance section
st.write("---")
st.subheader("💡 Pro Tips for High Engagement")
st.markdown("""
- **Use Visuals**: Tweets with images or videos generally see higher engagement.
- **Engage Emotionally**: Words that elicit emotion can increase shares and reactions.
- **Hashtags & Mentions**: Use relevant hashtags and tag popular accounts when appropriate.
- **Keep it Concise**: Tweets under 100 characters can improve readability and engagement.
- **Ask Questions**: Inviting your audience to answer questions can boost replies.
""")

# Footer with contact info
st.write("---")
st.markdown("<p style='text-align: center; color: grey;'>Made with ❤️ by Your Twitter Assistant</p>", unsafe_allow_html=True)

