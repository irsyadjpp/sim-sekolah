import pika
import json
import os
import sys
from dotenv import load_dotenv
from app.worker import process_database_chunking

load_dotenv()

def callback(ch, method, properties, body):
    try:
        # Parsing instruksi dari Go
        # Format: {"sekolah_id": "...", "fase": "A", "mapel": "Agama", "kelas": "1"}
        task = json.loads(body)
        
        sekolah_id = task.get('sekolah_id')
        fase = task.get('fase')
        mapel = task.get('mapel')
        kelas = task.get('kelas')

        print(f"\n📩 [NEW TASK] Ingestion Kurikulum: {mapel} Fase {fase}")

        # Jalankan proses query & chunking
        success = process_database_chunking(sekolah_id, fase, mapel, kelas)
        
        if success:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"🏁 Task selesai untuk {mapel}.")
        else:
            # Jika data tidak ada, tetap ack agar tidak macet di antrean
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"⚠️ Task diabaikan karena data DB kosong.")

    except Exception as e:
        print(f"❌ Global Worker Error: {e}")
        # Jangan requeue jika error format data, cegah loop error
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    # Kredensial RabbitMQ
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "user"),
        os.getenv("RABBITMQ_PASS", "password123")
    )
    
    parameters = pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=5672,
        credentials=credentials,
        heartbeat=3600 # Set 1 jam agar koneksi tidak putus saat Ollama sibuk
    )

    try:
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue='task_ingestion', durable=True)
        
        # Prefetch 1: Kerjakan satu-satu secara berurutan (SANGAT PENTING untuk RAM)
        channel.basic_qos(prefetch_count=1)
        
        channel.basic_consume(queue='task_ingestion', on_message_callback=callback)

        print('🚀 SIM-AI CURRICULUM WORKER IS RUNNING...')
        print('📍 Menunggu instruksi dari Go Backend...')
        channel.start_consuming()

    except KeyboardInterrupt:
        print("\n🛑 Worker dihentikan.")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Gagal startup: {e}")

if __name__ == "__main__":
    main()