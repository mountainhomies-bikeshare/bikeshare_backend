CREATE TABLE accounts (
  id text PRIMARY KEY,
  name text,
  email text,
  phone text
);

CREATE TABLE bikes (
  id text PRIMARY KEY,
  account_id text,
  description text,
  FOREIGN KEY (account_id)
    REFERENCES accounts(id)
    ON DELETE CASCADE
)