# Droneblocks Advanced Tello Programming
## Aruco Marker Detections

## Introduction

The purpose of this tutorial is demonstrate how we us use OpenCV to:

### １）ドローンシミュレーターを音声認識で操作する</br>
　概要：</br>
　ＧＣＰのSpeechToTextを使用して、音声をテキスト変換し、ChatGPT APIに入力し、ChatGPTの返答を基にシミュレーターへコマンドを送信する。また、ChatGPTからの返答は、pyttsx3を使用して音声に変換し、Chatボットとしても機能させる

　使用方法：</br>
    １. GCPのアカウント登録</br>
    　以下のサイトを参考にアカウント登録後、Google Cloud SDKを使えるようにする</br>
　   </link>https://blog.apar.jp/web/9893/</br>
    ２．必要なライブラリをインストールする</br>
    　※google-cloud-speechも要インストール</br>
    ３．Telloドローンシミュレーターを起動する</br>
    　以下のサイトからシミュレータを起動し、SimulationKeyをコピーして、sample_recognition_speech.py内のsim_keyに設定する</br>
    </link>https://coding-sim.droneblocks.io/</br>
    ４．sample_recognition_speech.pyスクリプト内のOPENAI_API_KEYにAPIキーを設定する</br>
    ５．必要に応じて、sample_recognition_speech.py内のAPI設定でChatGPT3.5と4.0を切り替える</br>
    ６. スクリプトを実行する</br>
    `python3 sample_recognition_speech.py`


### ２）Telloドローン実機で人の顔を追従させる
   概要：</br>
   Telloドローン実機を持ちて、カメラで人の顔をカスケード分類器により認識する
   認識した顔の位置が、カメラ画像の中央に来るようにドローンに左右上下の指示を送信する
   カメラ画像の更新周期遅延を抑制するため、画像認識＆ドローン操作コマンド演算は、画像更新とは別スレッドで処理する

   使用方法：</br>
    １. ドローンの起動</br>
        ドローンに電源をいれた後に、ドローンとWifi接続する</br>
    ２．python仮想環境の立ち上げ（各自設定）</br>
　　　`git clone https://github.com/dbaldwin/tello-adv-setup.git` </br>
　　　`cd venv/Scripts`</br>
　　　`Set-ExecutionPolicy RemoteSigned -Scope Proces`</br>
　　　`./active`</br>
　　　仮想環境内で必要なライブラリをインストールする</br>
　　　　※必要なライブラリは、tello-adv-setup-master/Readme.mdを参照のこと</br>
    ３．スクリプト実行<br>
　　　`cd ../../../tello-edv-aruco`</br>
　　　`python .\tello_script_runner.py --display-video --handler .\face-tracking.py --fly`

