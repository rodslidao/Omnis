from threading import Thread
from datetime import time

from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask import Flask, Response, request, session,copy_current_request_context, render_template
from flask_cors import CORS

from engineio.payload import Payload
from threading import Lock
from waitress import serve
from time import sleep

import concurrent.futures as cf
import subprocess
import logging
import random
import json

Payload.max_decode_packets = 500

logging.getLogger('werkzeug').setLevel(logging.ERROR)

class Server(object):
    def __init__(self, app_ip, app_port, app_report_time, app_build_folder, node_info, **kargs):
        """
            ### Parameters
            @app_ip :\n
                - type -> (str)\n
                - ip from socketio connection\n
                    'localhost' or '127.0.0.1' also work.

            @app_port :\n
                - type -> (int)\n
                - port from socketio connection (0000:9999)\n

            @report_time : int
            - After 'n' seconds, server run a background Thread.\n
                Backgorund Thread: report all avaliable threads, and if they are running or not. 

            Raises
            ------
            - ServerCrash
                - [description]
            - ServerLosingConection
                - [description]
            - ServerStopResponse
                - [description]
        """

        self.report_time = app_report_time
        self.buildfolder = app_build_folder
        self.thread_lock = Lock()
        self.port = app_port
        self.thread = None
        self.ip = app_ip
        self.app = Flask(__name__, template_folder = self.buildfolder, static_folder = f"{self.buildfolder}/static")
        self.socketio = SocketIO(self.app, async_mode=None, async_handlers=True, cors_allowed_origins='*')
        CORS(self.app)
        self.process = {}
        self.cameras = kargs.get("app_cameras")
        self.functions = kargs.get("app_functions")
        self.app.config['SECRET_KEY'] = 'secret!'
        self.defineRoutes()
        self.last_ping = 0
        self.running_nodes = node_info

    def start(self):
        print("rodando....")
        self.socketio.run(self.app, host=self.ip, port=self.port)
        print("parou!")


    def addCamera(self, nome, valor):
        self.cameras[nome] = valor
    

    def removeCamera(self, nome):
        self.cameras.pop(nome)


    def addFunction(self, name, function):
        self.functions[name] = function


    def removeFunction(self, name):
        self.functions.remove(name)


    def stop(self):
        serve.graceful_shutdown()


    def stopped(self):
        return self._stop_event.is_set()


    def shutdown_server(self):
        self.socketio.stop()
        return "Server stopped"


    def message_formatter(event='RESPONSE_MESSAGE', command=None, message=None):
        return(event, {"command":command, "data":message})


    def defineRoutes(self):
        app = self.app
        socketio = self.socketio
        def background_thread():
            """Example of how to send server generated events to clients."""
            while True:
                # update = {}
                # for k, v in self.process.items():
                #     update[k] = {"alive": v.is_alive()}
                #print('Updating all clients')
                socketio.emit('NODE_UPDATE',
                           {'data': json.dumps(self.running_nodes, indent=2, ensure_ascii=False)})
                socketio.sleep(self.report_time)

        # @app.route('/')
        # def index():
        #     print('index:', self.buildfolder)
        #     return render_template('index.html', async_mode=socketio.async_mode)

        @socketio.on('call_function')
        def call_function(message):
            _id = random.randint(0, 100000)
            print(f"Nova requisção [{_id}] recebida:")
            if self.functions.get(message.get("command")) is not None:
                with cf.ThreadPoolExecutor() as executor:
                    for r in cf.as_completed([executor.submit(self.functions.get(message.get("command")), message.get("args"))]):
                        print('resultado: ', r.result())
                        emit('RESPONSE_MESSAGE', {'data': message.get("command")+'_sucess'})
            else:
                print(message.get("command")+'_error')
            print(f"Requisição [{_id}] finalizada")


        @socketio.on('TEST_FUNCTION')
        def test(message):
            message = json.loads(message)
            print(message)
            message['name'] = 'xxx'
            emit('RESPONSE_MESSAGE',{'command':'update','parameter':{'operation':message}})
            

        @socketio.on('start_updates')
        def start_updates(*args):
            global thread
            with self.thread_lock:
#                print(f"Recive resquest to starting a threading uptade with args {args}")
                if self.thread is None:
                    #print("updating thread started")
                    thread = socketio.start_background_task(background_thread)
            #emit('RUNNING_NODES', {'data': 'Connected', 'count': 0})


        @socketio.on('connect')
        def connect():
            emit('CONNECTED', {'data': 'Connected'})


        @socketio.on('disconnect')
        def disconnect():
            emit('DISCONNECTED', {'data': 'Connected'})
            print('Client disconnected', request.sid)


        @socketio.on('ping')
        def ping():
            emit('PONG')


        @app.route('/video_feed/<camera>')
        def video_feed(camera):
            try:
                return Response(getattr(self.cameras[camera], "image_stream")(),
                                mimetype='multipart/x-mixed-replace; boundary=frame')
            except KeyError:
                return f"{camera} is offline or disabled"


        @app.route('/kill_<camera>')
        def kill_camera(camera):
            try:
                getattr(self.cameras[camera], "stop")()
                self.removeCamera(camera)
            except KeyError:
                return f"{camera} is offline or disabled"
            return "Kill successfully"
        

        @app.route('/kill_server')
        def kill_server():
            for camera in self.cameras.values():
                camera.stop()
            return self.shutdown_server()