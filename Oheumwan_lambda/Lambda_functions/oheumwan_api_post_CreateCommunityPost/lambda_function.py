import json
import pymysql

# RDS 정보
rds_host = ""
user_name = ""
user_password = ""
db_name = ""

def lambda_handler(event, context):
    # RDS 연결 설정
    try:
        conn = pymysql.connect(rds_host, user=user_name, passwd=user_password, db=db_name, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("RDS 연결 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

    # 게시글 데이터 추출
    post_id = event['post_id']
    author_id = event['author_id']
    content = event['content']
    image_path = event['image_path']
    creation_date = event['creation_date']
    views = event.get('views', 0)  # 조회수는 선택적으로 받음

    # 게시글 삽입 쿼리
    insert_query = f"INSERT INTO CommunityPosts (post_id, author_id, content, image_path, creation_date, views) " \
                   f"VALUES ({post_id}, {author_id}, '{content}', '{image_path}', '{creation_date}', {views})"

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

