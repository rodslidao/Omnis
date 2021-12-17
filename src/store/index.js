// import { constants } from "fs";
import Vue from "vue";
import Vuex from "vuex";
import serverJson from "../../engine/data/json/config/editable/server.json";
Vue.use(Vuex);

//lista de coisas q eu posso pedir pro back
export const actions = {
  STOP_REASONS_LIST_REQUEST: "stopReasonsListRequest",
  STOP_REASON_RESPONSE: "stopReasonsResponse",
  SHUTDOWN_RASPBERRY: "shutdown_raspberry",
  START_CAMERA_STREAM: "startCameraStream",
  RESTART_RASPBERRY:"restart_raspberry",
  RESTART_PROCESS: "restartProcess",
  START_AUTOCHECK: "startAutoCheck",
  UPDATE_ASSEMBLY: "updateAssembly",
  GENERATE_ERROR: "generateError",
  RESTORE_CAMERA: "restoreCamera",
  SERIAL_MONITOR: "serialMonitor",
  PAUSE_PROCESS: "pauseProcess",
  START_PROCESS: "startProcess",
  UPDATE_CAMERA: "updateCamera",
  UPDATE_FILTER: "updateFilter",
  UPDATE_SLIDER: "updateSlider",
  POPUP_TRIGGER: "popupTigger",
  REQUEST_JSON: "requestJson",
  RESTORE_JSON: "restoreJson",
  STOP_PROCESS: "stopProcess",
  UPDATE_USERS: "updateUsers",
  LOG_REQUEST: "logRequest",
  MODIFY_JSON: "modifyJson",
  SAVE_CAMERA: "saveCamera",
  PARAFUSA: "sendParafusa",
  SEND_GCODE: "sendGcode",
  SHOW_POPUP: "showPopup",
  START_SCAN: "startScan",
};

