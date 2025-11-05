from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2, os

app = Flask(__name__)
CORS(app)

# Veritabanı bağlantısı
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://sevval:C2TbUsmgDpeSO5zG34kl2cLqd94IoUaC@dpg-d426lkpr0fns739009mg-a.oregon-postgres.render.com/hello_cloud2_db_n274"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# 🔹 Ana sayfa rotası (Render ve tarayıcı testleri için)
@app.route("/")
def home():
    return "Ziyaretçi API çalışıyor 🚀"

# 🔹 Ziyaretçi kayıt & listeleme endpoint'i
@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ziyaretciler (id SERIAL PRIMARY KEY, isim TEXT)")

    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(isimler)

# 🔹 Uygulama yerel çalıştırma ayarı
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
