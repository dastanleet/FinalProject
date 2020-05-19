import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare(queue='example1')

channel.basic_publish(exchange='',routing_key='example1',body='Example 1')

print("sent 'Example 1'")
channel.close()