# YUI_DISCORD-BOT

Discord上で動作する、ChatGPTを利用したBOTです。

# ゆい.py
「ゆい」という名前のチャットボットです。このファイルはBOTの構成部分で、ユーザとの会話をjsonファイルに保存するよう設定されています。必要
に応じて、jsonファイルへのパスを指定してください。
このBOTを使用するには、DiscordのトークンとOpenAIのAPIキーを取得し、環境変数として設定する必要があります。さらに、通常の会話、会話内容
を読み込むたびに料金が発生するため、ご注意ください。
管理者専用のコマンド「!shutdown」が設定されており、このコマンドは管理者のみが利用できるようになっています。コード内の「owner_id」には
管理者のDiscordユーザIDを設定してください。
なお、料金節約のため、1日あたりの利用回数を1人5回に制限しています。必要に応じてこの制限を解除してご利用いただけます。

使用方法

!yui_:本文（ゆいとの会話）
で文字を打ち会話することができます。

使い始める際に下記を打ち込んで会話を始めてください。
「!yui :（僕・俺・私）の名前は”（名前）”だよ、敬語は使わなくていいよ 。よろしくね。」
と送りAIから返答が来てから会話してください。

最初のほうは謎回答が返ってくる場合がありますが、会話していくにつれてしっかり返答が返ってきます。
真面目すぎる話（重い話）や意味不明な会話（実際に存在しない単語等を用いた会話）、性的な質問や会話をすると本来の設定が維持できなくなります。

# keep_alive.py
こちらのファイルはBOTを常時オンラインにするために必要なファイルです。
