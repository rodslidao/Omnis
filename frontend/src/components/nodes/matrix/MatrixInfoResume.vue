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
            <span class="text-h5">
              <v-icon
                class="ml-4"
                :color="item.color"
                large
                :class="item.rotateIcon ? 'rotate90' : ''"
                >{{ item.icon }}</v-icon
              >
              {{ item.number }}</span
            ><span class="">{{ item.unit }}</span>
            <!-- <v-divider class="ml-2"></v-divider> -->
            <div class="caption ml-3 d-flex justify-center">
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
    origin: Object,
  },

  computed: {
    infoList() {
      const lines = this.slots.qtd.y * this.subdivisions.qtd.y;
      const column = this.slots.qtd.x * this.subdivisions.qtd.x;
      const total = lines * column;

      const list = [
        {
          text: 'Origem X',
          unit: '',
          number: this.origin.x,
          icon: 'mdi-alpha-x-circle',
          color: 'primary',
        },
        {
          text: 'Origem Y',
          unit: '',
          number: this.origin.y,
          icon: 'mdi-alpha-y-circle',
          color: 'primary',
        },
        {
          text: 'Linhas',
          unit: '',
          number: lines,
          icon: 'mdi-table-column',
          color: 'primary',
          rotateIcon: true,
        },
        {
          text: 'Colunas',
          unit: '',
          number: column,
          icon: 'mdi-table-column',
          color: 'primary',
        },

        // {
        //   text: 'Subdivisões',
        //   unit: '',
        //   number: this.subdivisions.qtd.X,
        //   icon: 'mdi-table-settings',
        //   color: 'primary',
        // },
        {
          text: 'Total',
          unit: '',
          number: total,
          icon: 'mdi-table-large',
          color: 'primary',
        },
      ];
      return list;
    },
  },
};
</script>

<style lang="scss" scoped>
p {
  margin-bottom: 0 !important;
}

.rotate90 {
  transform: rotate(90deg);
}
</style>
