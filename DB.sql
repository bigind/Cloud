-- 회원 테이블 (Members)
CREATE TABLE Members (
  member_id INT PRIMARY KEY,        -- 회원 번호
  nickname VARCHAR(50) NOT NULL,    -- 회원 닉네임
  password VARCHAR(50) NOT NULL,    -- 회원 비밀번호
  email VARCHAR(100) NOT NULL,      -- 회원 이메일
  registration_date DATETIME NOT NULL -- 회원 가입 일시
);

-- 커뮤니티 게시글 테이블 (CommunityPosts)
CREATE TABLE CommunityPosts (
  post_id INT PRIMARY KEY,          -- 게시글 번호
  title VARCHAR(100) NOT NULL,      -- 게시글 제목
  author_id INT,                    -- 게시글 작성자의 회원 번호
  content TEXT,                     -- 게시글 내용
  creation_date DATETIME NOT NULL,  -- 게시글 작성 일시
  views INT DEFAULT 0,              -- 조회수
  FOREIGN KEY (author_id) REFERENCES Members(member_id) -- 외래 키: 작성자는 회원 테이블의 회원 번호 참조
);

--댓글 테이블 (Comments)
CREATE TABLE Comments (
  comment_id INT PRIMARY KEY,       -- 댓글 번호
  post_id INT,                      -- 댓글이 달린 게시글 번호
  author_id INT,                    -- 댓글 작성자의 회원 번호
  content TEXT,                     -- 댓글 내용
  creation_date DATETIME NOT NULL,  -- 댓글 작성 일시
  FOREIGN KEY (post_id) REFERENCES CommunityPosts(post_id), -- 외래 키: 게시글 번호는 커뮤니티 게시글 테이블의 게시글 번호 참조
  FOREIGN KEY (author_id) REFERENCES Members(member_id)     -- 외래 키: 작성자는 회원 테이블의 회원 번호 참조
);

--재료 테이블 (Ingredients)
CREATE TABLE Ingredients (
  owner_id INT,                     -- 재료 소유자의 회원 번호
  ingredient_id INT PRIMARY KEY,    -- 재료 번호
  name VARCHAR(100) NOT NULL,       -- 재료 이름
  image_path VARCHAR(200),          -- 재료 이미지 경로
  FOREIGN KEY (owner_id) REFERENCES Members(member_id) -- 외래 키: 소유자는 회원 테이블의 회원 번호 참조
);

--레시피 테이블 (Recipes)
CREATE TABLE Recipes (
  owner_id INT,                     -- 레시피 소유자의 회원 번호
  recipe_id INT PRIMARY KEY,        -- 레시피 번호
  name VARCHAR(100) NOT NULL,       -- 레시피 이름
  image_path VARCHAR(200),          -- 레시피 이미지 경로
  FOREIGN KEY (owner_id) REFERENCES Members(member_id) -- 외래 키: 소유자는 회원 테이블의 회원 번호 참조
);

CREATE TABLE RecipeIngredients (
  recipe_id INT,                    -- 레시피 번호
  ingredient_id INT,                -- 재료 번호
  FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id),      -- 외래 키: 레시피 번호는 레시피 테이블의 레시피 번호 참조
  FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id) -- 외래 키: 재료 번호는 재료 테이블의 재료 번호 참조
);
