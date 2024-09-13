import streamlit as st
import pickle
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from googletrans import Translator

st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .main {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        color: #4B7BEC;
    }
    .footer {
        font-size: 0.85em;
        color: gray;
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🎬 IMDB Sentiment Analysis</div>', unsafe_allow_html=True)
st.write("Analyze the sentiment of movie reviews with a touch of AI!")

# Translator nesnesi
translator = Translator()

swords = set(stopwords.words("english"))

# Model ve vectorizer yükleme
with open('sentiment_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    loaded_vectorizer = pickle.load(vectorizer_file)

# Metin işleme fonksiyonu
def process(review):
    review = BeautifulSoup(review).get_text()
    review = re.sub("[^a-zA-Z]", ' ', review)
    review = review.lower().split()
    review = [w for w in review if w not in swords]
    stemmer = PorterStemmer()
    review = [stemmer.stem(word) for word in review]
    return " ".join(review)

# Kullanıcı girdisi ve dil seçeneği
user_input = st.text_area("📝 Enter your review:", key='english')
secenek = st.selectbox(
    '🌍 In which language do you want to perform sentiment analysis?',
    ('English', 'Turkish')
)

if st.button("🔮 Predict Sentiment"):
    st.write("---")
    st.subheader("🧠 Sentiment Analysis Result")

    if secenek == "English":
        processed_review = process(user_input)
    else:
        translated_input = translator.translate(user_input, dest='en')
        processed_review = process(translated_input.text)

    # Model tahmini
    transformed_review = loaded_vectorizer.transform([processed_review]).toarray()
    prediction = loaded_model.predict(transformed_review)
    result = "Positive" if prediction[0] == 1 else "Negative"

    if result == "Positive":
        st.success(f"Prediction: {result} 😊")
    else:
        st.error(f"Prediction: {result} 😔")

# Footer
st.markdown('<div class="footer">Powered by Natural Language Processing & AI 🚀</div>', unsafe_allow_html=True)
