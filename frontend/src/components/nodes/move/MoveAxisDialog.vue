<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <v-form v-model="valid">
            <NodeConfigTitle
              title="Placa"
              description="Selecione a placa que executara o movimento."
            >
              <v-select
                @click="getBoards()"
                :items="boardList"
                v-model="selectedBoard"
                item-text="name"
                return-object
                dense
                required
                :rules="requiredRules"
              ></v-select>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Distancias"
              description="Distancia que a maquina vai se mexer em relação a origem da maquina."
            >
              <div class="mb-n4">
                <div
                  v-for="(axis, index) in axisListCopy"
                  :key="index"
                  class="mb-4 d-flex"
                >
                  <v-checkbox
                    class="mt-0"
                    v-if="axis.name != 'F'"
                    :label="axis.name"
                    v-model="axis.isActive"
                    hide-details
                  ></v-checkbox>
                  <v-text-field
                    v-if="axis.name != 'F'"
                    class="ml-3"
                    v-model="axis.value"
                    type="number"
                    :disabled="!axis.isActive"
                    dense
                    hide-details
                  ></v-text-field>
                </div>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Velocidade"
              description="Defina a Velocidade que todos os eixos irão se deslocar."
            >
              <div class="d-flex">
                <v-checkbox
                  class="mt-0"
                  v-model="axisListCopy.at(-1).isActive"
                  hide-details
                ></v-checkbox>

                <v-text-field
                  class="ml-3"
                  v-model="axisListCopy.at(-1).value"
                  number
                  :disabled="!axisListCopy.at(-1).isActive"
                  type="number"
                  dense
                  hide-details
                ></v-text-field>
              </div>
            </NodeConfigTitle>
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="blue darken-1"
            text
            @click="dialog = false"
            rounded
            large
          >
            Close
          </v-btn>
          <v-btn
            large
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
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    selectedBoard: null,
    boardCopy: null,
    boardList: [],
    Description: '',
    requiredRules: [(v) => !!v || 'Esse campo não pode ficar em branco'],

    rules: {
      positive: (value) => value >= 0 || 'voce só pode inserir numeros',
    },
    valid: false,
    type: null,
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
        this.dialog = true;
        this.init();
      }
    });
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.node.setOptionValue('axisList', this.axisListCopy);
      this.node.setOptionValue('board', this.selectedBoard);
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
      this.boardList = [];
      // make a list of boards name from the response
      this.boardList.push(...response.data.getNodeInfo.data.options);
      if (!this.boardCopy) {
        this.boardList.push(this.boardCopy);
        this.selectedBoard = this.boardCopy;
      }
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
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style scoped>
</style>
