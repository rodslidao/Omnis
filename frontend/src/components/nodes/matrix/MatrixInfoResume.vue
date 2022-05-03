<template>
  <div>
    <v-row>
      <div class="pr-5 pl-3 d-flex justify-space-around statistics">
        <div
          class="d-flex justify-space-around"
          v-for="item in infoList"
          :key="item.text"
        >
          <div>
            <span class="text-h5 text--primary">
              <v-icon class="ml-4" :color="item.color" large>{{
                item.icon
              }}</v-icon>
              {{ item.number }}</span
            ><span class="text--secondary">{{ item.unit }}</span>
            <!-- <v-divider class="ml-2"></v-divider> -->
            <div class="text--secondary caption ml-3 d-flex justify-center">
              {{ item.text }}
            </div>
          </div>
        </div>
      </div>
    </v-row>
  </div>
</template>

<script>
export default {
  // mixins: [mixins],
  data: () => ({}),

  props: {
    subdivisions: Object,
    slots: Object,
  },

  methods: {},

  computed: {
    infoList: () => {
      console.log('infoList');
      const lines = this.slots.qtd.Y * this.subdivisions.qtd.Y;
      const column = this.slots.qtd.X * this.subdivisions.qtd.X;
      const total = lines * column;
      console.log(lines);
      console.log(column);

      const list = [
        {
          text: 'Colunas',
          unit: '',
          number: column,
          icon: 'mdi-chart-timeline-variant',
          color: 'blue lighten-2',
        },
        {
          text: 'Linhas',
          unit: '',
          number: lines,
          icon: 'mdi-check',
          color: 'green lighten-2',
        },
        {
          text: 'Subdivisões',
          unit: '',
          number: this.subdivisions.qtd.X,
          icon: 'mdi-close',
          color: 'red lighten-2',
        },
        {
          text: 'Total',
          unit: '',
          number: total,
          icon: 'mdi-timer-outline',
          color: 'blue lighten-2',
        },
      ];
      return list;
    },
  },
};
</script>

<style lang="scss" scopped>
p {
  margin-bottom: 0 !important;
}
</style>
