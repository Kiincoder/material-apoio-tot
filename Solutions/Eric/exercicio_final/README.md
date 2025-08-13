# Resumo

Esta é uma api simpes, desenvolvida para fins educativos utilizando as seguintes tecnologias:
  * Flask
  * AWS
  * Boto3
  * Bucket (S3)
  * Queue (SQS)
  * Docker

Como não há intuito de escalabilidade ou financeiro nessa api os serviços da AWS foram consumido através da imagem do **[Localstack](https://www.localstack.cloud/)**, assim facilitando o contexto geral da aplicação.


## Etapa 1: Instalar Docker
Primeiramente devemos ter o docker instalado na nossa máquina, a seguir o link da documentação do docker: **[DockerDocs](https://docs.docker.com/)**

## Etapa 2: Criar config/config.py
Nesta etapa devemos fazer a criação de uma pasta chamada ```/config``` e dentro dela deve haver um arquivo python chamado ```config.py```, o conteúdo dele será as chaves e constantes necessárias para que o sistema funcione. Siga o modelo abaixo:

```python
import os

ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "sua_info")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
AWS_REGION = os.getenv("AWS_REGION", "sua_info")

S3_BUCKET_INPUT = os.getenv("S3_BUCKET_INPUT", "sua_info")
S3_BUCKET_PROCESSED = os.getenv("S3_BUCKET_PROCESSED", "sua_info")

SQS_QUEUE_INPUT = os.getenv("SQS_QUEUE_INPUT", "sua_info")
SQS_QUEUE_PROCESSED = os.getenv("SQS_QUEUE_PROCESSED", "sua_info")

SQS_MESSAGE_GROUP_ID = os.getenv("SQS_MESSAGE_GROUP_ID", "sua_info")
```

## Etapa 3: Iniciar o container
Agora que temos o ambiente configurado, com docker instalado e com as configurações de env feitas, vamos partir para a iniciaização do container através dos comandos abaixo:

```bash
cd /diretorio_do_repositorio
docker-compose build #Build do container
```
Verifique se os container estão em execução devidamente:
```bash
docker ps
```

Caso queira parar o container:
```bash
docker-compose down
```

# Dicas

Esta API possui documentação própria, logo quando você inicializar pode acessar a rota ```http://localhost:5000/docs```, nela você irá encontrar as rotas para o uso da api, além disso o **worker** possui uma rota de checagem de saúde, através de ```http://localhost:5001/healthcheck```.

Para usuários windowns recomendo fortemente a utilização do **Docker Desktop**, pois facilita toda integração e controle dos containers.




