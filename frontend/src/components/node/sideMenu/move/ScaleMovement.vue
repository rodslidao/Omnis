<template>
  <div class="mt-10">
    <side-menu-title
      tooltip="Define a escala de movimento, quando apertar pra movimentar o eixo"
      tooltipBottom
    >
      Escala de movimento
    </side-menu-title>
    <v-btn-toggle v-model="stepSelected" dark mandatory dense>
      <v-btn v-for="(steps, index) in stepsList" :key="index"
        >{{ steps.value }}
      </v-btn>
    </v-btn-toggle>
  </div>
</template>

<script>
import SideMenuTitle from '../SideMenuTitle.vue';

export default {
  components: { SideMenuTitle },
  data() {
    return {
      stepSelected: '1',
      stepsList: [
        {
          name: '0,01',
          value: '0.01',
        },
        {
          name: '0,1',
          value: '0.1',
        },
        {
          name: '1',
          value: '1',
        },
        {
          name: '10',
          value: '10',
        },
        {
          name: '100',
          value: '100',
        },
      ],
    };
  },
  watch: {
    stepSelected() {
      const msg = {
        context: 'movementScale',
        value: this.stepsList[this.stepSelected].value,
      };
      this.$emit('send', msg);
    },
  },
};
</script>

<style>
</style>
