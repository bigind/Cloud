import json
import pymysql
from datetime import datetime

# RDS 정보


def lambda_handler(event, context):
    post_id = int(event["post_id"])
    author_id = int(event["author_id"])
    new_content = event["new_content"]
    new_image_path = event["new_image_path"]

    # RDS 연결 설정
    try:
        conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("RDS 연결 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('내부 서버 오류', ensure_ascii=False)
        }
    
    try:
        with conn.cursor() as cursor:
            # 주어진 post_id에 해당하는 포스트를 가져옴
            sql_get_post = "SELECT * FROM CommunityPosts WHERE post_id = %s"
            cursor.execute(sql_get_post, (post_id,))
            post = cursor.fetchone()

            if not post:
                return {
                    'statusCode': 404,
                    'body': json.dumps('해당 포스트를 찾을 수 없습니다', ensure_ascii=False)
                }
            
            # 튜플에서 딕셔너리로 변환
            post_dict = {
                'post_id': post[0],
                'author_id': post[1],
                'content': post[2],
                'image_path': post[3],
                'creation_date': datetime.fromtimestamp(post[4]).strftime('%Y-%m-%d %H:%M:%S'),
                'views': post[5]
            }

            # 포스트의 author_id가 주어진 author_id와 일치하는지 확인
            if post_dict['author_id'] == author_id:
                # author_id가 일치하는 경우, 해당 포스트를 업데이트

                # 업데이트할 컬럼이 있는지 확인하여 해당 컬럼들을 새로운 값으로 업데이트
                if new_content:
                    post_dict['content'] = new_content
                
                if new_image_path:
                    post_dict['image_path'] = new_image_path

                # 업데이트된 값들을 데이터베이스에 반영
                sql_update_post = "UPDATE CommunityPosts SET content = %s, image_path = %s, creation_date = now() WHERE post_id = %s"
                cursor.execute(sql_update_post, (post_dict['content'], post_dict['image_path'], post_id))
                conn.commit()
                return {
                    'statusCode': 200,
                    'body': json.dumps('포스트가 성공적으로 업데이트되었습니다', ensure_ascii=False)
                }
            else:
                return {
                    'statusCode': 403,
                    'body': json.dumps('해당 포스트를 업데이트할 권한이 없습니다', ensure_ascii=False)
                }
    
    except pymysql.MySQLError as e:
        print("쿼리 실행 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('내부 서버 오류', ensure_ascii=False)
        }
    finally:
        conn.close()

