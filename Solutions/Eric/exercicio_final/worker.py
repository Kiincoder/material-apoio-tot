from flask import Flask, jsonify
import time
from services.cv_processor import binarize_image
import threading

from services.aws_aux import (
  get_object_bucket,
  put_object_bucket,
  send_message,
  receive_message,
  delete_message
)

from config.config import (
  S3_BUCKET_INPUT,
  S3_BUCKET_PROCESSED,
  SQS_QUEUE_INPUT, 
  SQS_QUEUE_PROCESSED
)

app = Flask(__name__)

def queue_pooling():
  while True:
    try:
      messages = receive_message(SQS_QUEUE_INPUT)
      if not messages:
        continue
      for message in messages:
        image_key = message["Body"].strip()
        s3_object = get_object_bucket(image_key, S3_BUCKET_INPUT)

        data = s3_object["Body"].read()

        binarized_img = binarize_image(data)

        put_object_bucket(image_key, binarized_img, S3_BUCKET_PROCESSED)
        print("-> Imagem enviada para o bucket!") 
        send_message(f"{image_key} processada!", SQS_QUEUE_PROCESSED)
        print("-> Processado!") 
        delete_message(message, SQS_QUEUE_INPUT)
        
    except Exception as e:
      print(f"Erro ao processar mensagem: {e}")
      time.sleep(5)

@app.route("/healthcheck", methods=["GET"])
def worker_health():
    return jsonify({"status": "O guri tá bem!"}), 200

if __name__ == "__main__":
  thread = threading.Thread(target=queue_pooling, daemon=True)
  thread.start()
  app.run(host="0.0.0.0", port=5001)
