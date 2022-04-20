<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ nodeCopy.name }}</span>
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pb-1 pt-5">
          <v-form v-model="valid">
            <v-col>
              <v-row>
                <v-text-field
                  label="Name"
                  :rules="[rules.required]"
                  v-model="nodeCopy.name"
                  outlined
                  dense
                  hide-details
                ></v-text-field>
              </v-row>
              <v-row
                v-for="(axis, index) in axisListCopy"
                :key="index"
                class="pt-5"
              >
                <v-checkbox
                  :label="axis.name == 'F' ? 'Velocidade' : axis.name"
                  v-model="axis.isActive"
                  hide-details
                ></v-checkbox>
                <v-text-field
                  class="ml-3"
                  v-model="axis.value"
                  number
                  :disabled="!axis.isActive"
                  outlined
                  dense
                  hide-details
                ></v-text-field>
              </v-row>
              <v-row>
                <v-overflow-btn
                  class="my-2"
                  :items="boardList"
                  :label="boardCopy"
                  editable
                  item-value="text"
                ></v-overflow-btn>
              </v-row>
            </v-col>
            <v-col cols="6"> </v-col>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Close
          </v-btn>
          <v-btn color="blue darken-1" :disabled="!valid" text @click="save">
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
import gql from 'graphql-tag';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    boardCopy: null,
    boardList: [
      'Arduino',
      'Raspberry Pi',
      'ESP32',
      'ESP8266',
      'BeagleBone Black',
    ],

    rules: {
      required: (value) => !!value || 'Required.',
      positive: (value) => value > 0 || 'Positive number required.',
    },
    valid: false,
    type: null,
  }),

  props: ['option', 'node', 'value'],
  created() {
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        this.dialog = true;
        this.init();
      }
    });
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('axisList', this.axisListCopy);
      this.node.name = this.nodeCopy.name;
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
    },

    async getBoards() {
      const response = await this.$apollo.query({
        query: gql`
          query {
            getNodeInfo(node_type: "MOVEMENT") {
              data {
                options
              }
            }
          }
        `,
      });
      console.log(this.$apollo.store);
      this.boardList = response.data.getNodeInfo.data.options;
      console.log(this.boardList);
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.boardCopy = this.node.getOptionValue('board');
      this.axisListCopy = JSON.parse(
        JSON.stringify(this.node.getOptionValue('axisList'))
      );
      await this.getBoards();
    },
  },
};
</script>
