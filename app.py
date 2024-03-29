from PyQt6 import QtCore, QtGui, QtWidgets
import speech_recognition as sr
import google.generativeai as genai
import os, time
from api_gemini import API_KEY
from template import Ui_MainWindow
from functools import cache
from gtts import gTTS
from playsound import playsound

def ocultar_output():
    ui.txt_resposta.hide()

def exibir_output():
    ui.txt_resposta.show()

# Inicia Gemini
@cache
def gemini_ai(pergunta):

    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(pergunta)
    if response:
        texto = response.text
        # Atualiza caixa de resposta
        ui.txt_chat.setText(f"{pergunta}")
        ui.txt_resposta.setMarkdown(f"{texto}")
        
        # Fala a Resposta
        cria_audio(texto.replace("*", " "))
             
    else:
        ui.txt_resposta.setText("Erro!")        
        cria_audio("Aconteceu algum erro!")         
     

# Funcao responsavel por falar
def cria_audio(texto):
    lingua= "pt"
    tts = gTTS(texto, lang=lingua)
    tts.save("audio.mp3")
    playsound("audio.mp3")    

# Funcao responsavel por ouvir e reconhecer a fala
def ouvir_microfone():  

    exibir_output() 
    time.sleep(0.3)    

    ui.txt_resposta.setText("")

    # Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:

        # Avisa ao usuario que esta pronto para ouvir
        cria_audio("Diga!")

        # Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)

        # Armazena a informacao de audio na variavel
        audio = microfone.listen(source)

        try:
            # Passa o audio para o reconhecedor de padroes do speech_recognition
            pergunta = microfone.recognize_google(audio, language="pt-BR")           

            # Após alguns segundos, retorna a frase falada 
            gemini_ai(pergunta)

            # Atualiza Caixa de pergunta
            ui.txt_chat.setText(pergunta.capitalize())                


        # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            cria_audio("Não entendi! Clique no botão novamente!")
            

# Entrada de texto
def enviar_chat():

    exibir_output()
    time.sleep(0.3)

    ui.txt_resposta.setText("")

    txt = ui.txt_chat.toPlainText()

    if txt:
       
        try:
            # Após alguns segundos, retorna a frase falada                   
            gemini_ai(txt)
            
            # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except:
            cria_audio("Verifique sua conexão ou api-key...")
            time.sleep(3)
            # ouvir_microfone()
    else:

        cria_audio("Digite alguma coisa!")

# Função para limpar a caixa de texto
def limpar_caixa_de_texto():
    ocultar_output()
    ui.txt_resposta.setText("")
    ui.txt_chat.setText("")

# Copiar a caixa de texto
def copiar_a_caixa_de_texto():
    texto = ui.txt_chat.toPlainText()
    texto += ui.txt_resposta.toPlainText()
    
    os.system(f"echo '{texto}' | xclip -select clipboard")
    
    limpar_caixa_de_texto()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    ocultar_output()

    # botões
    ui.bt_enviar.clicked.connect(enviar_chat)
    ui.bt_usar_mic.clicked.connect(ouvir_microfone)
    ui.bt_erase.clicked.connect(limpar_caixa_de_texto)
    ui.bt_copy.clicked.connect(copiar_a_caixa_de_texto)

    MainWindow.show()
    sys.exit(app.exec())
