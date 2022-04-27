<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-row>
          <div class="text-h3">SE</div>
        </v-row>
        <v-row class="d-flex">
          <v-select
            :items="inputListCopy"
            v-model=""
            item-text="name"
          ></v-select>

          <v-select
            :items="operationObjList"
            v-model="selectedCamera"
            item-text="name"
            
          ></v-select>
          <v-select
            :items="cameraList"
            v-model="selectedCamera"
            item-text="name"
            
          ></v-select>
        </v-row>
        <v-row><div class="text-h3">SE</div> </v-row>

        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="close()" rounded>
            Close
          </v-btn>
          <v-btn
            color="blue darken-1"
            :disabled="!valid"
            text
            @click="save"
            rounded
          >
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import EventBus from '@/event-bus';
import { mapActions } from 'vuex';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    inputListCopy: null,
    operationObjList: [
      {
        name: 'igual',
        icon: 'equal-box',
        value: '==',
      },
      {
        name: 'diferente',
        icon: 'code-not-equal',
        value: '!=',
      },
      {
        name: 'maior',
        icon: 'code-greater-than',
        value: '>',
      },
      {
        name: 'menor',
        icon: 'code-less-than',
        value: '<',
      },
      {
        name: 'maior igual',
        icon: 'code-greater-than-or-equal',
        value: '>=',
      },
      {
        name: 'menor igual',
        icon: 'code-less-than-or-equal',
        value: '<=',
      },
    ],
  }),
  components: {
    TextEditable,
    NodeConfigTitle,
  },

  props: ['option', 'node', 'value'],

  created() {
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        console.log(this.dialog);
        this.dialog = true;
        this.init();
      }
    });
  },

  mounted() {},

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('expression', this.getSelectedCameraObj());
      this.saveNodeConfig(this.node.id);
      this.dialog = false;

      this.init();
    },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.inputListCopy = this.node.getOptionValue('inputList');
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style lang="scss" scoped>
</style>
