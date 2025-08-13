#!/bin/bash
set -e

sleep 5

export AWS_DEFAULT_REGION=sa-east-1
export AWS_DEFAULT_OUTPUT=json

echo "---"
echo "Inicializando recursos da AWS no LocalStack..."
echo "---"
echo "Criando buckets S3"
awslocal s3 mb s3://image-input
awslocal s3 mb s3://image-processed

echo "Criando filas FIFO SQS" 
awslocal sqs create-queue --queue-name new-image-input.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true
awslocal sqs create-queue --queue-name new-image-processed.fifo --attributes FifoQueue=true,ContentBasedDeduplication=true

echo "Buckets e filas criados com sucesso!"