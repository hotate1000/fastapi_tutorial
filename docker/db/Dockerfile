# postgresのイメージを参考に、コンテナを作成
FROM postgres:latest

# 以下コマンドを実行
# -i ja_JP: 入力ロケールデータをja_JP（日本）に設定
# -c: エラーが発生しても続行
# -f UTF-8: 文字セットをUTF-8に設定し
# -A /usr/share/locale/locale.alias: ロケールエイリアスファイルを指定
# ja_JP.UTF-8: 定義するロケールの名前
RUN localedef -i ja_JP -c -f UTF-8 -A /usr/share/locale/locale.alias ja_JP.UTF-8
ENV LANG ja_JP.utf8
