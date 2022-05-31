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
              title="Tempo de espera"
              description="Coloque o tempo em Segundos que esse nó vai esperar antes de passar para o próximo."
            >
              <v-text-field
                required
                class="text-field"
                placeholder="5"
                v-model="delay"
                :rules="requiredRules"
                hint="Tempo em segundos"
              ></v-text-field>
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
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
    pwmRules: [
      (v) => (v >= 0 && v <= 100) || 'Valor tem que ser entre 0 e 100',
    ],
    delayCopy: null,
    delay: 0,
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

  watch: {
    getSerials() {
      if (this.portCopy) {
        console.log('port', this.portCopy);
        this.selectedBoard = this.portCopy.board;
        this.selectedPort = this.portCopy.port;
        this.selectedPortType = this.portCopy.portType;
      } else {
        // eslint-disable-next-line prefer-destructuring
        this.selectedBoard = this.getSerials[0];
      }
    },
  },

  computed: {
    pwmPeriod() {
      return 100 / this.pwmDivision;
    },
  },

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.$refs.form.validate();
      if (
        (this.isAdvanced && this.isValidAdvancedForm) ||
        (!this.isAdvanced && this.isValidSimpleForm)
      ) {
        if (this.isAdvanced) {
          // this.node.setOptionValue('expression', this.advancedExpression);
        } else {
          // eslint-disable-next-line prefer-const
          this.node.setOptionValue('delay', this.delay);
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
      this.delayCopy = this.node.getOptionValue('delay');
      this.delay = this.delayCopy;
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
