import json
import pymysql
import requests
from datetime import datetime

# RDS 정보

# 토큰 정보 확인 URL
access_token_info = "https://kapi.kakao.com/v1/user/access_token_info"
# 사용자 정보 가져오는 URL
user_info = "https://kapi.kakao.com/v2/user/me"



def lambda_handler(event, context):
    token = event["token"]  # 토큰을 받아옴

    # 헤더에 Authorization 토큰 추가 (JWT를 사용하는 경우)
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-type': "application/x-www-form-urlencoded;charset=utf-8"
    }

    # RDS 연결 설정
    try:
        conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db, connect_timeout=5)
        cursor = conn.cursor()
    except pymysql.MySQLError as e:
        print("RDS 연결 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('내부 서버 오류', ensure_ascii=False)
        }

    # 1. 토큰의 유효기간을 확인
    try:
        response = requests.get(access_token_info, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            print("API 응답:", response_data)
        else:
            print("API 요청 실패:", response.status_code)

    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 400,
            'body': json.dumps('토큰 다시 발급해주세요!')
        }

    # 2. 사용자 정보를 요청 후 정보를 RDS에 조회 (없으면 추가 후 반환, 있으면 그대로 반환)
    try:
        response = requests.get(user_info, headers=headers)

        if response.status_code == 200:
            data = response.json()

            user_id = data['id']
            username = data['properties']['nickname']
            registration_date_str = data['connected_at']  # 문자열 형식으로 받음

            # registration_date_str을 DATETIME 형식으로 변환
            registration_date = datetime.fromisoformat(registration_date_str.replace('Z', '+00:00'))

            profile_image = data['properties']['profile_image']
            thumbnail_image = data['properties']['thumbnail_image']
            age_range = data['kakao_account']['age_range'] if data['kakao_account']['has_age_range'] else None
            email = data['kakao_account']['email'] if data['kakao_account']['has_email'] else None
            gender = data['kakao_account']['gender'] if data['kakao_account']['has_gender'] else None

            print(user_id, username, registration_date, profile_image, thumbnail_image, age_range, email, gender)

            # 사용자 ID가 데이터베이스에 존재하는지 확인합니다.
            sql_select = "SELECT * FROM Members WHERE member_id = %s;"
            cursor.execute(sql_select, (user_id,))
            row = cursor.fetchone()

            if row:
                # 사용자 ID가 존재하는 경우 해당 행을 반환합니다.
                result = {
                    'statusCode': 200,
                    'body': json.dumps({
                        'member_id': row[0],
                        'username': row[1],
                        'registration_date': row[2].isoformat(),  # datetime 객체를 문자열로 변환
                        'email': row[3],
                        'profile_image': row[4],
                        'thumbnail_image': row[5],
                        'age_range': row[6],
                        'gender': row[7]
                    })
                }
            else:
                # 사용자 ID가 존재하지 않는 경우 데이터를 데이터베이스에 삽입한 후 반환합니다.
                sql_insert = "INSERT INTO Members (member_id, username, registration_date, email, profile_image, thumbnail_image, age_range, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
                cursor.execute(sql_insert, (user_id, username, registration_date, email, profile_image, thumbnail_image, age_range, gender))
                conn.commit()
                result = {
                    'statusCode': 200,
                    'body': json.dumps({
                        'member_id': user_id,
                        'username': username,
                        'registration_date': registration_date.isoformat(),  # datetime 객체를 문자열로 변환
                        'email': email,
                        'profile_image': profile_image,
                        'thumbnail_image': thumbnail_image,
                        'age_range': age_range,
                        'gender': gender
                    })
                }

        else:
            print("API 요청 실패:", response.status_code)
            result = {
                'statusCode': 500,
                'body': json.dumps('API 요청 실패', ensure_ascii=False)
            }

    except requests.exceptions.RequestException as e:
        print("API 요청 오류:", e)
        result = {
            'statusCode': 500,
            'body': json.dumps('API 요청 오류', ensure_ascii=False)
        }

    cursor.close()
    conn.close()
    return result