#!/usr/bin/env python3

import asyncio
import json


class SubscriberServerProtocol(asyncio.Protocol):
    """ A Server Protocol listening for subscriber messages """

    def connection_made(self, transport):
        """ Called when connection is initiated """

        self.peername = transport.get_extra_info('peername')
        print('connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        """ The protocol expects a json message containing
        the following fields:

            type:       subscribe/unsubscribe
            channel:    the name of the channel

        Upon receiving a valid message the protocol registers
        the client with the pubsub hub. When succesfully registered
        we return the following json message:

            type:           subscribe/unsubscribe/unknown
            channel:        The channel the subscriber registered to
            channel_count:  the amount of channels registered
        """

        # Receive a message and decode the json output
        recv_message = json.loads(data.decode())

        # Check the message type and subscribe/unsubscribe
        # to the channel. If the action was succesful inform
        # the client.
        if recv_message['type'] == 'subscribe':
            print('Client {} subscribed to {}'.format(self.peername,
                                                      recv_message['channel']))
            send_message = json.dumps({'type': 'subscribe',
                                       'channel': recv_message['channel'],
                                       'channel_count': 10},
                                      separators=(',', ':'))
        elif recv_message['type'] == 'unsubscribe':
            print('Client {} unsubscribed from {}'
                  .format(self.peername, recv_message['channel']))
            send_message = json.dumps({'type': 'unsubscribe',
                                       'channel': recv_message['channel'],
                                       'channel_count': 9},
                                      separators=(',', ':'))
        else:
            print('Invalid message type {}'.format(recv_message['type']))
            send_message = json.dumps({'type': 'unknown_type'},
                                      separators=(',', ':'))

        print('Sending {!r}'.format(send_message))
        self.transport.write(send_message.encode())

    def eof_received(self):
        """ an EOF has been received from the client.

        This indicates the client has gracefully exited
        the connection. Inform the pubsub hub that the
        subscriber is gone
        """
        print('Client {} closed connection'.format(self.peername))
        self.transport.close()

    def connection_lost(self, exc):
        """ A transport error or EOF is seen which
        means the client is disconnected.

        Inform the pubsub hub that the subscriber has
        Disappeared
        """
        if exc:
            print('{} {}'.format(exc, self.peername))


loop = asyncio.get_event_loop()

# Each client will create a new protocol instance
coro = loop.create_server(SubscriberServerProtocol, '127.0.0.1', 10666)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
try:
    server.close()
    loop.until_complete(server.wait_closed())
    loop.close()
except:
    pass