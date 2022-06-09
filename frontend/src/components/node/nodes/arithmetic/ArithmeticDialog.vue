/* eslint-disable max-len */
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="750px">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-form ref="form" v-model="isValidSimpleForm" v-if="!isAdvanced">
          <v-card-text class="simple-mode">
            <NodeConfigTitle
              title="Conta"
              description="Insira a operação que será realizada em cima das variáveis, a saida recebera o resultado da conta."
            >
              <v-select
                required
                :items="operationObjList"
                v-model="selectedInputOperation"
                item-text="name"
                return-object
                :rules="requiredRules"
              >
                <template slot="item" slot-scope="data">
                  <v-icon class="mr-3">mdi-{{ data.item.icon }}</v-icon>
                  {{ data.item.name }}
                </template>
              </v-select>
              <v-col class="d-flex flex-wrap justify-center align-center">
                <div class="text mr-4 ml-4">A</div>
                <v-icon large>mdi-{{ selectedInputOperation.icon }}</v-icon>
                <div class="ml-4 text">B</div>
              </v-col>
            </NodeConfigTitle>
          </v-card-text>
        </v-form>
        <v-form v-else ref="form" v-model="isValidAdvancedForm">
          <v-card-text class="pt-8">
            <NodeConfigTitle
              title="Expressão"
              description="Aqui você poderá fazer uma requisição customizada usando as outras letras como 'C' e 'D'"
            >
              <v-text-field
                required
                class="text-field"
                placeholder="((a+10)/c)"
                v-model="advancedExpression"
                :rules="requiredRules"
                hint=" potencia: ^ | raiz quadrada: sqrt | arredondar: round | Ignorar decimal: trunc | logaritmo base 10: log | exponencial: exp | seno: sin | cosseno: cos | tangente: tan | pi: pi"
              ></v-text-field
            ></NodeConfigTitle>
          </v-card-text>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
          <v-checkbox v-model="isAdvanced" label="Modo Avançado"></v-checkbox>
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
import NodeConfigTitle from '@/components/node/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/node/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    isValidAdvancedForm: false,
    isValidSimpleForm: false,
    isAdvanced: false,
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
    expressionCopy: null,
    arithmeticSelectedCopy: null,
    operationObjList: [
      {
        name: 'soma',
        icon: 'plus-box',
        signal: '+',
        hint: 'A + B',
        category: 'functions',
      },
      {
        name: 'subtração',
        icon: 'minus-box',
        signal: '-',
        hint: 'A - B',
        category: 'functions',
      },
      {
        name: 'multiplicação',
        icon: 'multiplication-box',
        signal: '*',
        hint: 'A * B',
        category: 'functions',
      },
      {
        name: 'divisão',
        icon: 'division-box',
        signal: '/',
        hint: 'A / B',
        category: 'functions',
      },
    ],
    selectedInputOperation: '',
    advancedExpression: '',
    onFailureValue: '',
    onSuccessValue: '',
  }),
  components: {
    TextEditable,
    NodeConfigTitle,
  },

  props: ['option', 'node', 'value'],

  computed: {},

  created() {
    this.init();
    EventBus.$on('OPEN_SETTINGS', (nodeId) => {
      if (nodeId === this.node.id) {
        this.dialog = true;
        this.init();
      }
    });
  },

  mounted() {},

  methods: {
    ...mapActions('node', ['saveNodeConfig']),

    save() {
      this.$refs.form.validate();
      if (
        (this.isAdvanced && this.isValidAdvancedForm) ||
        (!this.isAdvanced && this.isValidSimpleForm)
      ) {
        if (this.isAdvanced) {
          this.node.setOptionValue('expression', this.advancedExpression);
        } else {
          let expression = '';
          expression = `A${this.selectedInputOperation.signal}B`;
          this.node.setOptionValue(
            'ArithmeticSelected',
            this.selectedInputOperation
          );
          this.node.setOptionValue('expression', expression);
        }

        this.saveNodeConfig(this.node.id);
        this.dialog = false;
        // this.engine.calculate();

        this.init();
      }
    },

    addMdi(icon) {
      return `mdi-${icon}`;
    },

    getOperationPropertyValueByName(property) {
      const result = this.operationObjList.find(
        (operation) => operation.value === this.selectedInputOperation
      );

      if (result) {
        console.log(result[property]);
        return result[property];
        // return `mdi-${result.icon}`;
      }
      return '';
    },

    close() {
      this.dialog = false;
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.expressionCopy = this.node.getOptionValue('expression');
      this.arithmeticSelectedCopy =
        this.node.getOptionValue('ArithmeticSelected');
      if (this.arithmeticSelectedCopy) {
        this.selectedInputOperation = this.arithmeticSelectedCopy;
      }

      if (this.expressionCopy) {
        this.advancedExpression = this.expressionCopy;
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
$text-size: 3rem;
$sub-text-size: 2rem;

.simple-mode {
  .sub-text {
    font-size: $text-size;
    color: rgb(63, 63, 63);
    line-height: 3rem;
  }
  .text {
    font-size: $text-size;
    line-height: 4rem;
    color: rgb(233, 233, 233);
  }
  .text-field {
    max-width: 5.5em;
    font-size: $text-size;
  }

  //   .middle-select {
  //     max-width: 25em;
  //     width: fit-content;
  //   }
  //variáveis que são acessadas dentro do componente pelo ::v-deep
  //   .v-text-field ::v-deep {
  //     align-self: center;
  //     padding-top: 0;

  //     .v-select__selections {
  //       font-size: $text-size;
  //       line-height: 1.1em;
  //     }

  // input {
  //   font-size: $text-size;
  //   font-weight: 100;
  //   text-transform: capitalize;
  //   max-height: 50px;
  // }

  // label {
  //   font-size: $text-size;
  // }
  // .v-text-field button {
  //   font-size: $text-size;
  // }
  //   }
}
</style>
