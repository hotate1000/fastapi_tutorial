import jwt
import secrets
from fastapi import FastAPI, HTTPException, Request, Security
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field, model_validator
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict


app = FastAPI()

# JWTの設定
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"

# Bearer認証スキームを設定する
security = HTTPBearer()


class TokenData(BaseModel):
    data: Dict[str, str] = Field(
        ...,
        example={
            "user_id": "1234",
            "user_name": "testuser"
        }
    )

    @model_validator(mode="before")
    def check_data_keys(cls, values: dict):
        """
        トークンのパラメータをチェックする

        Parameters
        ----------
        values: dict\n
            チェックする値
        """
        # 送付データを確認
        data = values.get("data")
        if "user_id" not in data or "user_name" not in data:
            raise ValueError("user_idまたはuser_nameパラメータが存在しません。")
        return values


@app.post("/token", tags=["token"])
def generate_token(token_data: TokenData):
    """
    トークンを生成

    Parameters
    ----------
    token_data: TokenData\n
        トークンの値
    """
    access_token = __create_access_token(token_data.data)
    return {"access_token": access_token}


@app.get("/check_token", tags=["token"])
def check_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    """
    トークンの情報を確認

    Parameters
    ----------
    request: Request\n
        クライアントからのリクエスト情報\n
    credentials : HTTPAuthorizationCredentials, optional\n
        Bearerトークンを含む認証情報を取得\n
        Security(security)によって、認証スキームを適応
    """
    # トークンを取得
    token = credentials.credentials
    payload = verify_token(token)
    return {"valid": True, "payload": payload}


# エンドポイントの確認
@app.get("/")
def read_root():
    return {"message": "Hello World"}


# トークンを生成する関数（JWSを利用）
def __create_access_token(data: dict):
    """
    JWSを利用してトークンを作成

    Parameters
    ----------
    token: dict\n
        トークン情報
    """
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    トークンを検証

    Parameters
    ----------
    token: str\n
        トークンの情報
    """
    try:
        # トークンをデコードし、検証。ペイロードを取得
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="トークン認証エラー")
