from flask import Blueprint, request
import json
import boto3
import botocore
import os
import subprocess

# 블루프린트 생성
image_recog = Blueprint('image_recog', __name__)

# 음식에 각각 매칭되는 라벨
food_list = {
    0: "양배추",
    1: "당근",
    2: "닭고기",
    3: "오이",
    4: "계란",
    5: "마늘",
    6: "버섯",
    7: "양파",
    8: "감자",
    9: "애호박",
    10: "생선",
    11: "햄",
    12: "고기",
    13: "가루",
    14: "두부",
    15: "고추",
    16: "김치",
    17: "피망",
    18: "토마토"
}

# 이미지 가져오는 함수
def s3_get_img(s3_file_path):
    # 외부에서 이미지 가져올때
    AWS_ACCESS_KEY_ID = "AKIARXDDTB7ONG754H7T"
    AWS_SECRET_ACCESS_KEY = "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"
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # 다운로드할 파일의 S3 버킷 경로와 로컬에 저장할 파일명 지정
    s3_bucket_name = 'oheumwan-image-upload'  # S3 버킷 이름
    # s3_file_path = '244d4abe-8ec3-4402-affe-7cee06b24043.jpg'  # S3 내부의 파일 경로
    local_filename = 'yolov5/Image.jpg'  # 로컬에 저장될 파일명

    try:
        s3_client.download_file(s3_bucket_name, s3_file_path, local_filename)  # S3 버킷에서 파일 다운로드
        return print("[로그] 이미지 파일 다운로드 성공")

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return print("[경고] 해당 파일이 S3 버킷에 존재하지 않습니다.")
        else:
            return print("[심각] S3에서 파일을 다운로드하는 도중 오류가 발생했습니다.")

# 이전에 진행했던 데이터를 삭제하는 함수
def remove_directory(path):
    # 해당 경로의 폴더가 존재하면 모두 제거합니다.
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
    print("[로그] 잔여 파일을 제거합니다. (yolov5/runs/detect/exp*)")

# yolov5_detection 이미지 인식을 진행하는 함수
def run_yolov5_detection():
    print("[로그] 이미지 인식을 시작합니다.")
    detect_command = f"python3 detect.py --weights bestv3.pt --img 416 --conf 0.1 --save-txt --source Image.jpg"
    subprocess.run(detect_command, shell=True, cwd="yolov5")
    print("[로그] 이미지 인식을 성공 하였습니다.")

# 인식을 통해 나온 결과에서 라벨 값만 리스트로 추출하는 함수
def extract_first_numbers_from_file(file_path):
    numbers_list = []
    
    try:
      with open(file_path, 'r') as file:
          for line in file:
              number = int(line.split()[0])
              numbers_list.append(number)
      return numbers_list
    
    except Exception as e:
        return False

# 숫자 리스트와 음식 리스트를 매칭하여 결과를 반환하는 함수
def match_food_with_numbers(numbers_list):
    result = {}
    for number in numbers_list:
        food = food_list.get(number)
        if food:
            result[food] = result.get(food, 0) + 1

    return result

# 이미지 인식 GET 매서드
@image_recog.route('/', methods=['GET'])
def get_image():
    image_url = request.args.get('image') # URL에서 Image 추출
    image_url_val = os.path.splitext(image_url)[0] # 이미지 이름만 추출

    # URL이 들어오면,
    if image_url:
        # 함수 호출하여 S3 버킷에서 파일 다운로드
        s3_get_img(image_url)

        # 기존 폴더 제거
        remove_directory("yolov5/runs/detect/")

        # 이미지 분석 YOLOv5 detect 명령어 실행
        run_yolov5_detection()

        # 이미지 라벨 출력
        detect_command = f"cat yolov5/runs/detect/exp/labels/Image.txt"  # 인식한 이미지 로그 출력
        subprocess.run(detect_command, shell=True)
        labels = extract_first_numbers_from_file('yolov5/runs/detect/exp/labels/Image.txt') # 로그에서 라벨만 출력
        
        if labels == False:
          return {
          'statusCode': 400,
          'body': json.dumps("인식된 재료가 없습니다!", ensure_ascii=False)
        }

        # 음식 매칭 후 JSON 반환
        result_dict = match_food_with_numbers(labels)
        print(result_dict)

        return {
          'statusCode': 200,
          'body': json.dumps(result_dict, ensure_ascii=False)
        }
        
    else:
        return {
            'statusCode': 400,
            'body': "No image URL provided."
        }

