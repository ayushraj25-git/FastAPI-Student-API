from database import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute(
    "SELECT username, hashed_password FROM users WHERE username = ?",
    ("ayush_test",)
)

user = cursor.fetchone()

if user:
    print("Username:", user["username"])
    print("Stored password hash:", user["hashed_password"])
else:
    print("User not found")

conn.close()