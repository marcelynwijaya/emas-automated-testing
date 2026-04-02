from flask import Flask, render_template, request, jsonify
import pickle
import re
import string
import pandas as pd
import random

app = Flask(__name__)

# --- LOAD MODEL & DATA ---
try:
    model = pickle.load(open('model_lmknn.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf.pkl', 'rb'))
    print("✅ Model & TF-IDF Berhasil Dimuat")
except Exception as e:
    print(f"❌ Error Load Model: {e}")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+|@\w+|#\w+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stats')
def get_stats():
    try:
        df = pd.read_csv('hasil_sentimen_emas.csv')
        
        # Distribusi Sentimen
        col_label = 'label' if 'label' in df.columns else df.columns[-1]
        sentiment_counts = df[col_label].value_counts().to_dict()
        
        # Top 20 Kata
        col_text = 'clean_text' if 'clean_text' in df.columns else df.columns[0]
        all_text = " ".join(df[col_text].astype(str))
        words = [w for w in all_text.split() if len(w) > 3]
        word_freq = pd.Series(words).value_counts().head(20).to_dict()
        
        # Data Jam & Tren (Simulasi Agar Grafik Terisi)
        hours = [f"{str(i).zfill(2)}:00" for i in range(24)]
        hourly_total = [random.randint(50, 150) for _ in range(24)]
        trend_pos = [random.randint(20, 60) for _ in range(24)]
        trend_neg = [random.randint(10, 40) for _ in range(24)]
        trend_neu = [random.randint(10, 50) for _ in range(24)]

        return jsonify({
            'sentiment': sentiment_counts,
            'top_words': word_freq,
            'hours': hours,
            'hourly_total': hourly_total,
            'trend_pos': trend_pos,
            'trend_neg': trend_neg,
            'trend_neu': trend_neu
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    tweet = data.get('tweet', '')
    cleaned = clean_text(tweet)
    vec = tfidf.transform([cleaned])
    prediction = model.predict(vec)[0]
    return jsonify({'sentiment': str(prediction)})

if __name__ == '__main__':
    app.run(debug=True)