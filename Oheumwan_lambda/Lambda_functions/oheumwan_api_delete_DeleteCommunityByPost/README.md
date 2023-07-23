## API: ReadCommunityByUse

포스트를 삭제하는 API 입니다.
포스트 작성자가 해당 포스트의 삭제 권한이 있는지 확인 후 삭제를 수행합니다.

Endpoint: GET /community

### JSON Request Example:
```json
{
    "post_id":"1",
    "author_id": "1"
}
```

#### Parameters:

- `post_id` (string): 포스트 아이디
- `author_id` (string): 포스트 작성자 아이디

## Responses:

- `200 OK`: 포스트가 성공적으로 삭제되었습니다
- `403 Bad Request`: 해당 포스트를 삭제할 권한이 없습니다
- `404 Not Found`: 해당 포스트를 찾을 수 없습니다
- `500 Internal Server Error`: 내부 서버 오류

## axios
```js
axios.delete(apiEndpoint, {
    post_id: "1",
    author_id: "1",
}).then(res => {
  console.log(res);
}).catch(err => console.log(err))
```
