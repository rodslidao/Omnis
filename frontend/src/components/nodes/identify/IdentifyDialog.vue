/* eslint-disable max-len */
<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="600px" class="mt-20">
      <v-card dark>
        <v-card-title>
          <TextEditable :text="node.name" @changeText="changeName" />
          <!-- <span class="headline">{{ nodeCopy.name }}</span> -->
        </v-card-title>
        <v-divider></v-divider>
        <v-form ref="form" v-model="isValidForm">
          <v-card-text
            class="pt-6 mb-4 d-flex flex-column justify-center align-center"
          >
            <v-menu v-if="filtersList.length > 0 || isLoading">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  :loading="isLoading"
                  class="mx-2 mb-6"
                  fab
                  dark
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon dark> mdi-plus </v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(item, index) in filtersList"
                  :key="item.title"
                  @click="addItem(index)"
                >
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <div>
              <v-card
                outlined
                v-for="(filter, index) in selectedFilters"
                :key="filter.title"
                class="mb-4"
              >
                <v-card-text class="pt-2 pb-n8">
                  <NodeConfigTitle
                    :title="filter.title"
                    :description="filter.description"
                    class="mb-n6"
                  >
                    <div class="pr-8">
                      <v-text-field
                        label="Máximo"
                        required
                        class="text-field"
                        placeholder="Valor mínimo"
                        type="number"
                        v-model.number="filter.max"
                        :rules="requiredRules"
                        hint="O valor mínimo pode variar de acordo com o tamanho do objeto a ser identificado."
                      ></v-text-field>
                      <v-text-field
                        label="Mínimo"
                        required
                        class="text-field"
                        placeholder="Valor Máximo"
                        type="number"
                        v-model.number="filter.min"
                        :rules="requiredRules"
                        hint="O valor máximo pode variar de acordo com o tamanho do objeto a ser identificado."
                      ></v-text-field>
                    </div>
                    <v-btn icon dark @click="removeItem(index)" class="close">
                      <v-icon dark> mdi-close </v-icon>
                    </v-btn>
                  </NodeConfigTitle>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-form>
        <v-divider></v-divider>
        <v-card-actions>
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
import gql from 'graphql-tag';
import NodeConfigTitle from '@/components/nodes/NodeConfigTitle.vue';
import TextEditable from '@/components/nodes/dialogs/TextEditable.vue';

export default {
  data: () => ({
    dialog: false,
    isValidForm: false,
    isLoading: true,
    requiredRules: [(v) => !!v || 'Campo não pode ficar em branco'],
    filtersCopy: null,
    selectedFilters: [],
    filtersList: [
      // {
      //   key: 'area',
      //   title: 'Área',
      //   description:
      //     'Determine a area minima e máxima para a identificação, ou seja, apenas areas com tamanho entre os valores serão identificadas',
      //   min: 0,
      //   max: 100,
      // },
      // {
      //   key: 'perimeter',
      //   title: 'Perímetro',
      //   description:
      //     'Determine o perímetro minima e máxima para a identificação, ou seja, apenas perímetros com tamanho entre os valores serão identificadas',
      //   min: 0,
      //   max: 100,
      // },
      // {
      //   key: 'diameter',
      //   title: 'Diâmetro',
      //   description:
      //     'Determine o diâmetro mínimo e máxima para a identificação, ou seja, apenas diâmetros com tamanho entre os valores serão identificadas',
      //   min: 0,
      //   max: 100,
      // },
      // {
      //   key: 'vertices',
      //   title: 'Vertices (quinas)',
      //   description:
      //     'Determine o número de vértices minima e máxima para a identificação, ou seja, apenas objetos com número de vértices entre os valores serão identificados',
      //   min: 0,
      //   max: 5,
      // },
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
      if (this.isValidForm) {
        let objFilters = {};

        this.selectedFilters.forEach((filter) => {
          objFilters[filter.key] = filter;
        });

        console.log('selected filter', objFilters);
        this.node.setOptionValue('filters', objFilters);

        this.saveNodeConfig(this.node.id);
        this.dialog = false;

        this.init();
      }
    },

    async getFilterList() {
      this.isLoading = true;
      const response = await this.$apollo.query({
        query: gql`
          query {
            getNodeInfo(node_type: "IdentifyNode") {
              data {
                options
              }
            }
          }
        `,
      });
      // console.log(this.$apollo.store);

      this.filtersList = response.data.getNodeInfo.data.options;
      console.log('filtersList', this.filtersList);

      this.isLoading = false;
    },

    close() {
      this.dialog = false;
    },

    removeItem(index) {
      this.filtersList.push(...this.selectedFilters.splice(index, 1));
    },

    addItem(index) {
      this.selectedFilters.push(...this.filtersList.splice(index, 1));
    },

    async init() {
      this.nodeCopy = { ...this.node };
      this.filtersCopy = this.node.getOptionValue('filters');

      if (!this.filtersCopy) {
        this.getFilterList();
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
.close {
  position: absolute;
  top: 0;
  right: 0;
}
</style>
