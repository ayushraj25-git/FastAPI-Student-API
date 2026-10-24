from pwdlib import PasswordHash
password_hash=PasswordHash.recommended()
password="mypassword123"
hashed_password= password_hash.hash(password)

print("Hashed password:",hashed_password)
#correct password check
result1=password_hash.verify(
    "mypassword123",
    hashed_password
)
print("Correct password:",result1)

#wrong password check
result2=password_hash.verify(
    "wrongpassword",
    hashed_password
)
print("Wrong password:",result2)