from flask import Flask, request
from flask_restx import Api, Resource, Namespace, fields
from config.config import (
  S3_BUCKET_INPUT, 
  SQS_QUEUE_INPUT
)

from services.aws_aux import (
  put_object_bucket,
  send_message  
)



app = Flask(__name__)
api = Api(
    app,
    version="0.0.1",
    title="Process-Image-API",
    description="API para binarização de imagens, utilizando SQS e S3",
    doc="/docs"
)

ns = Namespace("api", description="Operações com arquivos")
api.add_namespace(ns)

upload_response = ns.model("UploadResponse", {
  "message": fields.String(description="Mensagem de sucesso")
})

error_response = ns.model("ErrorResponse", {
  "error": fields.String(description="Mensagem de erro")
})

health_response = ns.model("HealthResponse", {
  "status": fields.String(description="Status da aplicação")
})

@ns.route("/upload")
class UploadFile(Resource):
  @ns.response(200, "Arquivo enviado com sucesso", upload_response)
  @ns.response(400, "Erro de validação", error_response)
  @ns.doc(
    description="Recebe um arquivo .png ou .jpg, envia para o bucket e envia mensagem na fila.",
    consumes=["multipart/form-data"]
  )
  @ns.expect(ns.parser().add_argument("file", location="files", type="file", required=True))
  def post(self):
    if "file" not in request.files:
      return {"error": "Nenhum arquivo enviado"}, 400

    file = request.files["file"]

    if not file.filename.lower().endswith((".png", ".jpg")):
      return {"error": "Apenas .png e .jpg são aceitos"}, 400

    key = file.filename
    body = file.read()

    put_object_bucket(key, body, S3_BUCKET_INPUT)
    send_message(key, SQS_QUEUE_INPUT)

    return {"message": f"Arquivo '{file.filename}' enviado com sucesso!"}, 200

@ns.route("/healthcheck")
class HealthCheck(Resource):
  @ns.marshal_with(health_response)
  def get(self):
      return {"status": "O app tá bem"}, 200

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)