const store = new Vuex.Store({
  //estado do dado
  
  state: {
    operation: {
      name: "",
      type: "",
      panel: "",
      timeSeconds: 0,
      total: 1,
      right: 10,
      wrong: 5,
      placed: 0,
      finished: false,
      running:false,
      played: false,
      started: false,
      onlyCorrectParts: false,
    },
    stopSuccess:false,

    localTimer: {
      currentSeconds: null,
      minutes: null,
      seconds: null,
    },

    allJsons: {
      "AVI": {
        "code": 113,
        "description": "Auto verificiação iniciou",
        "listed": false,
        "type": "info"
      },
    },

    progress: 5.1,
    started: false,
    playing: false,
    paused: true,
    finished: false,
    stoped: true,

    idVar: null,

    connectionStatus: null,
    connectionStatusList: {
      connecting: "Tentando se conectar ao servidor...",
      connected: "Conectando com sucesso!",
      closed: "A conexão foi encerrada!",
      error: "Não conseguimos conectar ao servidor!, certifique-se que ele está ligado",
    },

    ws_message: {
      command: "",
      parameter: "",
    },

    dialogAlert: {
      show: false,
      code: 0,
      description: "",
      type: "error",
      button_text: "None",
      button_action: "None"
    },

    isConnecting: false,
    isConnected: false,
    autoCheckComplete: false,
    scanConnectorsComplete: false,

    production: {
      A:{
        avarage:{
          avarage_total: [
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0,
              40
          ],
          avarage_rigth: [
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0,
              40
          ],
          avarage_wrong: [
              0.0,
              0.0,
              0.0,
              0.0,
              0.0,
              0,
              0
          ]
        },
        info:{
          name: "A",
          partNumber: 0,
          date: "11/11/2021, 14:59:38",
          avarage_size: 7,
          date_format: "%m/%d/%Y, %H:%M:%S"
        },
        today:{
          total: 50,
          rigth: 50,
          wrong: 0
        },
        total:{
          total: 90,
          rigth: 90,
          wrong: 0
        }
      }
  },

    log: [
      {
        code: Number,
        description: String,
        type: String,
        date: Number,
      }
    ],

    serialMonitor: [
      // {hour: 1611539081 ,sent: true, message:["ok","eaee","M117"]},
    ],

    selectedFilter: "hole",

    configuration: {
      logged: false,
      allJsons: {
        // name: 'mike',
        // age: 23,
        // phone: '419988756100',
        // address: ['AAA C1', 'BBB C2']
      },

      cameraList: [
        {
          name: "Camera Furação",
          cameraId: 0,
          filter: "hole",
        },
        {
          name: "Camera de Validação",
          cameraId: 2,
          filter: "screw",
        },
      ],

      health: {

        listOfSystem: [
          {
            hardware: "CPL",
            status: "Online ",
            conected: true
          }

        ]
      },

      assembly: {
        listOfParts: [
          {
            index: 0,
            partName: "Peça Menor",
            frontImg: "estribo-quadrado-front.png",
            perspectiveImg: "estribo-quadrado.png",
            listed: true,
            listOfHoles: [
              {
                index: 1,
                checkboxPosition: {
                  top: "8.3%",
                  left: "50%",
                },
                mount: true,
              },
              {
                index: 2,
                checkboxPosition: {
                  top: "25%",
                  left: "83%",
                },
                mount: true,
              },
              {
                index: 3,
                checkboxPosition: {
                  top: "57%",
                  left: "83%",
                },
                mount: true,
              },
              {
                index: 4,
                checkboxPosition: {
                  top: "72%",
                  left: "50%",
                },
                mount: true,
              },
              {
                index: 5,
                checkboxPosition: {
                  top: "25%",
                  left: "11%",
                },
                mount: true,
              },
              {
                index: 6,
                checkboxPosition: {
                  top: "57%",
                  left: "11%",
                },
                mount: true,
              },
            ],
          },
          {
            index: 1,
            partName: "Peça Maior",
            frontImg: "estribo-retangular-front.png",
            perspectiveImg: "estribo-retangular.png",
            listed: true,
            listOfHoles: [
              {
                index: 1,
                checkboxPosition: {
                  top: "0",
                  left: "50%",
                },
                mount: true,
              },
              {
                index: 2,
                checkboxPosition: {
                  top: "18%",
                  left: "83%",
                },
                mount: true,
              },
              {
                index: 3,
                checkboxPosition: {
                  top: "55%",
                  left: "83%",
                },
                mount: true,
              },
              {
                index: 4,
                checkboxPosition: {
                  top: "72%",
                  left: "50%",
                },
                mount: true,
              },
              {
                index: 5,
                checkboxPosition: {
                  top: "18%",
                  left: "11%",
                },
                mount: true,
              },
              {
                index: 6,
                checkboxPosition: {
                  top: "55%",
                  left: "11%",
                },
                mount: true,
              },
            ],
          },
        ],
      },

      informations: {
        ip: serverJson.ip,
        connectionId: 123456,
        port: serverJson.port,
        //portStream: serverJson.configuration.informations.portStream,
        users: {
          logged: false,
          levelList: [
            {
              name: String,
              level: Number,
              componentsProhibitedAccess: Array
            },
          ],
          userList: [
            {
              name: String,
              id: String,
              lastAcess: Number,
              level: String
            },
          ],
        },
        version: {
          backend: "0",
          frontend: "0", //fazer sistema para pegar automaticamente
          marlin: "0",
        },
        machine: {
          limits: {
            xMin: null,
            yMin: null,
            zMin: null,
            aMin: null,
            bMin: null,
            xMax: null,
            yMax: null,
            zMax: null,
            aMax: null,
            bMax: null,
          },
          maxFeedrate: {
            xMax: null,
            yMax: null,
            zMax: null,
            aMax: null,
            bMax: null,
          },
          defaultPosition: {
            pegaTombador: {
              X: 2,
              Y: 49,
              Z: null,
              E: 0
            },

            analisaFoto: {
              X: 80,
              Y: 9,
              Z: null,
              E: null
            },

            descarteErrado: {
              X: 230,
              Y: 0,
              Z: null,
              E: null
            },

            descarteCerto: {
              X: 0,
              Y: 0,
              Z: null,
              E: 0
            },

            camera0Centro: {
              X: 74.5,
              Y: 7.5,
              Z: null,
              E: null
            },

            camera1Centro: {
              X: 230,
              Y: 0,
              Z: null,
              E: null
            },

            parafusadeiraCentro: {
              X: 240,
              Y: 16,
              Z: null,
              E: null
            },
          },
        },
      },
      statistics: {
        stopReasons: [{
          code: 998,
          description: "Parada para ajuste técnico",
          listed: true,
          type: "info",
          button_text: "Entendi",
          button_action: "popupResponseSolve"
          }],
        stopReasonsList: [
          { "000": "Maquin ok" },
        ],
      },
      camera: {
        process: null,
        filters: {
          hole: {
            name: "hole",
            area: [10, 20],
            gradient: {
              color: "#a02727",
              color2: "#e261ae",
            },
            hsv: {
              hue: [2, 50],
              sat: [0, 250],
              val: [30, 50],
            }
          }

        },
      },
    },
    socketMessage:"nada",
    messages: {},
    messagesOrder: []
  },

    mutations: {

    // use the vue instace methods 'socket' to emit events to the server
  

    SOCKET_disconnect(state) {
      console.log("The server conection has been closed");
      state.isConnected = false;
      state.isConnecting = false;
      state.connectionStatus = state.connectionStatusList.closed;
      console.log(state.isConnected);
      
    },

    SOCKET_connect: (state) => {
      console.log("The server connection has been established");
      state.isConnecting = true;
      state.isConnected = true;
      state.connectionStatus = state.connectionStatusList.connected;
      console.log(state.isConnected);
    },

    SOCKET_reconnect_attempt: (state) => {
      console.log("Reconnecting to the server...");
    },

    SOCKET_reconnect: (state) => {
      console.log("Reconnecting...");
    },


    SOCKET_connect_error: (state) => {
      console.log("Não foi possivel se conecar com o servidor");
      state.connectionStatus = state.connectionStatusList.error;
      state.isConnected = false;
      state.isConnecting = false;
      console.log(state.isConnected);
    },
    
    
    SOCKET_RESPONSE_MESSAGE : (state, message) => {
      console.log("%c Recebido:", 'color: #51a4f7')
      console.log(message);
      store.commit("RUN_COMMAND", message);
      // state = Object.assign(state, message.data); //unifica os objetos
    },

    RUN_COMMAND: (state, message) => {
      switch (message.command) {
        case actions.START_AUTOCHECK + "_success":
          console.log("autocheck");
          state.autoCheckComplete = true;
          break;

        case actions.START_SCAN + "_success":
          state.scanConnectorsComplete = true;
          console.log("scan conector");
          // code block
          break;

        case actions.START_PROCESS + "_success":
          store.commit("START2");
          console.log("START process");
          // code block
          break;

        case actions.PAUSE_PROCESS + "_success":
          store.commit("START2");
          console.log("PAUSE process");
          // code block
          break;

        case actions.RESTART_PROCESS + "_success":
          store.commit("RESTART");
          console.log("RESTART process");
          // code block
          break;

        case actions.STOP_PROCESS + "_success":
          store.commit("STOP")
          console.log("STOP Process")
          // code block
          break;

        case "update":
          state = Object.assign(state, message.parameter);
          console.log("update")
          console.log(state.configuration)
          // code block
          break;

        case "error":
          console.log("Back-end constata falha: ")
          console.log(message.parameter)
          state.dialogAlert.show = true
          state.dialogAlert.description = message.parameter.description
          state.dialogAlert.type = message.parameter.type
          state.dialogAlert.code = message.parameter.code
          state.dialogAlert.button_action = message.parameter.button_action
          state.dialogAlert.button_text = message.parameter.button_text

          // code block
          break;

        case actions.SERIAL_MONITOR + "_response":
          //confere se a ultimo intem da lista é uma msg recebida, se sim.. 
          var lastArrayItem = state.serialMonitor[state.serialMonitor.length - 1]

          if (lastArrayItem.sent == false) {
            lastArrayItem.message.push(message.parameter)
          } else {
            state.serialMonitor.push({ hour: Math.floor(Date.now() / 1000), sent: false, message: [message.parameter] })
          }

          // state = Object.assign(state, message.parameter);
          console.log("Update Serial Monitor Received");
          // code block
          break;

        default:
          console.log("default");
        // code block
      }
    },

    SCAN_COMPLETE_CHANGE: (state) => (state.scanConnectorsComplete = false),

    SEND_MESSAGE: function (state, payload){
      state.ws_message.command = payload.command;
      state.ws_message.parameter = payload.args;
      this._vm.$socket.emit('call_function', payload);
      console.log("recebi:", this);
      console.log("%c Enviado:", 'color: #bada55');
      console.log(payload)
      // console.log(JSON.stringify({'command':command, 'args':args, 'kwargs':kwargs}, null, 2));
    },

    START: (state) => {
      state.paused = !state.paused;

      if (state.localTimer.currentSeconds == null) {
        state.localTimer.currentSeconds = state.operation.timeSeconds;

        state.localTimer.minutes = Math.floor(state.operation.timeSeconds / 60);
        state.localTimer.seconds = state.operation.timeSeconds % 60;
      }

      console.log(state.localTimer.currentSeconds);

      if (state.paused == false && state.localTimer.currentSeconds > 0) {
        state.idVar = setInterval(() => {
          console.log("current time: " + state.localTimer.currentSeconds);

          //diminui em 1 seg
          if (state.localTimer.currentSeconds > 0) {
            state.localTimer.currentSeconds--;
          }

          //caucula a porcentagem
          if (state.localTimer.currentSeconds == null) {
            state.localTimer.currentSeconds = state.operation.timeSeconds;
          }

          state.progress = Math.floor(
            (state.localTimer.currentSeconds * 100) /
            state.operation.timeSeconds
          );

          //se o tempo for zero, interronpe o loop
          if (state.localTimer.currentSeconds == 0) {
            state.finished = true;
            clearInterval(state.idVar);
          }
        }, 1000);
      } else {
        state.paused = true;
        clearInterval(state.idVar);
      }
    },

    START2: (state) => {
      // state.playing = true
      // state.started = true
      // state.stoped = false
      state.stopSuccess = false
    },

    RESTART(state) {
      // state.localTimer.currentSeconds = null;
      // state.progress = 5.1;
      // state.paused = true;
      // state.finished = false;
      // state.started = false;
      state.stopSuccess = false
    },

    STOP(state) {
      // state.localTimer.currentSeconds = 0;
      // state.progress = 5.1;
      // state.playing = false
      // state.paused = true;
      // state.finished = false;
      // // state.started = false;
      // state.stoped = true
      state.stopSuccess = true
    },

    
  },
  //trata os dados
  getters: {
    operation: (state) => state.operation,
    minutes: (state) =>
    (state.localTimer.minutes = Math.floor(
      state.localTimer.currentSeconds / 60
    )),
    seconds: (state) =>
      (state.localTimer.seconds = state.localTimer.currentSeconds % 60),
    progress: (state) => 100 - state.progress,
    state: (state) => state,
  },
  //conecta com o banco e o commit chama o mutation
  actions: {
    startConnection: (context) => context.commit("SOCKET_CONNECT"),
    startStatusChage: (context) => context.commit("START"),
    restart: (context) => context.commit("RESTART"),
    stop: (context) => context.commit("STOP"),
  },
});

export { store };
