<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="700px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text class="pt-4">
          <!-- <v-btn @click="removeX()"> removeInterface </v-btn> -->
          <v-form v-model="valid">
            <NodeConfigTitle
              title="Placa"
              description="Selecione a placa que executara o movimento."
            >
              <v-select
                :v-if="getNodeInfo"
                :items="getNodeInfo.data.options"
                v-model="selectedBoard"
                item-text="name"
                return-object
                dense
                required
                :rules="requiredRules"
              ></v-select>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Tipo de Ajuste"
              description="Selecione o tipo de ajuste desejado."
            >
              <v-select
                required
                :items="modeList"
                v-model="selectedMode"
                item-text="name"
                return-object
                :rules="requiredRules"
              >
                <template slot="item" slot-scope="data">
                  <v-icon
                    class="mr-3"
                    :class="data.item.rotate ? 'rotate180' : ''"
                    >mdi-{{ data.item.icon }}</v-icon
                  >
                  {{ data.item.name }}
                </template>
              </v-select>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Distancias"
              description="Distancia que a maquina vai se mexer em relação posição atual da maquina."
            >
              <template #description
                ><div class="container">
                  <div class="bar bar--vertical"></div>
                  <div class="bar bar--horizontal"></div></div
              ></template>

              <div class="mb my-4">
                <div
                  v-for="(axis, index) in axisList"
                  :key="index"
                  class="mb-12 d-flex"
                >
                  <v-text-field
                    v-if="axis.name != 'F'"
                    class="ml-3"
                    v-model="axis.min"
                    dense
                    :label="axis.name + ' min.'"
                    hide-details
                  ></v-text-field>
                  <v-text-field
                    v-if="axis.name != 'F'"
                    class="ml-3"
                    v-model="axis.max"
                    dense
                    :label="axis.name + ' max.'"
                    hide-details
                  ></v-text-field>
                </div>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Repetições"
              description="Define quantas vezes o movimento sera repetido"
            >
              <div class="d-flex">
                <v-text-field
                  class="ml-3"
                  v-model.number="repetitions"
                  dense
                  type="number"
                  hide-details
                ></v-text-field>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Divisões"
              description="A cada vez que uma repetição for executada a distancia de X e Y ira ser dividida por esse numero"
            >
               <div class="d-flex">
                <v-text-field
                  class="ml-3"
                  v-model.number="divider"
                  dense
                  type="number"
                  hide-details
                ></v-text-field>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Sentido"
              description="O sequência padrão é do X para o Y do sentido -(Negativo) para o (+)Positivo"
            >
              <div >
                <v-checkbox
                  class="mt-0 mr-4"
                  label="Inverter sentido"
                  v-model="invert.direction"
                  hide-details
                ></v-checkbox>
                <v-checkbox
                  class="mt-0"
                  label="inverter eixo"
                  v-model="invert.axis"
                  hide-details
                ></v-checkbox>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Passo Z"
              :description="
                'Distancia do movimento entre cada repetição. O deslocamento total será de: ' +
                this.zStep * this.repetitions
              "
            >
              <div class="d-flex">
                <v-text-field
                  class="ml-3"
                  v-model.number="zStep"
                  dense
                  type="number"
                  hide-details
                ></v-text-field>
              </div>
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Velocidade"
              description="Defina a Velocidade que todos os eixos irão se deslocar."
            >
              <div class="d-flex">
                <v-checkbox
                  class="mt-0"
                  v-model="velocity.isActive"
                  hide-details
                ></v-checkbox>

                <v-text-field
                  class="ml-3"
                  v-model="velocity.value"
                  :disabled="!velocity.isActive"
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
import TextEditable from '@/components/node/nodes/dialogs/TextEditable.vue';
import NodeConfigTitle from '@/components/node/nodes/NodeConfigTitle.vue';

const GET_BOARDS = gql`
  query getNodeInfo {
    getNodeInfo(node_type: "MoveAxisNode") {
      data {
        options
      }
    }
  }
`;

export default {
  data: () => ({
    dialog: false,
    nodeCopy: null,
    axisListCopy: null,
    selectedBoard: null,
    boardCopy: null,
    repetitions: 1,
    invert: { direction: false, axis: false },
    velocity: { isActive: true, value: 0 },
    zStep: 1,
    divider: 1,
    modeList: [
      { name: 'Cruz', icon: 'plus', description: '' },
      { name: 'ZigZag', icon: 'filter-variant', description: '' },
      { name: 'Cone', icon: 'traffic-cone', description: '', rotate: true },
    ],
    selectedMode: null,
    boardList: [],
    Description: '',
    axisList: [
      { name: 'X', min: -1, max: 1 },
      { name: 'Y', min: -1, max: 1 },
    ],
    requiredRules: [(v) => !!v || 'Esse campo não pode ficar em branco'],
    getNodeInfo: { data: { options: [] } },

    rules: {
      positive: (value) => value >= 0 || 'voce só pode inserir números',
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

  apollo: {
    getNodeInfo: GET_BOARDS,
  },

  watch: {
    getNodeInfo() {
      if (this.boardCopy?.id) {
        this.selectedBoard = this.boardCopy;
      } else {
        // eslint-disable-next-line prefer-destructuring
        this.selectedBoard = this.getNodeInfo.data.options[0];
      }
    },
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    removeX() {
      this.node.addOutputInterface('g');
      this.node.calculate();
    },

    save() {
      this.node.setOptionValue('axisList', this.axisList);
      this.node.setOptionValue('board', this.selectedBoard);
      this.node.setOptionValue('zStep', this.zStep);
      this.node.setOptionValue('repetitions', this.repetitions);
      this.node.setOptionValue('invert', this.invert);
      this.node.setOptionValue('divider', this.divider);
      this.node.setOptionValue('velocity', this.velocity);
      this.saveNodeConfig(this.node.id);
      // this.$store.commit('saveNodeConfig', this.node.id);
      this.dialog = false;
      this.init();
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.axisList = this.node.getOptionValue('axisList');
      this.selectedBoard = this.node.getOptionValue('board');
      this.selectedMode = this.node.getOptionValue('mode');
      this.zStep = this.node.getOptionValue('zStep');
      this.repetitions = this.node.getOptionValue('repetitions');
      // this.invert = this.node.getOptionValue('invert');
      this.divider = this.node.getOptionValue('divider');
      this.velocity = this.node.getOptionValue('velocity');
      // this.axisList = JSON.parse(
      //   JSON.stringify(this.node.getOptionValue('axisList'))
      // );
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style scoped>
.rotate180 {
  transform: rotate(180deg);
}

.container {
  margin: 0 auto;
  width: 100px;
  height: 100px;
  align-items: center;
  position: relative;
}

.bar {
  position: absolute;
  top: 50px;
  height: 5px;
  width: 50px;
  background-color: rgb(255, 255, 255);
}

.bar--horizontal {
  transform: rotate(90deg);
}

@keyframes plus {
  /*   0% {
    transform: rotate(0deg);
  } */
  100% {
    transform: rotate(450deg);
  }
}

@keyframes minus {
  /*   0% {
    transform: rotate(450deg);
  } */
  100% {
    transform: rotate(-360deg);
  }
}

.plus {
  animation: plus 0.5s ease;
  animation-fill-mode: forwards;
}

.minus {
  animation: minus 0.5s ease;
  animation-fill-mode: forwards;
}
</style>
