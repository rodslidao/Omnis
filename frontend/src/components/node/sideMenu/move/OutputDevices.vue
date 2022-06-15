/* eslint-disable no-underscore-dangle */
<template>
  <div class="mt-10">
    <side-menu-title> controle de dispositivos </side-menu-title>
    <div
      v-for="(device, index) in getDevicesList"
      :key="index"
      v-on.once="generateVariables(device.name)"
    >
      <div v-if="device.visible">
        <div v-if="device.type === 'switch'" class="d-flex align-end mb-6">
          <v-switch
            v-model="device.pwm"
            color="primary"
            false-value="0"
            :prepend-icon="'mdi-' + device.icon"
            hide-details
            v-haptic
            true-value="255"
            @change="sendPwm(device.name, device.pwm)"
          ></v-switch>
          <div
            class="
              switch-label
              text-h6
              grey--text
              text--lighten-2
              ml-2
              d-flex
              align-center
            "
          >
            {{ device.name }}
          </div>
        </div>
      </div>
      <div v-if="device.type === 'slider'" class="pr-4 pt-4">
        <div
          class="text-h6 grey--text text--lighten-2 mr-6 d-flex align-center"
        >
          <v-icon small class="mr-3">mdi-{{ device.icon }}</v-icon>
          {{ device.name }}
        </div>
        <div class="d-flex">
          <v-slider
            class="slider"
            v-model="device.range.selected"
            :min="device.range.min"
            :max="device.range.max"
            v-haptic
            @mouseup="sendCommand(device.range.selected, device.id)"
          >
            <template v-slot:prepend>
              <v-icon @click="decrement(index)"> mdi-minus </v-icon>
            </template>

            <template v-slot:append>
              <v-icon @click="increment(index)"> mdi-plus </v-icon>
            </template>
          </v-slider>
          <div>
            <v-text-field
              class="text-field ml-2"
              v-if="variableList[index].manualMode"
              v-model="device.range.selected"
              label="Coordenada que deseja mover"
              single-line
              dense
              type="number"
              v-on:keyup.enter="
                (variableList[index].manualMode = false),
                  sendCommand(device.range.selected, device.id)
              "
              @blur="
                (variableList[index].manualMode = false),
                  sendCommand(device.range.selected, device.id)
              "
              autofocus
            ></v-text-field>
            <div
              v-else
              class="
                slider-value
                text-h5
                grey--text
                text--lighten-2 text-end
                mr-6
              "
              @click="variableList[index].manualMode = true"
            >
              {{ device.range.selected }}
            </div>
          </div>
        </div>
      </div>
      <v-divider></v-divider>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SideMenuTitle from '../SideMenuTitle.vue';

const GET_DEVICES_LIST = gql`
  query {
    getDevicesList {
      _id
      name
      command
      board
      port
      icon
      type
      visible
      pwm
      range
    }
  }
`;

export default {
  components: { SideMenuTitle },
  data() {
    return {
      variableList: [],
      outputDevices: [
        {
          id: 1,
          name: 'Garra',
          port: '1',
          icon: 'hand-okay',
          type: 'switch',
          visible: true,
          value: null,
        },
        {
          id: 2,
          name: 'Cilindro',
          port: '2',
          icon: 'rotate-right-variant',
          type: 'switch',
          visible: true,
          value: null,
        },
        {
          id: 3,
          name: 'LED',
          port: '3',
          icon: 'lightbulb',
          type: 'slider',
          visible: true,
          value: {
            min: 0,
            max: 100,
            selected: 0,
          },
        },
      ],
    };
  },

  apollo: {
    getDevicesList: {
      query: GET_DEVICES_LIST,
    },
  },

  methods: {
    increment(index) {
      this.getDevicesList[index].range.selected += 1;
      this.sendCommand(
        this.getDevicesList[index].range.selected,
        this.getDevicesList[index]._id
      );
    },

    decrement(index) {
      this.getDevicesList[index].range.selected -= 1;
      this.sendCommand(
        this.getDevicesList[index].range.selected,
        this.getDevicesList[index]._id
      );
    },

    sendCommand(data, index) {
      const msg = {
        context: 'outputDevices',
        id: this.getDevicesList[index]._id,
        pwm: data,
      };
      this.$emit('send', msg);
    },

    generateVariables(name) {
      if (this.variableList.length !== this.outputDevices.length) {
        const variable = {
          name,
          manualMode: false,
        };
        this.variableList.push(variable);
        // console.log(this.variableList);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.slider-value {
  width: 4rem;
}

.switch-label {
  line-height: 1.3;
}
.v-text-field ::v-deep input {
  font-size: 1.3em;
}

.text-field {
  width: 4rem;
}

/* remove arrows from text-field */
.text-field::v-deep input[type='number'] {
  -moz-appearance: textfield;
}

.text-field::v-deep input::-webkit-outer-spin-button,
.text-field::v-deep input::-webkit-inner-spin-button {
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}
</style>
