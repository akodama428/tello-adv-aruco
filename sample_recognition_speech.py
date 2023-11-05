import speech_recognition as sr
from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager
import os
import openai
import pyttsx3
import re

## 元ネタ
## https://qiita.com/Nekonun/items/2de0d5b3c77206c5ba31

## ここにOpenAIのAPI Keyを入力
## https://platform.openai.com/account/api-keys
OPENAI_API_KEY = "sk-***"

##############
# 音声認識関数 #
##############
def recognize_speech():

    recognizer = sr.Recognizer()    
    # Set timeout settings.
    recognizer.dynamic_energy_threshold = False

    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
    
        while(True):
            print(">> Please speak now...")
            audio = recognizer.listen(source, timeout=1000.0)

            try:
                # Google Web Speech API を使って音声をテキストに変換
                text = recognizer.recognize_google(audio, language="ja-JP")
                print("[You]")
                print(text)
                return text
            except sr.UnknownValueError:
                print("Sorry, I could not understand what you said. Please speak again.")
                #return ""
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                #return ""


#################################
# Pyttsx3でレスポンス内容を読み上げ #
#################################
def text_to_speech(text):
    # テキストを読み上げる
    engine.say(text)
    engine.runAndWait()

def chat(conversationHistory):
    # APIリクエストを作成する
    response = openai.ChatCompletion.create(
        messages=conversationHistory,
        max_tokens=1024,
        n=1,
        stream=True,
        temperature=0.5,
        stop=None,
        presence_penalty=0.5,
        frequency_penalty=0.5,
        model="gpt-3.5-turbo"
    )

    # ストリーミングされたテキストを処理する
    fullResponse = ""
    RealTimeResponce = ""   
    for chunk in response:
        text = chunk['choices'][0]['delta'].get('content')

        if(text==None):
            pass
        else:
            fullResponse += text
            RealTimeResponce += text
            print(text, end='', flush=True) # 部分的なレスポンスを随時表示していく

            target_char = ["。", "！", "？", "\n"]
            for index, char in enumerate(RealTimeResponce):
                if char in target_char:
                    pos = index + 2        # 区切り位置
                    sentence = RealTimeResponce[:pos]           # 1文の区切り
                    RealTimeResponce = RealTimeResponce[pos:]   # 残りの部分
                    # 1文完成ごとにテキストを読み上げる(遅延時間短縮のため)
                    engine.say(sentence)
                    engine.runAndWait()
                    break
                else:
                    pass

    # APIからの完全なレスポンスを返す
    return fullResponse


##############
# メインの関数 #
##############
if __name__ == '__main__':

    ##################
    # ChatGPTの初期化 #
    ##################
    openai.api_key = OPENAI_API_KEY
    # UserとChatGPTとの会話履歴を格納するリスト
    conversationHistory = []
    # setting = {"role": "system", "content": "句読点と読点を多く含めて応答するようにして下さい。また、1文あたりが長くならないようにして下さい。"}
    # setting = {"role": "system", "content": "あなたはドローンを制御する操縦士です。何かお願いされたら一言チャットで回答した後に、離陸してとお願いされた場合[takeoff]をつけて回答してください"}
    setting = {"role": "system", "content": "あなたはドローンを制御する操縦士です。何かお願いされたら一言チャットで回答した後に、依頼された内容に応じて末尾にドローン操縦コマンド[takeoff][land][forward][backward][right][left][up][down]をつけてください。複数コマンドがある場合は、最後にまとめてください。"}
    conversationHistory.append(setting)
    # chat(conversationHistory)
    
    ##################
    # Pyttsx3を初期化 #
    ##################
    engine = pyttsx3.init()
    # 読み上げの速度を設定する
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate)
    # Kyokoさんに喋ってもらう(日本語)
    engine.setProperty('voice', "com.apple.ttsbundle.Kyoko-premium")

    #######################
    # DroneSimulator初期化 #
    #######################
    # https://coding-sim.droneblocks.io/
    sim_key = '4ff79232-ca72-4625-9638-ce97b64299e7'
    distance = 40

    # Ctrl-Cで中断されるまでChatGPT音声アシスタントを起動
    while True:
        with DroneBlocksSimulatorContextManager(simulator_key=sim_key) as drone:

            # 音声認識関数の呼び出し
            text = recognize_speech()

            if text:
                print(" >> Waiting for response from ChatGPT...")
                # ユーザーからの発話内容を会話履歴に追加
                user_action = {"role": "user", "content": text}
                conversationHistory.append(user_action)

                print("[ChatGPT]") #応答内容をコンソール出力
                res = chat(conversationHistory)

                # ChatGPTからの応答内容を会話履歴に追加
                chatGPT_responce = {"role": "assistant", "content": res}
                conversationHistory.append(chatGPT_responce) 
                # print(conversationHistory)

                # if res.count("takeoff") >0:
                #     drone.takeoff()
                # elif res.count("forward") >0:
                #     drone.fly_forward(distance, 'in')
                # elif res.count("backward") >0:
                #     drone.fly_backward(distance, 'in')
                # elif res.count("left") >0:
                #     drone.fly_left(distance, 'in')
                # elif res.count("right") >0:
                #     drone.fly_right(distance, 'in')
                # elif res.count("up") >0:
                #     drone.fly_up(distance, 'in')
                # elif res.count("down") >0:
                #     drone.fly_down(distance, 'in')
                # elif res.count("land") >0:
                #     drone.land()
                command_functions = {
                    "takeoff": lambda: drone.takeoff(),
                    "forward": lambda: drone.fly_forward(distance, 'in'),
                    "backward": lambda: drone.fly_backward(distance, 'in'),
                    "left": lambda: drone.fly_left(distance, 'in'),
                    "right": lambda: drone.fly_right(distance, 'in'),
                    "up": lambda: drone.fly_up(distance, 'in'),
                    "down": lambda: drone.fly_down(distance, 'in'),
                    "land": lambda: drone.land()
                }

                # res内の単語を取得
                # 正規表現を使用して[]や「」を区切り文字として利用
                words = re.split(r'[ \[\]「」]', res)

                # 空の文字列を除外
                words = [word for word in words if word]
                print(words)

                # res内の単語の順番でコマンドを実行
                for word in words:
                    if word in command_functions:
                        command = command_functions[word]
                        command()
                        print(word)