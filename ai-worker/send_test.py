import pika
import json

# 1. Setting Kredensial (Harus sama dengan di Docker & main.py)
credentials = pika.PlainCredentials('user', 'password123')

# 2. Hubungkan ke RabbitMQ
parameters = pika.ConnectionParameters(
    host='localhost',
    port=5672,
    credentials=credentials
)

try:
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # 3. Pastikan antrean (queue) ada
    channel.queue_declare(queue='task_ingestion', durable=True)

    # 4. Siapkan Data Percobaan (Gunakan UUID yang ada di Postgres kamu)
    message = {
        "sekolah_id": "3a4cbeac-3023-4699-8d52-6dc87183df49",
        "narasi": """
        Desa Majapahit di Bonerate memiliki keunikan geografis berupa pantai berpasir putih. 
        Masyarakat lokal sangat mahir dalam navigasi laut tradisional. 
        Komoditas utama mereka selain kelapa adalah hasil laut berupa teripang. 
        Jarak ke pusat kabupaten Selayar sekitar 120 mil laut.
        """
    }

    # 5. Kirim Pesan
    channel.basic_publish(
        exchange='',
        routing_key='task_ingestion',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Membuat pesan persisten (tidak hilang jika restart)
        )
    )

    print("📨 [BERHASIL] Pesan pengujian telah dikirim ke RabbitMQ!")
    print(f"Sekolah ID: {message['sekolah_id']}")

    connection.close()

except Exception as e:
    print(f"❌ Gagal mengirim pesan: {e}")