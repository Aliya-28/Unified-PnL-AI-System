from authentication import authenticate_user

username = input("Enter username: ")
password = input("Enter password: ")

user = authenticate_user(username, password)

if user:
    print("Login successful")
    print("Role:", user["role"])
else:
    print("Invalid login")