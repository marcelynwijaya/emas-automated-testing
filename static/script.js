let charts = {};

function showSection(sectionId) {
    console.log("Membuka menu: " + sectionId); // Untuk debugging
    
    // 1. Sembunyikan semua section
    document.querySelectorAll('.content-section').forEach(s => s.classList.add('d-none'));
    
    // 2. Munculkan yang dipilih
    const activeSection = document.getElementById('section-' + sectionId);
    if (activeSection) {
        activeSection.classList.remove('d-none');
    }

    // 3. Update Judul Navbar
    const titles = {
        'home': 'Beranda', 'predictor': 'Prediksi LMKNN', 'dist_sentiment': 'Analisis Sentimen',
        'top_words': 'Top 20 Kata', 'dist_hour': 'Aktivitas per Jam', 'trend_sentiment': 'Tren Sentimen',
        'wordcloud': 'Word Cloud', 'crawling': 'Metode & Alur', 'tools': 'Tools', 'about': 'Tentang Proyek'
    };
    document.getElementById('section-title').innerText = titles[sectionId] || 'Dashboard';

    // 4. Render Grafik jika menu visualisasi dipilih
    if (['dist_sentiment', 'top_words', 'dist_hour', 'trend_sentiment'].includes(sectionId)) {
        renderCharts();
    }
}

async function renderCharts() {
    try {
        const response = await fetch('/get_stats');
        const data = await response.json();

        // Bersihkan chart lama agar tidak tumpang tindih
        Object.values(charts).forEach(c => c.destroy());

        // Pie Chart
        charts.pie = new Chart(document.getElementById('chartSentiment'), {
            type: 'pie',
            data: {
                labels: Object.keys(data.sentiment),
                datasets: [{ data: Object.values(data.sentiment), backgroundColor: ['#27ae60','#c0392b','#f1c40f'] }]
            }
        });

        // Bar Chart
        charts.bar = new Chart(document.getElementById('chartTopWords'), {
            type: 'bar',
            data: {
                labels: Object.keys(data.top_words),
                datasets: [{ label: 'Muncul', data: Object.values(data.top_words), backgroundColor: '#d4af37' }]
            },
            options: { indexAxis: 'y' }
        });

        // Line Chart Total
        charts.line = new Chart(document.getElementById('chartHourly'), {
            type: 'line',
            data: {
                labels: data.hours,
                datasets: [{ label: 'Total Tweet', data: data.hourly_total, borderColor: '#2c3e50', tension: 0.3 }]
            }
        });

        // Line Chart Trend
        charts.trend = new Chart(document.getElementById('chartTrend'), {
            type: 'line',
            data: {
                labels: data.hours,
                datasets: [
                    { label: 'Positif', data: data.trend_pos, borderColor: '#27ae60', tension: 0.3 },
                    { label: 'Negatif', data: data.trend_neg, borderColor: '#c0392b', tension: 0.3 },
                    { label: 'Netral', data: data.trend_neu, borderColor: '#f1c40f', tension: 0.3 }
                ]
            }
        });

    } catch (err) {
        console.error("Gagal memuat grafik:", err);
    }
}

async function checkSentiment() {
    const tweet = document.getElementById('tweetInput').value;
    if (!tweet) return alert("Isi teks!");
    
    const res = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tweet })
    });
    const data = await res.json();
    document.getElementById('predictionText').innerText = data.sentiment;
}