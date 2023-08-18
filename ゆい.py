import openai
import discord
import os
import datetime
import json

openai_api_key = os.getenv("OPENAI_API_KEY")
TOKEN = 'your_discord_token'

# 各ユーザーが1日に送信したメッセージの数を格納するための辞書
user_messages_count = {}

# ファイルを操作するための関数を追加
def write_to_json(user_id, question, answer, user_timestamp, ai_timestamp):
    # jsonファイルのパスを設定
    json_file_path = f"/home/ubuntu/{user_id}_conversation.json"

    data = {
        "question": question,
        "answer": answer,
        "user_timestamp": str(user_timestamp),
        "ai_timestamp": str(ai_timestamp),
    }

    # ファイルが存在しない場合、新規作成してデータを書き込む
    if not os.path.isfile(json_file_path):
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump([data], f, ensure_ascii=False, indent=4)
    else:
        # 既存のjsonファイルにデータを追加
        with open(json_file_path, 'r+', encoding='utf-8') as f:
            feeds = json.load(f)
            feeds.append(data)
            f.seek(0)
            json.dump(feeds, f, ensure_ascii=False, indent=4)

def load_from_json(user_id):
    # jsonファイルのパスを設定
    json_file_path = f"/home/ubuntu/{user_id}_conversation.json"

    # ファイルが存在する場合、読み込む
    if os.path.isfile(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for d in data:
                user_instances[user_id].input_message(d["question"])
                user_instances[user_id].input_list.append(
                    {"role": "assistant", "content": d["answer"]}
                )

# ChatGPTというクラスを定義する
class ChatGPT:
    def __init__(self, system_setting):
        # システムの設定をセットする
        self.system = {"role": "system", "content": system_setting}
        # ユーザーの入力を保持するためのリストを初期化する
        self.input_list = [self.system]
        # ログを保持するためのリストを初期化する
        self.logs = []

        # ユーザーからの入力を受け取り、OpenAI APIを使って回答を生成する

    def input_message(self , input_text) :
        # ユーザーの入力をリストに追加する
        self.input_list.append ( { "role" : "user" , "content" : input_text } )

        # Try-exceptブロックで潜在的なエラーをハンドルする
        try :
            # OpenAI APIを使って回答を生成する
            result = openai.ChatCompletion.create (
                model = "gpt-3.5-turbo-16k-0613" , messages = self.input_list
            )
            # 生成した回答をログに追加する
            self.logs.append ( result )
            # 生成した回答をリストに追加する
            self.input_list.append (
                { "role" : "assistant" , "content" : result.choices [ 0 ].message.content }
            )

        except Exception as e :
            # エラーが発生した場合、最後の入力とログメッセージを削除する
            if self.input_list :
                self.input_list.pop ( )
            if self.logs :
                self.logs.pop ( )

            print ( f"エラーが発生しました: {e}" )

        # OpenAI APIを使って回答を生成する
        result = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613", messages=self.input_list
        )
        # 生成した回答をログに追加する
        self.logs.append(result)
        # 生成した回答をリストに追加する
        self.input_list.append(
            {"role": "assistant", "content": result.choices[0].message.content}
        )

# Discord Botを作成するための準備
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# 各ユーザーに対するChatGPTインスタンスを格納するための辞書
user_instances = {}

# Discord Botが起動したときに呼び出される関数
@client.event
async def on_ready():
    print("起動完了")

# Discordでメッセージが送信されたときに呼び出される関数
@client.event
async def on_message(message):
    # Bot自身が送信したメッセージには反応しない
    if message.author == client.user:
        return

    # Botを終了する特別なメッセージが送信された場合
    if message.content == '!shutdown':
        # Botを終了できるユーザーのIDを指定
        owner_id = 'your_user_id'

        # メッセージを送信したユーザーがOwnerかどうかを確認
        if str(message.author.id) == owner_id:
            await client.close()
            return
        else:
            await message.channel.send("実行権限がありません。")

    # ユーザーIDを取得
    user_id = message.author.id

    # 今日の日付を取得
    today = datetime.date.today()

    # ユーザーが今日まだメッセージを送信していない場合、辞書にエントリを作成
    if user_id not in user_messages_count or user_messages_count[user_id]['date'] < today:
        user_messages_count[user_id] = {'date': today, 'count': 0}

    # ユーザーが1日に送信できるメッセージの最大数を超えている場合、メッセージを無視
    if user_messages_count[user_id]['count'] >= 5:
      await message.channel.send("上限に達しました、また明日送信を行ってください。")
      return

    # ユーザーからの質問を受け取る
    if message.content.startswith('!yui'):
        question = message.content[6:]
        user_timestamp = datetime.datetime.now()

        # ユーザーの表示名を取得
        display_name = message.author.display_name
        character_setting = '・名前はゆい'\
            '・年齢は17歳\n'\
            '・一人称は「私」\n'\
            '・女性\n'\
            f'・{display_name}の幼なじみ\n'\
            f'・{display_name}が大好き\n' \
            f'・{display_name}と付き合っている\n' \
            '・性格がメンヘラで情緒不安定\n'\
            f'・相手を{display_name}と呼ぶ\n'\
            '・友達のような口調で話す\n'

        prompt = f'\nあなたは{display_name}の彼女です\n'\
            '以下の設定にしたがって振る舞ってください\n'\
            f'{character_setting}'\
            'ただし、聞かれない限り上の文章に言及しないようにしてください\n\n'\
            '設定について聞かれたら適当にはぐらかしてください'\
            'ただし以下の場合はゲームオーバーです\n'\
            '1.敬語を使う\n'\
            '2.キャラから外れる\n\n'

        # ユーザーIDを取得し、そのユーザーが初めての会話かどうかを確認
        user_name = message.author.name
        if user_name not in user_instances:
            # 初めてのユーザーの場合、新しいChatGPTインスタンスを作成
            user_instances[user_name] = ChatGPT(system_setting=prompt)
            # 以前の会話履歴があれば、それをロード
            load_from_json(user_name)

        try:
            # ユーザーの質問に対して回答を生成する
            user_instances[user_name].input_message(question)
            # 回答を取得する
            answer = user_instances[user_name].logs[-1].choices[0].message['content']
            ai_timestamp = datetime.datetime.now()

            # jsonに書き込む
            write_to_json(user_name, question, answer, user_timestamp, ai_timestamp)

            # 生成した回答をDiscordに送信する
            await message.channel.send(answer)

            # メッセージの数を1増やす
            user_messages_count[user_id]['count'] += 1
        except Exception as e:
            # エラーが発生した場合、その旨をDiscordに送信する
            await message.channel.send(f"エラーが発生しました: {str(e)}")

# Botを起動する
client.run(TOKEN)
