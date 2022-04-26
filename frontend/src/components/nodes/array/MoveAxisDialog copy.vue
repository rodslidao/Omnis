<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card dark>
        <v-card-title >
          <TextEditable
            :text="node.name"
            @changeText="changeName"
          />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <v-form v-model="valid">
            <v-col class="">
              <v-row>
                <v-select
                  :items="boardListName"
                  :label="
                    boardCopy === null ? 'Selecione uma placa' : boardCopy
                  "
                  dense
                  outlined
                ></v-select>
              </v-row>
              <h3>
                Distancia que a maquina vai se mexer em relação a origem da
                maquina.
              </h3>
              <v-row
                v-for="(axis, index) in axisListCopy"
                :key="index"
                class=" mb-4 mt-4"
              >
                <v-checkbox
                  class="mt-0"
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
            </v-col>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false" rounded>
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
import gql from 'graphql-tag';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    boardCopy: null,
    boardListName: [],
    Description: '',

    rules: {
      required: (value) => !!value || 'Required.',
      positive: (value) => value > 0 || 'Positive number required.',
    },
    valid: false,
    type: null,
  }),
  components: {
    TextEditable,
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

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('axisList', this.axisListCopy);
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
      this.init();
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
      // console.log(this.$apollo.store);

      // make a list of boards name from the response
      response.data.getNodeInfo.data.options.forEach((item) => {
        this.boardListName.push(item.name);
      }, this);
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.boardCopy = this.node.getOptionValue('board');
      this.axisListCopy = JSON.parse(
        JSON.stringify(this.node.getOptionValue('axisList'))
      );
      await this.getBoards();
    },

    changeName(data) {
      console.log(data);
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style scoped>
</style>
