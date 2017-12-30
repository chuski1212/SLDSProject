import socket
import pyautogui
import threading
import twitchplaysWeb as webapp

server = "irc.twitch.tv"
port = 6667

# identificador de usuario para Twitch de la cuenta SLDS_Bot
password = "oauth:ivitob4is4f3q9g9mkv3fwk5f2jahe"

user = "bot"
owner = "slds_bot"

twitchirc = socket.socket()
twitchirc.connect((server, port));
twitchirc.send(('PASS %s\r\n' %password).encode())
twitchirc.send(('NICK %s\r\n' %user).encode())
twitchirc.send(('JOIN #%s\r\n' %owner).encode())


def sendMessage(message):
    temp = "PRIVMSG #" + owner + " :" + message + "\n"
    try:
        twitchirc.send(temp.encode())
    except:
        print("No he podido enviar el mensaje")


def enviar_a_socket(msg):
    webapp.send(msg)


def getUser(line):
    return line.split("!")[0][1:]


def getMessage(line):
    return line.split(":")[2]


# La key pulsada tendra efecto en la ventana que tenga el focus del sistema.
def pulsar_boton(boton):
        pyautogui.keyDown(boton)
        pyautogui.keyUp(boton)

# Inicio en paralelo del webservice que muestra los botones escritos en el chat
thread = threading.Thread(target=webapp.init)
thread.start()

while True:
    try:
        chatbuffer = twitchirc.recv(4096).decode()
        for line in chatbuffer.split("\n"):

            # Filtrado de las lineas que envía el servidor. Solamente nos quedamos con los mensajes
            # de los usuarios en el chat y los mensajes PING de Twitch

            if "PRIVMSG" in line:
                user = getUser(line)
                message = getMessage(line)
                if (message == "up\r"):
                    pulsar_boton('up')
                    enviar_a_socket({"button": {"user":user, "button":"up"}})
                if (message == "down\r"):
                    pulsar_boton('down')
                    enviar_a_socket({"button": {"user":user, "button":"down"}})
                if (message == "left\r"):
                    pulsar_boton('left')
                    enviar_a_socket({"button": {"user":user, "button":"left"}})
                if (message == "right\r"):
                    pulsar_boton('right')
                    enviar_a_socket({"button": {"user":user, "button":"right"}})

                # En este caso, nuestro emulador tiene asociadas las teclas 's' y 'a' con
                # los botones A y B de la consola respectivamente.

                if (message == "a\r"):
                    pulsar_boton('s')
                    enviar_a_socket({"button": {"user":user, "button":"a"}})
                if (message == "b\r"):
                    pulsar_boton('a')
                    enviar_a_socket({"button": {"user":user, "button":"b"}})
                if (message == "select\r"):
                    pulsar_boton('n')
                    enviar_a_socket({"button": {"user":user, "button":"select"}})
                if (message == "start\r"):
                    pulsar_boton('m')
                    enviar_a_socket({"button": {"user":user, "button":"start"}})
                # En caso de necesitar nuevas teclas para otros emuladores distintos,
                # simplemente habria que añadir aquí otro if para cada tecla nueva


            # El servidor de twitch nos envia un mensaje PING cada 5 minutos para comprobar que la conexión sigue
            # establecida y que hay alguien escuchando. Para mantener la conexión tenemos que contestar a estos PINGs
            # con un mensaje PONG

            if "PING" in line:
                respuesta = "PONG tmi.twitch.tv\r\n"
                twitchirc.send(respuesta.encode())

    except:
        continue

