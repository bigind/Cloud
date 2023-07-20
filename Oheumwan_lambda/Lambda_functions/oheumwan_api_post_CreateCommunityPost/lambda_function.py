import json
import pymysql
from datetime import datetime

# RDS 정보
rds_host = ""
user_name = ""
user_password = ""
db_name = ""

def lambda_handler(event, context):
    # RDS 연결 설정
    try:
        conn = pymysql.connect(host=rds_host, user=user_name, passwd=user_password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("RDS 연결 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

    # 게시글 데이터 추출
    username = event['username']
    content = event['content']
    image_path = event['image_path']
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 회원 조회 및 author_id 추출
    select_member_query = f"SELECT member_id FROM Members WHERE username = '{username}'"
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_member_query)
            result = cursor.fetchone()
            if result:
                author_id = result[0]
            else:
                print("해당 닉네임을 가진 회원이 존재하지 않습니다.")
                return {
                    'statusCode': 404,
                    'body': json.dumps('Member Not Found')
                }
    except pymysql.MySQLError as e:
        print("회원 조회 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

    # 게시글 삽입 쿼리
    insert_query = f"INSERT INTO CommunityPosts (author_id, content, image_path, creation_date, views) " \
                   f"VALUES ({author_id}, '{content}', '{image_path}', '{creation_date}', 0)"

    # RDS에 게시글 삽입
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_query)
            conn.commit()
        print("게시글이 성공적으로 생성되었습니다.")
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    except pymysql.MySQLError as e:
        print("게시글 생성 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    finally:
        conn.close()
