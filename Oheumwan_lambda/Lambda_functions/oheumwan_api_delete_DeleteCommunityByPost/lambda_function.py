import json
import pymysql
from datetime import datetime

# RDS 정보


def lambda_handler(event, context):
    # RDS 연결 설정
    try:
        conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db, connect_timeout=5)
    except pymysql.MySQLError as e:
        print("RDS 연결 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('내부 서버 오류')
        }
    
    # 유저 추출    
    username = event['username']
    
    try:
        with conn.cursor() as cursor:
            # 제공된 username을 기반으로 Members 테이블에서 member_id 가져오기
            sql_get_member_id = "SELECT member_id FROM Members WHERE username = %s"
            cursor.execute(sql_get_member_id, (username,))
            result = cursor.fetchone()
            
            # 멤버가 존재하지 않는 경우
            if not result:
                return {
                    'statusCode': 404,
                    'body': json.dumps('사용자를 찾을 수 없습니다')
                }
            
            member_id = result[0]
            
            # 해당 member_id에 대한 CommunityPosts 테이블에서 포스트 가져오기
            sql_get_posts = "SELECT * FROM CommunityPosts WHERE author_id = %s"
            cursor.execute(sql_get_posts, (member_id,))
            rows = cursor.fetchall()
            
            # 결과를 담을 리스트 초기화
            posts = []
            
            # 조회 결과를 딕셔너리 형태로 변환하여 리스트에 추가
            for row in rows:
                post = {
                    'post_id': row[0],
                    'author_id': row[1],
                    'content': row[2],
                    'image_path': row[3],
                    'creation_date': datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S'),  # datetime 객체를 문자열로 변환
                    'views': row[5]
                }
                posts.append(post)
            
            # 조회 결과가 없을 경우 메시지 반환
            if not posts:
                return {
                    'statusCode': 404,
                    'body': json.dumps('해당 사용자의 포스트를 찾을 수 없습니다')
                }
                
            return {
                'statusCode': 200,
                'body': json.dumps(posts, default=str)  # datetime 객체를 직렬화하기 위해 default=str 옵션 추가
            }
    
    except pymysql.MySQLError as e:
        print("쿼리 실행 오류:", e)
        return {
            'statusCode': 500,
            'body': json.dumps('내부 서버 오류')
        }
    finally:
        conn.close()
