from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import random
# IMPORT LOGIKA DARI PROCESSOR.PY
from processor import clean_text, validate_input 

app = Flask(__name__)

# --- LOAD MODEL & DATA ---
try:
    model = pickle.load(open('model_lmknn.pkl', 'rb'))
    tfidf = pickle.load(open('tfidf.pkl', 'rb'))
    print("✅ Model & TF-IDF Berhasil Dimuat")
except Exception as e:
    print(f"❌ Error Load Model: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stats')
def get_stats():
    try:
        df = pd.read_csv('hasil_sentimen_emas.csv')
        col_label = 'label' if 'label' in df.columns else df.columns[-1]
        sentiment_counts = df[col_label].value_counts().to_dict()
        
        col_text = 'clean_text' if 'clean_text' in df.columns else df.columns[0]
        all_text = " ".join(df[col_text].astype(str))
        words = [w for w in all_text.split() if len(w) > 3]
        word_freq = pd.Series(words).value_counts().head(20).to_dict()
        
        hours = [f"{str(i).zfill(2)}:00" for i in range(24)]
        return jsonify({
            'sentiment': sentiment_counts,
            'top_words': word_freq,
            'hours': hours,
            'hourly_total': [random.randint(50, 150) for _ in range(24)],
            'trend_pos': [random.randint(20, 60) for _ in range(24)],
            'trend_neg': [random.randint(10, 40) for _ in range(24)],
            'trend_neu': [random.randint(10, 50) for _ in range(24)]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    tweet = data.get('tweet', '')
    
    # GUNAKAN VALIDASI SEBELUM PREDIKSI
    if not validate_input(tweet):
        return jsonify({'sentiment': 'Input Tidak Valid (Minimal 3 Karakter)'})

    cleaned = clean_text(tweet)
    vec = tfidf.transform([cleaned])
    prediction = model.predict(vec)[0]
    return jsonify({'sentiment': str(prediction)})

if __name__ == '__main__':
    app.run(debug=True)