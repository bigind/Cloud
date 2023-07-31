import json
import openai

# OpenAI API 키 설정
openai.api_key = ""


def lambda_handler(event, context):
    ingredient = event['ingredient']  # 재료 받아오기
    
    prompt = f"나에게 {ingredient}가 있어 해당 재료로 만들 수 있는 음식 1가지만 추천해주고 해당 음식의 이름은 title에 담고 필요한 재료는 ingredients 에 담고 조리방법은 recipe 에 담아 나열해줘 부가설명없이 텍스트만"
    
    # ChatGPT에게 음식 추천 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "{}"}
        ]
    )

    # API 응답 처리
    recommendation = eval(response['choices'][0]['message']['content'].strip())
    
    name = recommendation['title']
    recipee = recommendation['recipe']
    object = recommendation['ingredients']
    
    return {
        'statusCode': 200,
        'dish': json.dumps(name, ensure_ascii=False),
        'object': json.dumps(object, ensure_ascii=False),
        'recipe': json.dumps(recipee, ensure_ascii=False)
    }