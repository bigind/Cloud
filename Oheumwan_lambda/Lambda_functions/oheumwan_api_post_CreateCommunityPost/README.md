## API: CreateCommunityPost

포스트를 생성하는 API 입니다.

Endpoint: POST /community

### JSON Request Example:
```json
{
  "username": "user1",
  "content": "테스트",
  "image_path": "test.jpg"
}
```

#### Parameters:

- `username` (string): 사용자 아이디.
- `content` (string): 생성할 포스트 내용.
- `image_path` (string): 이미지 경로.

## Responses:

- `200 OK`: 게시글이 성공적으로 생성되었습니다.
- `400 Bad Request`: 올바르지 않은 요청 매개변수입니다.
- `404 Not Found`: 요청에서 지정한 사용자명이 존재하지 않습니다.
- `500 Internal Server Error`: 요청 처리 중 오류가 발생했습니다.

## axios
```js
axios.post(apiEndpoint, {
    username: "user1",
    content: initialContent,
    image_path: fileName,
}).then(res => {
  console.log(res);
}).catch(err => console.log(err))
```
