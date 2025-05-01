CREATE TABLE biodata (
    id SERIAL PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    address TEXT,
    dob DATE,
    phone TEXT,
    email TEXT,
    gender TEXT,
    photo BYTEA,
    hobbies TEXT
);
