import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    name = event['name']
    image = event['file']
    
    print(name, image)
    
    image = image[image.find(",")+1:]
    dec = base64.b64decode(image + "===")
    content_type = 'image/jpeg'  # 타입 지정을 통해 s3에서 다운로드가 아닌 웹 형태로 보여지도록 설정
    
    s3.put_object(Bucket='oheumwan-image-upload', Key=name, Body=dec, ContentType=content_type)
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'successful lambda function call'})
    }
    