/* eslint-disable max-len */
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="650px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-form ref="form" v-model="isValidSimpleForm" v-if="!isAdvanced">
          <v-card-text class="simple-mode">
            <NodeConfigTitle
              title="Placa"
              description="Selecione a placa que executara o movimento."
            >
              <v-select
                :items="getSerials"
                v-model="selectedBoard"
                item-text="name"
                return-object
                required
                :loading="$apollo.queries.getSerials.loading"
                :rules="requiredRules"
              ></v-select>
            </NodeConfigTitle>

            <NodeConfigTitle
              v-if="selectedBoard"
              title="Porta"
              description="Selecione a porta que será utilizada."
            >
              <v-select
                @click="updatePorts()"
                :items="getPorts"
                v-model="selectedPort"
                item-text="name"
                return-object
                dense
                :loading="$apollo.queries.getPorts.loading"
                :rules="requiredRules"
                required
              ></v-select>

              <!-- <div class="caption">Porta: {{selectedPort.port}}</div> -->
            </NodeConfigTitle>
            <NodeConfigTitle
              title="Tipo de Porta"
              description="Selecione o tipo de porta que será utilizada dependendo do uso"
              v-if="selectedPort"
            >
              <v-radio-group v-model="selectedPortType" row>
                <v-radio label="Liga" :value="true"></v-radio>
                <v-radio label="Desliga" :value="false"></v-radio>
                <v-radio label="PWM" value="pwm"></v-radio>
              </v-radio-group>
            </NodeConfigTitle>
            <NodeConfigTitle
              v-if="selectedPortType == 'pwm'"
              title="PWM"
              description="O PWM é utilizado para controlar rotação de um motor, intensidade de brilho de uma lâmpada,
               Seu valor varia de 0% a 100%"
              ><v-slider
                v-model="pwmValue"
                thumb-label="always"
                max="100"
                min="0"
                thumb-color="primary"
              ></v-slider>
              <div class="pwm d-flex flex-row">
                <div
                  class="wrapper d-flex flex-row"
                  v-for="pulse in pwmDivision"
                  :key="pulse"
                  :style="'width: ' + pwmPeriod + '%'"
                >
                  <div class="high" :style="'width: ' + pwmValue + '%'"></div>
                  <div
                    class="low"
                    :style="'width: ' + (100 - pwmValue) + '%'"
                  ></div>
                </div>
              </div>
            </NodeConfigTitle>
          </v-card-text>
        </v-form>
        <v-form v-else ref="form" v-model="isValidAdvancedForm">
          <v-card-text class="pt-8"> </v-card-text>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <!-- <v-checkbox v-model="isAdvanced" label="Modo Avançado"></v-checkbox> -->
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1 " text @click="close()" large rounded>
            fechar
          </v-btn>
          <v-btn color="blue darken-1" text @click="save" rounded large>
            salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import EventBus from '@/event-bus';
import gql from 'graphql-tag';
import { mapActions } from 'vuex';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    nodeCopy: null,
    dialog: false,
    isValidAdvancedForm: false,
    isValidSimpleForm: false,
    isAdvanced: false,
    pwmDivision: 4,
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
    pwmRules: [
      (v) => (v >= 0 && v <= 100) || 'Valor tem que ser entre 0 e 100',
    ],
    portCopy: null,
    selectedPort: null,
    boardCopy: null,
    boardListCopy: [],
    boardList: [],
    selectedBoard: null,
    selectedPortType: null,
    pwmValue: 0,
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

  computed: {
    pwmPeriod() {
      return 100 / this.pwmDivision;
    },
  },

  apollo: {
    getSerials: {
      query: gql`
        query {
          getSerials {
            data {
              _id
              name
            }
          }
        }
      `,
      update(data) {
        return data.getSerials.data;
      },
    },

    getPorts: {
      query: gql`
        query getNodeInfo($kwargs: JSON) {
          getNodeInfo(node_type: "IoNode", kwargs: $kwargs) {
            data {
              options
            }
          }
        }
      `,
      variables() {
        return {
          // eslint-disable-next-line no-underscore-dangle
          kwargs: { board: this.selectedBoard._id },
        };
      },
      update(data) {
        console.log(data.getNodeInfo.data.options);
        return data.getNodeInfo.data.options;
      },
    },
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    updatePorts() {
      this.$apollo.queries.getPorts.refetch();
    },

    save() {
      this.$refs.form.validate();
      if (
        (this.isAdvanced && this.isValidAdvancedForm) ||
        (!this.isAdvanced && this.isValidSimpleForm)
      ) {
        if (this.isAdvanced) {
          // this.node.setOptionValue('expression', this.advancedExpression);
        } else {
          let port = this.selectedPort;

          port.selectedBoard = this.selectedBoard;

          switch (this.selectedPortType) {
            case true:
              port.pwm = 255;
              break;
            case false:
              port.pwm = 0;
              break;
            case 'pwm':
              port.pwm = this.pwmValue;
              break;
            default:
          }

          this.node.setOptionValue('port', port);
        }
        this.saveNodeConfig(this.node.id);
        this.dialog = false;

        this.init();
      }
    },
    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.portListCopy = this.node.getOptionValue('port');
      if (this.node.getOptionValue('port')) {
        this.selectedBoard = this.node.getOptionValue('port').board;
        this.selectedPort = this.node.getOptionValue('port');
        this.selectedPortType = this.node.getOptionValue('port').pwm;
      }
    },

    changeName(data) {
      this.node.name = data;
      this.saveNodeConfig(this.node.id);
    },
  },
};
</script>
<style lang="scss" scoped>
.pwm {
  width: 100%;
  height: 50px;
  // border: 2px solid #e0e0e0;

  .wrapper {
    height: 100%;
    width: val(width);

    .high {
      height: 100%;
      border: 2px;
      border-top-style: solid;
      border-right-style: solid;
      border-bottom-style: none;
      border-left-style: solid;
    }
    .low {
      height: 100%;
      border: 2px;
      border-bottom-style: solid;
      width: fit-content;
    }
  }
}
</style>
