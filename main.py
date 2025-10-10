
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import qrcode
import io
import base64
import pyotp

# --- Database Configuration ---
# TODO: Replace with your actual database credentials
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Yashbodake@9100",
    "database": "app_data",
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    finally:
        conn.close()

# --- Security Configuration ---
# TODO: Replace with a strong, randomly generated secret key
SECRET_KEY = "a_very_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

class UserInDB(BaseModel):
    username: str
    password: str
    otp_secret: str | None = None
    otp_enabled: bool = False

class User(BaseModel):
    username: str
    otp_enabled: bool

class Code(BaseModel):
    code: str

# --- FastAPI App Initialization ---
app = FastAPI()

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Utility Functions ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: mysql.connector.MySQLConnection = Depends(get_db_connection), expected_scope: str = None):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        scopes = payload.get("scopes", [])
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, scopes=scopes)
    except JWTError:
        raise credentials_exception

    if expected_scope and expected_scope not in token_data.scopes:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token scope",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (token_data.username,))
    user = cursor.fetchone()
    cursor.close()

    if user is None:
        raise credentials_exception
    return UserInDB(**user)


# --- API Endpoints ---
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (user.username,))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    
    hashed_password = get_password_hash(user.password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (user.username, hashed_password),
    )
    db.commit()
    cursor.close()
    return {"message": "User created successfully"}


@app.post("/login", response_model=Token)
def login(form_data: UserLogin, db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
    user = cursor.fetchone()
    cursor.close()

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user["otp_enabled"]:
        # If 2FA is enabled, issue a temporary token
        access_token_expires = timedelta(minutes=5)
        access_token = create_access_token(
            data={"sub": user["username"], "scopes": ["2fa:verify"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "scopes": ["full_access"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/2fa/enable")
def enable_2fa(current_user: UserInDB = Depends(get_current_user), db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    if current_user.otp_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is already enabled",
        )

    otp_secret = pyotp.random_base32()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET otp_secret = %s WHERE username = %s",
        (otp_secret, current_user.username),
    )
    db.commit()
    cursor.close()

    totp = pyotp.TOTP(otp_secret)
    qr_code_uri = totp.provisioning_uri(name=current_user.username, issuer_name="YourApp")

    # Generate QR code image
    img = qrcode.make(qr_code_uri)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"qr_code": f"data:image/png;base64,{img_str}", "otp_secret": otp_secret}


@app.post("/2fa/confirm")
def confirm_2fa(code: Code, current_user: UserInDB = Depends(get_current_user), db: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    if not code.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA code cannot be empty",
        )

    if current_user.otp_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is already enabled",
        )

    totp = pyotp.TOTP(current_user.otp_secret)
    if not totp.verify(code.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 2FA code",
        )

    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET otp_enabled = 1 WHERE username = %s",
        (current_user.username,),
    )
    db.commit()
    cursor.close()

    return {"message": "2FA enabled successfully"}

@app.post("/2fa/verify")
def verify_2fa(code: Code, current_user: UserInDB = Depends(get_current_user)):
    if not code.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA code cannot be empty",
        )

    if not current_user.otp_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA is not enabled for this user",
        )

    totp = pyotp.TOTP(current_user.otp_secret)
    if not totp.verify(code.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 2FA code",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username, "scopes": ["full_access"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=User)
def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user


@app.get("/dashboard")
def dashboard(current_user: UserInDB = Depends(get_current_user)):
    return {"message": f"Welcome {current_user.username} to your dashboard!"}
