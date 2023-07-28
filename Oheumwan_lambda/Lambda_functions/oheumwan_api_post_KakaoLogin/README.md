## API: KakaoLogin

토큰을 사용해서 사용자의 정보를 조회하고 가져옵니다.
1. 토큰의 유효기간을 확인
2. 사용자 정보를 요청 후 정보를 RDS에 조회 (없으면 추가 후 반환, 있으면 그대로 반환)


Endpoint: POST - /kakao-login

### JSON Request Example:
```json
{
    "token": "A76DyIqSBjt1XQZExr6LzNsQSJDbUGneW85BWGlACinI2gAAAYmacOIt"
}
```

#### Parameters:

- `token` (string): kakao token

## Responses:

- `200 OK`: 사용자를 성공적으로 불러왔습니다
- `400 Bad Request`: 토큰 재발급 요청
- `500 Internal Server Error`: 내부 서버 오류

## axios
```js
axios.post(apiEndpoint, {
    token: token,
}).then(res => {
  console.log(res);
}).catch(err => console.log(err))
```
