import jwt
from fastapi import FastAPI, Depends, HTTPException, Request
import secrets
from pydantic import BaseModel, Field, model_validator, ValidationError
from typing import Dict

app = FastAPI()

# JWTの設定
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"


# トークンを生成する関数（JWSを利用）
def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# トークンを検証する関数
def verify_token(token: str):
    try:
        # トークンをデコードし、検証。ペイロードを取得
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="トークン認証エラー")


class TokenData(BaseModel):
    """
    トークンのパラメータをチェックする
    """
    data: Dict[str, str] = Field(..., example={"user_id": "1234", "username": "testuser"})

    @model_validator(mode="before")
    def check_data_keys(cls, values):
        # 送付データを確認
        data = values.get("data")
        if "user_id" not in data or "user_name" not in data:
            raise ValueError("user_idまたはuser_nameパラメータが存在しません。")
        return values

# トークンを生成するエンドポイント
@app.post("/token")
def generate_token(token_data: TokenData):
    access_token = create_access_token(token_data.data)
    return {"access_token": access_token}


# トークンを検証するエンドポイント
@app.get("/verify-token")
def check_token(request: Request):
    token = request.headers.get("Authorization")
    if token:
        token = token.split(" ")[1]  # "Bearer " の部分を除去
        payload = verify_token(token)
        return {"valid": True, "payload": payload}
    else:
        raise HTTPException(status_code=400, detail="Authorization header missing")


# エンドポイントの確認
@app.get("/")
def read_root():
    return {"message": "Hello World"}
