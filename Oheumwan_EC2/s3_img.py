import boto3
import botocore

# 외부에서 이미지 가져올때
# AWS_ACCESS_KEY_ID =""
# AWS_SECRET_ACCESS_KEY = ""
# s3_client = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

# boto3를 사용하여 AWS S3 서비스에 연결
s3_client = boto3.client('s3')

# 다운로드할 파일의 S3 버킷 경로와 로컬에 저장할 파일명 지정
s3_bucket_name = 'oheumwan-image-upload'  # S3 버킷 이름
s3_file_path = '244d4abe-8ec3-4402-affe-7cee06b24043.jpg'  # S3 내부의 파일 경로
local_filename = 'Image.jpg'  # 로컬에 저장될 파일명

def s3_get_img(s3_client, bucket, filepath, localpath):
    """
    S3 버킷에서 지정 파일을 다운로드합니다.
    :param s3: 연결된 S3 객체 (boto3 client)
    :param bucket: 버킷명
    :param filepath: 다운로드할 파일의 경로 및 이름 (S3 내부 경로)
    :param localpath: 저장 파일명 (다운로드 받을 로컬 파일명)
    :return: 성공 시 True, 실패 시 False 반환
    """
    try:
        s3_client.download_file(bucket, filepath, localpath) # S3 버킷에서 파일 다운로드
        return True
    
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("해당 파일이 S3 버킷에 존재하지 않습니다.")
        else:
            print("S3에서 파일을 다운로드하는 도중 오류가 발생했습니다.")
        return False


# 함수 호출하여 파일 다운로드
result = s3_get_img(s3_client, s3_bucket_name, s3_file_path, local_filename)
if result:
    print("파일 다운로드 성공!")
else:
    print("파일 다운로드 실패!")
