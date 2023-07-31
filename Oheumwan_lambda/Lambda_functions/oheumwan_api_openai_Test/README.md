## API: oheumwan_api_openai_Test
Chat GPT API를 사용하여 레시피를 추천받는 API 입니다.

Endpoint: POST /openai

### JSON Request Example:
```json
{
  "ingredient": "양파, 고기"
}
```

#### Parameters:

- `ingredient` (string): 재료 리스트

## Responses:

- `200 OK`: 성공
- `400 Bad Request`: 올바르지 않은 요청 매개변수입니다.
- `500 Internal Server Error`: 서버 오류

## axios
```js
axios.post(apiEndpoint, {
    ingredient: "양파, 고기",
}).then(res => {
  console.log(res);
}).catch(err => console.log(err))
```
