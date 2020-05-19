import uuid
from threading import Thread
import pygame
import pika
import json

ip = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen = pygame.display.set_mode((1000, 600))


class TankRpcClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=ip,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None
        self.bullet_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)
            print(self.response)

    def call(self, key, message={}):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self):
        self.call('tank.request.healthcheck')
        return self.response['status'] == '200'

    def obtain_token(self, room_id):
        message = {
            'room_id': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tank_id']
            self.room_id = self.response['room_id']
            #return True
        #return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self, token):
        message = {
            'token': token
        }
        self.call('tank.request.fire', message)
        if 'token' in self.response:
            self.bullet_id = self.response['owner']


class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=ip,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        event_listener = queue.method.queue
        self.channel.queue_bind(exchange='X:routing.topic',
                                queue=event_listener,
                                routing_key='event.state.room-5')
        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)


    def run(self):
        self.channel.start_consuming()

    def end(self):
        self.channel.close()


client = TankRpcClient()
client.check_server_status()
client.obtain_token('room-5')
event_client = TankConsumerClient('room-5')
event_client.start()

UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'
SPACE = 'SPACE'

MOVE_KEYS = {
    pygame.K_UP: UP,
    pygame.K_LEFT: LEFT,
    pygame.K_DOWN: DOWN,
    pygame.K_RIGHT: RIGHT
}

FIRE_KEY = {
    pygame.K_SPACE: SPACE
}


def draw_tank(x, y, width, height, direction, **kwargs):
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, (255, 0, 0),
                     (x, y, width, width), 2)
    pygame.draw.circle(screen, (255, 0, 0), tank_c, int(width / 2))


def draw_bullet(x, y, width, height, direction, **kwargs):
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 2)


def game_start():
    mainloop = True
    font = pygame.font.Font('freesansbold.ttf', 32)
    while mainloop:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainloop = False
                if event.key in MOVE_KEYS:
                    client.turn_tank(client.token, MOVE_KEYS[event.key])
                if event.key in FIRE_KEY:
                    client.fire_bullet(client.token)
        try:
            remaining_time = event_client.response['remainingTime']
            text = font.render('Remaining Time: {}'.format(remaining_time), True, (255, 255, 255))
            textRect = text.get_rect()
            textRect.center = (500, 100)
            screen.blit(text, textRect)
            hits = event_client.response['hits']
            bullets = event_client.response['gameField']['bullets']
            winners = event_client.response['winners']
            tanks = event_client.response['gameField']['tanks']
            for tank in tanks:
                draw_tank(**tank)
            for bullet in bullets:
                draw_bullet(**bullet)
        except:
            pass

        pygame.display.flip()

    client.connection.close()
    pygame.quit()


game_start()
