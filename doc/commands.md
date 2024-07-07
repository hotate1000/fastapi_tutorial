# コマンド関係

```bash
# 起動コマンド
# main: main.pyファイル (Python "module")。
# app: main.py内部で作られるobject（app = FastAPI()のように記述される）。
# --reload: コードの変更時にサーバーを再起動させる。開発用。
uvicorn main:app --reload
```

# サイト
| 概要 | URL |
| :--- | :--- |
| TOP | http://127.0.0.1:8000/ |
| APIリファレンス | http://127.0.0.1:8000/docs |
| OpenAPI | http://127.0.0.1:8000/redoc |
| OpenAPI_json形式 | http://127.0.0.1:8000/openapi.json |
