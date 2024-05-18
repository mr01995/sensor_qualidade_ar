import time
import board
import busio
import adafruit_scd30
import paho.mqtt.client as mqtt

# Configuração dos pinos I2C (dependendo da sua placa e conexão)
i2c = busio.I2C(board.SCL, board.SDA)

# Inicialização dos sensores
scd30 = adafruit_scd30.SCD30(i2c)  # Sensor de CO2
# Para outros sensores, adicione inicializações correspondentes

# Configuração MQTT
broker = 'seu_broker_mqtt'  # Endereço do seu broker MQTT
port = 1883  # Porta do broker MQTT
topic = 'qualidade_do_ar'  # Tópico MQTT para enviar os dados
client_id = 'sensor_node'

def on_connect(client, userdata, flags, rc):
    print(f"Conectado ao broker MQTT com código {rc}")

def on_publish(client, userdata, mid):
    print(f"Dado publicado com ID: {mid}")

# Inicialização do cliente MQTT
client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker, port, 60)
client.loop_start()

while True:
    if scd30.data_available:
        co2 = scd30.CO2
        temperature = scd30.temperature
        humidity = scd30.relative_humidity

        # Formatação dos dados
        payload = f"CO2: {co2:.2f} ppm, Temp: {temperature:.2f} C, Hum: {humidity:.2f}%"
        print(payload)
        
        # Publicação dos dados no broker MQTT
        result = client.publish(topic, payload)
        status = result[0]

        if status == 0:
            print(f"Mensagem enviada para o tópico {topic}")
        else:
            print(f"Falha ao enviar mensagem para o tópico {topic}")

    time.sleep(10)  # Intervalo de 10 segundos entre as leituras
