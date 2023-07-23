from flask import Flask, request, jsonify
import boto3
import botocore
import os
import subprocess

# 플라스크 앱 생성
app = Flask(__name__)

# 음식에 각각 매칭되는 라벨
food_list = {
    0: "cabbage : 양배추",
    1: "carrot : 당근",
    2: "chicken : 닭고기",
    3: "cucumber : 오이",
    4: "egg : 달걀",
    5: "fish : 생선",
    6: "garlic : 마늘",
    7: "ham : 스팸",
    8: "meat : 고기(돼지, 소)",
    9: "mushroom : 버섯",
    10: "onion : 양파",
    11: "potato : 감자",
    12: "powder : 가루 종류 포장지(튀김, 부침, 밀가루 ...)",
    13: "tofu : 두부",
    14: "zucchini : 애호박"
}

## 이미지 가져오는 함수
"""
    S3 버킷에서 지정 파일을 다운로드합니다.
    :param s3: 연결된 S3 객체 (boto3 client)
    :param bucket: 버킷명
    :param filepath: 다운로드할 파일의 경로 및 이름 (S3 내부 경로)
    :param localpath: 저장 파일명 (다운로드 받을 로컬 파일명)
    :return: 성공 시 True, 실패 시 False 반환
"""
def s3_get_img(s3_file_path):
    # 외부에서 이미지 가져올때
    AWS_ACCESS_KEY_ID = ""
    AWS_SECRET_ACCESS_KEY = ""
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # 다운로드할 파일의 S3 버킷 경로와 로컬에 저장할 파일명 지정
    s3_bucket_name = 'oheumwan-image-upload'  # S3 버킷 이름
    # s3_file_path = '244d4abe-8ec3-4402-affe-7cee06b24043.jpg'  # S3 내부의 파일 경로
    local_filename = 'yolov5/Image.jpg'  # 로컬에 저장될 파일명

    try:
        s3_client.download_file(s3_bucket_name, s3_file_path, local_filename)  # S3 버킷에서 파일 다운로드
        return True

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("해당 파일이 S3 버킷에 존재하지 않습니다.")
        else:
            print("S3에서 파일을 다운로드하는 도중 오류가 발생했습니다.")
        return False

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

# yolov5_detection 이미지 인식을 진행하는 함수
def run_yolov5_detection(image_path):
    detect_command = f"python3 detect.py --weights best.pt --img 416 --conf 0.1 --save-txt --source {image_path}"
    subprocess.run(detect_command, shell=True, cwd="yolov5")

# 인식을 통해 나온 결과에서 라벨 값만 리스트로 추출하는 함수
def extract_first_numbers_from_file(file_path):
    numbers_list = []
    with open(file_path, 'r') as file:
        for line in file:
            number = int(line.split()[0])
            numbers_list.append(number)
    return numbers_list

# 음식 리스트와 숫자 리스트를 매칭하여 결과를 반환하는 함수
def match_food_with_numbers(numbers_list):
    result = {}
    for number in numbers_list:
        food = food_list.get(number)
        if food:
            result[food.split(" : ")[1]] = result.get(food.split(" : ")[1], 0) + 1

    return result
    
@app.route("/")
def hello():
    return "Hello World!"

# 이미지 인식 GET 매서드
@app.route('/get_image', methods=['GET'])
def get_image():
    image_url = request.args.get('image') # URL에서 Image 추출

    if image_url: # URL이 들어오면,
        image_name = image_url.split('/')[-1]

        # 함수 호출하여 파일 다운로드
        result = s3_get_img(image_name)
        if result:
            print("[LOG] : 이미지 파일 다운로드 성공!")
        else:
            print("[ERROR] : 이미지 파일 다운로드 실패!")

        # 폴더 제거
        remove_directory("yolov5/runs/detect/")
        print("[LOG] : 잔여 파일을 제거합니다. (yolov5/runs/detect/exp*)")

        # YOLOv5 detect 명령어 실행
        print("[LOG] : 이미지 분석을 진행합니다.")
        run_yolov5_detection('test3.jpg')
        print("[LOG] : 이미지 분석을 성공 하였습니다.")

        detect_command = f"cat yolov5/runs/detect/exp/labels/test3.txt"
        subprocess.run(detect_command, shell=True)

        print("[LOG] : 이미지 라벨을 추출합니다.")
        labels = extract_first_numbers_from_file('yolov5/runs/detect/exp/labels/test3.txt')

        print("[LOG] : 이미지 라벨에서 음식을 매칭합니다.")
        result_dict = match_food_with_numbers(labels)

        print("[LOG] : 성공적으로 처리되었습니다.")
        return jsonify(result_dict), 200
    else:
        return "No image URL provided.", 400

    
if __name__ == '__main__': 
	app.run(host="0.0.0.0", debug=False, port=80)
