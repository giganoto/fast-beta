CREATE TABLE IF NOT EXISTS "admins" (
  id SERIAL PRIMARY KEY,
  name VARCHAR(128) NOT NULL,
  email VARCHAR(128) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS "invalid_tokens" (
  token VARCHAR(256) PRIMARY KEY,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO "admins" (name, email) VALUES ('Shanu Khera', 'kherashanu@gmail.com');