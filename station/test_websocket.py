import uwebsockets.client as websocket_client

from station.security import HOST

# Подключаемся к WebSocket серверу
websocket = websocket_client.connect(HOST)

mesg = "The quick brown fox jumps over the lazy dog"
websocket.send(mesg + "\r\n")

resp = websocket.recv()
print(resp)

assert mesg + "\r\n" == resp  # Проверяем, что ответ соответствует отправленному сообщению

# Закрываем соединение
websocket.close()