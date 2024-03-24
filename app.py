from PyQt6 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import google.generativeai as genai
import os, time
from api_gemini import API_KEY
from template import Ui_MainWindow
from functools import cache
from gtts import gTTS
from playsound import playsound

# Inicia Gemini
@cache
def gemini_ai(frase):
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(frase)
    try:
        texto = response.text
        ui.txt_chat.setText("Resposta:\n"+texto.replace("*", " "))        
        cria_audio(texto.replace("*", " "))
             
    except Exception as e:
        ui.txt_chat.setText(f'{type(e).__name__}: {e}')        
        cria_audio(f'{type(e).__name__}: {e}')         
     

# Funcao responsavel por falar
def cria_audio(texto):
    lingua= "pt"
    tts = gTTS(texto, lang=lingua)
    tts.save("audio.mp3")
    playsound("audio.mp3")    

# Funcao responsavel por ouvir e reconhecer a fala
def ouvir_microfone():   

    # Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:

        # Avisa ao usuario que esta pronto para ouvir
        cria_audio("Em que posso te ajudar?")

        # Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)

        # Armazena a informacao de audio na variavel
        audio = microfone.listen(source)

        try:
            # Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = microfone.recognize_google(audio, language="pt-BR")

            # Após alguns segundos, retorna a frase falada 
            if "sair" in frase:
                cria_audio("tudo bem")  
            else:         
                gemini_ai(frase)                


        # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            cria_audio("Não consegui entender...")
            time.sleep(3)
            ouvir_microfone()
            

# Entrada de texto
def enviar_chat():


    txt = ui.txt_chat.toPlainText()

    cria_audio(txt)

    try:
        # Após alguns segundos, retorna a frase falada                   
        gemini_ai(txt)
        ui.txt_chat.setText(texto.replace("*", " ")) 

        # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
    except:
        cria_audio("Verifique sua conexão ou api-key...")
        time.sleep(3)
        # ouvir_microfone()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # botões
    ui.bt_enviar.clicked.connect(enviar_chat)
    ui.bt_usar_mic.clicked.connect(ouvir_microfone)

    MainWindow.show()
    sys.exit(app.exec())
