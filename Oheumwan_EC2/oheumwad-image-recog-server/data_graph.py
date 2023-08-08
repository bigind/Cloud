from flask import Blueprint
from sklearn.preprocessing import MinMaxScaler
import pymysql
import numpy as np
import pandas as pd
import statistics
import json

# 블루프린트 생성
data_graph = Blueprint('data_graph', __name__)

def get_info(identification):
    # The parameter for this code is user_id
    
    rds_host = "db.diligentp.com"
    rds_user = "park"
    rds_password = "qkrwjdgus"
    rds_db = "Oheumwan"
    conn = pymysql.connect(host=rds_host, user=rds_user, passwd=rds_password, db=rds_db, connect_timeout=5)

    sql1 = """
    SELECT *
    FROM temporary_file_history
    """
    history_df = pd.read_sql(sql1, conn)
    
    # Only in the table
    # user_id('abc')에 맞는 history 데이터 추출
    user_history = history_df[history_df['user_id']==identification]  # 실제 DB에서 호출하는 코드로 변경 필요. # Replace with your actual data
    # user_history

    user_category = user_history['CKG_STA_ACTO_NM']  
    # user_category

    # 카테고리 최빈값
    category_mode = statistics.mode(user_category)
    # category_mode # keyword only in the table

    # 해당 카테고리의 조리 횟수
    count_category = user_category.tolist().count(category_mode)  # with category_mode

    user_method = user_history['CKG_MTH_ACTO_NM']
    # user_method

    # 조리방식 최빈값
    method_mode = statistics.mode(user_method)
    # method_mode # keyword only in the table

    # 해당 조리방식 조리 횟수
    count_method = user_method.tolist().count(method_mode)  # with method_mode

    # Shown on the radar chart.

    # No need for scaling.
    # 난이도
    difficulty_levels = user_history['CKG_DODF_NM']
    difficulty_scores = {'아무나': 2.5, '초급': 5.0, '중급': 7.5, '고급': 10.0}

    scored_levels = [difficulty_scores[level] for level in difficulty_levels]

    # 난이도 최빈값
    user_level = statistics.mode(scored_levels)
    # user_level # keyword 

    # 해당 레벨 조리 횟수 
    count_level = scored_levels.count(user_level)  
    
    # call user_df from SQL
    sql2 = """
    SELECT *
    FROM temporary_file_user
    """
    
    user_df = pd.read_sql(sql2, conn)
    
    user_info = user_df[user_df['user_id']==identification]  # 실제 DB에서 호출하는 코드로 변경 필요. # user 'abc'의 정보 

    # 평점
    user_recipe_rating = float(user_info['recipe_rating'])
    # user_recipe_rating # keyword

    # Need for scaling

    # 등록한 레시피 수.
    user_registration = int(user_info['recipe_registration'])
    # user_registration # keyword

    # 조리자격증 수. 
    user_certificate = int(user_info['craftsman_cook'])
    # user_certificate # keyword

    # 팔로워 수.
    user_followers = int(user_info['followers'])
    # user_followers # keyword

    # 조리 횟수.
    user_times = int(user_info['times'])
    # user_times # keyword
        
    # Radar chart

    # scaling

    scaler = MinMaxScaler(feature_range=(0, 10))

    # scaled_registration
    all_registered_recipes = user_df['recipe_registration']  # user_df # Replace with the actual data

    scaler.fit([[min(all_registered_recipes)], [max(all_registered_recipes)]])

    normalized_registration = round(scaler.transform([[user_registration]])[0][0], 1)
    # normalized_registration # keyword_radar

    # scaled_certificate
    all_registered_certificate = user_df['craftsman_cook']

    scaler.fit([[min(all_registered_certificate)], [max(all_registered_certificate)]])

    normalized_certificate = round(scaler.transform([[user_certificate]])[0][0], 1)
    # normalized_certificate # keyword_radar

    # scaled_followers
    all_user_followers = user_df['followers']

    scaler.fit([[min(all_user_followers)], [max(all_user_followers)]])

    normalized_followers = round(scaler.transform([[user_followers]])[0][0], 1)
    # normalized_followers # keyword_radar

    # the_scaled_number_of_times
    all_user_numberoftimes = user_df['times']

    scaler.fit([[min(all_user_numberoftimes)], [max(all_user_numberoftimes)]])

    normalized_times = round(scaler.transform([[user_times]])[0][0], 1)
    # normalized_times # keyword_radar
    
    return identification, category_mode, count_category, method_mode, count_method, user_level, count_level, user_registration, user_certificate, user_followers, user_times, user_recipe_rating, normalized_registration, normalized_certificate, normalized_followers, normalized_times

@data_graph.route('/graph', methods=['GET'])
def get_data_graph():
    identification, category_mode, count_category, method_mode, count_method, user_level, count_level, user_registration, user_certificate, user_followers, user_times, user_recipe_rating, normalized_registration, normalized_certificate, normalized_followers, normalized_times = get_info("abc")

    # identification = identification

    data = [
        {
            "subject": "조리난이도",
            "A": user_level,
            "fullMark": 10,
        },
        {
            "subject": "조리자격증",
            "A": user_recipe_rating,
            "fullMark": 10,
        },
        {
            "subject": "등록레시피",
            "A": normalized_registration,
            "fullMark": 10,
        },
        {
            "subject": "레시피평점",
            "A": normalized_certificate,
            "fullMark": 10,
        },
        {
            "subject": "팔로워",
            "A": normalized_followers,
            "fullMark": 10,
        },
        {
            "subject": "조리 횟수",
            "A": normalized_times,
            "fullMark": 10,
        }
    ]
    
    return {
      'statusCode': 200,
      'body': json.dumps(data)  
    }

# {identification: user_id,} 
# values in the table
# {category_mode: '카테고리', 
# count_category: '해당 카테고리의 조리 횟수(카테고리와 함께 표시)', 
# method_mode: '조리방식', 
# count_method: '해당 조리방식의 조리 횟수(조리방식과 함께 표시)', 
# user_level: '조리난이도', 
# count_level: '해당 조리난이도의 조리 횟수(조리난이도와 함께 표시)', 
# user_registration: '등록레시피', 
# user_certificate: '조리자격증', 
# user_followers: '팔로워', 
# user_times: '조리횟수',
# }
# values in the radar chart.  
# {user_level: '조리난이도',
# user_recipe_rating: '레시피평점', 
# normalized_registration: '등록레시피', 
# normalized_certificate: '조리자격증', 
# normalized_followers: '팔로워', 
# normalized_times: '조리횟수',
# }