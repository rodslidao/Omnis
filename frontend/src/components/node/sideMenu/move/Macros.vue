<template>
  <div class="mt-10">
    <side-menu-title tooltip="Ações Rápidas" tooltipBottom>
      Ações automáticas
    </side-menu-title>
    <div class="mb-4">
      <v-btn
        class="mr-2 mb-2 px-8"
        v-for="item in (getDevicesList ? getDevicesList : shortcutsList)"
        v-show="item.visible"
        :key="item.text"
        rounded
        dark
        large
        @click="sendCommand(item.command)"
        ><v-icon left> mdi-{{ item.icon }} </v-icon> {{ item.text }}</v-btn
      >
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SideMenuTitle from '../SideMenuTitle.vue';

const GET_MACROS_LIST = gql`
  query {
    getMacrosList {
      _id
      name
      command
      icon
      visible
    }
  }
`;

export default {
  components: { SideMenuTitle },
  data() {
    return {
      stepSelected: 3,
      shortcutsList: [
        {
          text: 'Zona Segura',
          visible: 'true',
          command: 'G28',
          icon: 'shield-home',
        },
      ],
    };
  },

  apollo: {
    getMacrosList: {
      query: GET_MACROS_LIST,
    },
  },

  methods: {
    sendCommand(command) {
      const msg = {
        context: 'macroAction',
        value: command,
      };
      this.$emit('send', msg);
    },
  },
};
</script>

<style>
</style>
