from passlib.context import CryptContext

# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# dummy user database
users_db = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),
        "role": "admin"
    },
    "analyst": {
        "username": "analyst",
        "password": pwd_context.hash("analyst123"),
        "role": "analyst"
    },
    "manager": {
        "username": "manager",
        "password": pwd_context.hash("manager123"),
        "role": "manager"
    }
}

# verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# authenticate user
def authenticate_user(username, password):

    user = users_db.get(username)

    if not user:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user


# authorization check
def authorize_user(user, required_role):

    if user["role"] != required_role:
        return False

    return True