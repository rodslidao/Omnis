<template>
  <section>
    <div class="d-flex">
      <v-dialog v-model="dialog" width="600px"><gcode></gcode></v-dialog>
      <div class="d-flex flex-wrap head">
        <div class="ml-auto mb-2 text-h4">
          Monitor Serial
          <v-btn text icon x-small @click="dialog = true">
            <v-icon>mdi-information</v-icon>
          </v-btn>
        </div>
        <v-spacer></v-spacer>
        <v-select
          class="ml-4"
          placeholder="Selecione a placa"
          :items="('data' in getSerials ? getSerials.data : [])"
          v-model="selectedSerial"
          item-text="name"
          return-object
          dense
          :loading="!getSerials.data"
        ></v-select>
      </div>
      <div class="ml-auto pa-2" outlined tile small>
        <div>
          <!-- <v-row class="d-flex">
            <v-btn v-model="toggle_exclusive" rounded class="mr-auto">
              <v-btn>
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              <v-btn>
                <v-icon>mdi-arrow-right</v-icon>
              </v-btn>
              <v-btn @click="clearSerialMonitor()">
                <v-icon>mdi-trash-can-outline</v-icon>
              </v-btn>
              <v-btn-toggle>
                <v-icon>mdi-format-letter-case-upper</v-icon>
              </v-btn-toggle>
            </v-btn>
          </v-row> -->
        </div>
      </div>
    </div>
    <div class="mb-4">
      <v-chip
        class="mr-2 mb-2"
        v-for="item in shortcutsList"
        :key="item.text"
        link
        @click="sendChip(item.sendDirect, item.command)"
        >{{ item.text }}{{ item.sendDirect ? '' : '+' }}</v-chip
      >
    </div>
    <v-divider></v-divider>
    <div class="textArea pt-2" ref="textArea">
      <div v-for="item in serialMonitor" :key="item.index">
        <v-row v-if="item.sent" class="item pl-2">
          <v-col class="col-2 d-flex justify-end">
            <v-chip class="pa-2" color="orange" outlined small chip>
              Enviada
            </v-chip>
          </v-col>
          <v-col class="message">
            <div class="pa-1">
              <p v-for="msg in item.message" :key="msg.index">{{ msg }}</p>
            </div>
          </v-col>
        </v-row>

        <v-row v-else class="item pl-2">
          <v-col class="col-2 d-flex justify-end">
            <v-chip class="pa-2" color="blue" outlined small chip>
              Recebida
            </v-chip>
          </v-col>
          <v-col class="message">
            <div class="pa-1">
              <p v-for="msg in item.message" :key="msg.index">{{ msg }}</p>
            </div>
          </v-col>
        </v-row>
      </div>
    </div>

    <v-divider></v-divider>
    <div class="d-flex flex-nowrap">
      <v-text-field
        filled
        dense
        rounded
        v-model="message"
        class="pt-6 d-flex align-center"
        ref="input"
        hide-details
        single-line
        type="text"
        v-on:keyup.enter="selectedSerial ? send() : ''"
        required
      >
        <v-btn
          class="mb-2"
          text
          icon
          small
          slot="append-outer"
          @click="send()"
          :disabled="!selectedSerial || !message"
        >
          <v-icon> mdi-send </v-icon>
        </v-btn>
        <!-- botão de upercase -->
        <div slot="prepend" class="d-flex align-center pb-2">
          <v-btn
            class="mr-2"
            text
            icon
            small
            color="primary"
            @click="upperCase = !upperCase"
          >
            <v-icon v-if="upperCase">mdi-format-letter-case-upper</v-icon>
            <v-icon v-else color="grey">mdi-format-letter-case</v-icon>
          </v-btn>
          <!-- fim botão de upercase -->

          <v-btn
            class="mr-2"
            text
            icon
            small
            color="greu"
            slot="prepend"
            @click="leftItem()"
          >
            <v-icon> mdi-arrow-left </v-icon>
          </v-btn>

          <v-btn
            class=""
            text
            icon
            small
            color="grey"
            slot="prepend"
            @click="rightItem()"
          >
            <v-icon> mdi-arrow-right </v-icon>
          </v-btn>
        </div>
      </v-text-field>
    </div>
  </section>
</template>

<script>
import gql from 'graphql-tag';
import Gcode from '@/components/settings/Gcode.vue';

const SEND_SERIAL = gql`
  mutation ($id: ID!, $msg: String!) {
    sendSerial(_id: $id, payload: $msg) {
      last_value_received
      date
    }
  }
`;

const GET_SERIALS = gql`
  query {
    getSerials {
      data {
        _id
        name
      }
    }
  }
`;

