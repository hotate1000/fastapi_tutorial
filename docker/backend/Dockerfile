# Pythonのイメージを参考に、コンテナを作成
FROM python:3.9.0

# 作業ディレクトリを指定
WORKDIR /src

# Pythonのキャッシュファイルを作成
ENV PYTHONPYCACHEPREFIX=/var/cache/python
# モジュールの検索ベースディレクトリを指定
ENV PYTHONPATH=/src
# リアルタイムで標準出力をする
ENV PYTHONUNBUFFERED 1
# 言語設定を行う
ENV LANG=C.UTF-8
# タイムゾーンの指定
ENV TZ=Asia/Tokyo

# ホストマシーンのファイルをDockerコンテナにコピーする
COPY ./docker/backend/requirements.txt /src
COPY ./src /src

# コマンドの実行
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

# コマンドの実行
CMD ["uvicorn", "main:app", "--reload"]
