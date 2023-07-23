## API: CreateCommunityPost

This API allows users to create community posts.

Endpoint: GET /community

### JSON Request Example:
```json
{
  "username": "user1"
}
```

#### Parameters:

- `username` (string): 작성자의 username.

## Responses:

- `200 OK`: 게시글을 성공적으로 가져왔습니다.
- `400 Bad Request`: 올바르지 않은 요청 매개변수입니다.
- `404 Not Found`: 요청에서 지정한 사용자명이 존재하지 않습니다.
- `500 Internal Server Error`: 요청 처리 중 오류가 발생했습니다.

## Axios
```
axios.get(`${apiEndpoint}?username=${username}`)
  .then(res => {
    console.log(res)
  })
  .chtch(err => console.log(err))
```
