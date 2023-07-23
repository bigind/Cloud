## API: UpdateCommunityByPost

포스트를 수정하는 API 입니다.
포스트 작성자가 해당 포스트의 수정 권한이 있는지 확인 후 수정를 수행합니다.

Endpoint: PUT /community

### JSON Request Example:
```json
{
    "post_id": "1",
    "author_id": "1",
    "new_content": "content",
    "new_image_path": "image_path.jpg"
}
```

#### Parameters:

- `post_id` (string): 포스트 아이디
- `author_id` (string): 포스트 작성자 아이디
- `new_content` (string): 수정된 포스트 내용
- `new_image_path` (string): 수정된 이미지 경로

## Responses:

- `200 OK`: 포스트가 성공적으로 수정되었습니다
- `403 Bad Request`: 해당 포스트를 수정할 권한이 없습니다
- `404 Not Found`: 해당 포스트를 찾을 수 없습니다
- `500 Internal Server Error`: 내부 서버 오류

## axios
```js
axios.put(apiEndpoint, {
    post_id: "1",
    author_id: "1",
    new_content: "content",
    new_image_path: "image_path.jpg"
}).then(res => {
  console.log(res);
}).catch(err => console.log(err))
```