export default {
  components: { Gcode },
  name: 'SerialMonitor',
  data() {
    return {
      upperCase: true,
      dialog: false,
      message: null,
      scrolled: false,
      sendCommandList: [],
      selectedItemCommandList: null,
      selectedSerial: null,
      receivedData: {},
      serialMonitor: [
        // {
        //   hour: 1611539081,
        //   sent: true,
        //   message: ['ok', 'eaee', 'M117'],
        // },
      ],

      shortcutsList: [
        {
          text: 'G0',
          command: 'G0 X ',
          sendDirect: false,
        },
        {
          text: 'G90 - Absoluto',
          command: 'G90 ',
          sendDirect: true,
        },
        {
          text: 'G91 - Relativo',
          command: 'G91 ',
          sendDirect: true,
        },
        {
          text: 'G28 E',
          command: 'G28 E',
          sendDirect: true,
        },
        {
          text: 'M114 - Posição Atual',
          command: 'M114',
          sendDirect: true,
        },
      ],
    };
  },

  watch: {
    receivedData(newData) {
      console.log('new', newData.data);
      if (newData.data.sendSerial.last_value_received) {
        this.serialMonitor.push({
          hour: Math.floor(Date.now() / 1000),
          sent: false,
          message: newData.data.sendSerial.last_value_received,
        });
        this.scrollToBottom();
      }
    },
    getSerials() {
      // eslint-disable-next-line prefer-destructuring
      this.selectedSerial = this.getSerials.data[0];
    },
  },

  apollo: {
    getSerials: {
      query: GET_SERIALS,
      // nextFetchPolicy: 'network-only',
      // update function to update selected
      // update: (data) => selectedSerial = data.getSerials.data[0],
    },
  },

  methods: {
    async send() {
      if (this.message !== '') {
        let msg;
        // eslint-disable-next-line no-underscore-dangle
        const id = this.selectedSerial._id;

        if (this.upperCase) {
          msg = this.message.toUpperCase();
        } else {
          msg = this.message;
        }

        this.serialMonitor.push({
          hour: Math.floor(Date.now() / 1000),
          sent: true,
          message: [msg],
        });

        await this.$apollo
          .mutate({
            mutation: SEND_SERIAL,
            variables: {
              id,
              msg,
            },
          })

          .then((data) => {
            // Result
            console.log('return', data);

            this.receivedData = data;

            this.sendCommandList.push(this.message);
            this.selectedItemCommandList = this.sendCommandList.length;
            this.clearMessage();

            // this.$alertFeedback(
            //   `Comando enviado para a placa ${this.selectedSerial.name}!`,
            //   'success'
            // );
          })

          .catch((error) => {
            // Error
            this.isLoading = false;
            console.error(
              'Não foi possível enviar comando para a placa  \n',
              error,
            );
            this.$alertFeedback(
              `Não foi possível enviar comando para a placa ${this.selectedSerial.name}!`,
              'error',
              error,
            );

            // We restore the initial user input
          });
      }
      setTimeout(() => this.scrollToEnd(), 200);
      this.setFocus();
    },

    setFocus() {
      this.$refs.input.focus();
    },

    sendChip(sendDirect, command) {
      this.message = command;

      if (sendDirect) {
        this.send();
      } else {
        this.setFocus();
      }
    },

    scrollToEnd() {
      // console.log("scroll");
      const container = this.$refs.textArea;
      container.scrollTop = container.scrollHeight;
      container.scrollIntoView({ behavior: 'smooth' });
    },

    clearMessage() {
      this.message = '';
    },

    clearSerialMonitor() {
      // console.log(this.serialMonitor);
      this.serialMonitor.length = 0;
    },

    leftItem() {
      // console.log(this.sendCommandList.length)
      if (
        this.sendCommandList.length >= this.selectedItemCommandList &&
        this.selectedItemCommandList >= 1
      ) {
        console.log(this.sendCommandList.length);

        // decrementa a lista
        this.selectedItemCommandList -= 1;
        this.message = this.sendCommandList[this.selectedItemCommandList];
        // console.log(this.sendCommandList[this.selectedItemCommandList - 1]);
      }
    },

    rightItem() {
      // console.log(this.sendCommandList.length + "  " + this.selectedItemCommandList);

      if (this.selectedItemCommandList < this.sendCommandList.length) {
        this.selectedItemCommandList += 1;
        this.message = this.sendCommandList[this.selectedItemCommandList - 1];
        // console.log(this.sendCommandList[this.selectedItemCommandList - 1]);
      }
    },
  },
};
</script>

<style scoped lang="scss">
.head {
  width: 100%;
  .text-h4 {
    min-width: 100px;
  }
}
.textArea {
  // max-height: 500px;
  height: 300px;
  overflow-y: scroll !important;
  flex-direction: column-reverse;
  /* border: solid 1px rgb(196, 196, 196); */

  .message {
    // background-color: rgb(248, 248, 248);
    border-radius: 0.5em;
    padding: 6px;
    margin: 0.2em;

    p {
      font-size: 0.8em;
      margin: 0;
    }
  }
}
</style>
