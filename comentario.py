import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"] # nueva variable para el s3 bucket
    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
          'texto': texto
        }
    }
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # ingesta push
    s3 = boto3.client('s3')
    nombre_archivo = f"{uuidv1}.json" # usamos el uuid como nombre único del archivo
    
    response_s3 = s3.put_object(
        Bucket=nombre_bucket,
        Key=nombre_archivo,
        Body=json.dumps(comentario),
        ContentType='application/json'
    )
    
    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response,
        'response_s3' : response_s3
    }
