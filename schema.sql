CREATE TABLE accounts (
  id text PRIMARY KEY,
  name text,
  email text,
  phone text
);

CREATE TABLE bikes (
  id text PRIMARY KEY,
  hypertrack_id text,
  account_id text,
  description text,
  is_on_loan boolean,
  loan_account_id text,
  FOREIGN KEY (account_id)
    REFERENCES accounts(id)
    ON DELETE CASCADE,
  FOREIGN KEY (loan_account_id)
    REFERENCES accounts(id)
    ON DELETE NO ACTION
)