from PyQt6 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import google.generativeai as genai
import os
from api_gemini import API_KEY
from template import Ui_MainWindow
import pyttsx3


# Inicia Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Funcao responsavel por falar
def cria_audio(texto):

    # Inicialize o mecanismo TTS
    engine = pyttsx3.init()

    # Portugues brasil
    engine.setProperty("voice", "brazil")
    engine.setProperty('language', 'pt-br')

    # Altere a velocidade da fala (o padrão é 200)
    engine.setProperty("rate", 150)

    # Altere o volume da fala (o padrão é 1.0)
    engine.setProperty("volume", 0.8)

    # Fale o texto
    engine.say(texto)

    del texto

    # Aguarde até que a fala seja concluída antes de encerrar o programa
    engine.runAndWait()
   
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

            del audio
            

            # Após alguns segundos, retorna a frase falada
            response = model.generate_content(f"{frase}")

            del frase

            texto = response.text.replace("*", "")

            # imprime texto
            ui.txt_chat.setText(texto)

            cria_audio(texto)

            del texto

            
        # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            cria_audio("Verifique sua conexão à internet, se su microfone está ligado ou se configurou a api-key da Gemini corretamente...")


def enviar_chat():
    txt = ui.txt_chat.toPlainText()
    
    cria_audio(txt)

    del txt

    try:
        # Após alguns segundos, retorna a frase falada
        response = model.generate_content(f"{txt}")

        texto = response.text.replace("*", "")

        # imprime texto
        ui.txt_chat.setText(texto)        

        cria_audio(texto)

        del texto

        
    # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
    except:
        cria_audio("Verifique sua conexão à internet, se su microfone está ligado ou se configurou a api-key da Gemini corretamente...")


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