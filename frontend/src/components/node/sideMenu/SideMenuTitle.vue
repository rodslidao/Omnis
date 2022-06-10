<template>
  <div class="text-overline text--white d-flex">
    <slot></slot>
    <v-tooltip
      v-if="tooltip"
      open-delay="550"
      :color="color"
      :max-width="tooltipMaxWidth"
      :bottom="tooltipBottom"
      :top="tooltipTop"
      :right="tooltipRight"
      :left="tooltipLeft"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          class="ml-1"
          dark
          v-bind="attrs"
          v-on="on"
          small
          :color="tooltipIconColor"
          >mdi-information-outline</v-icon
        >
      </template>
      <span>{{ tooltip }}</span>
    </v-tooltip>
  </div>
</template>

<script>
export default {
  props: {
    color: {
      type: String,
      default: 'grey darken-4',
    },
    tooltipMaxWidth: {
      type: String,
      default: '300px',
    },
    tooltipBottom: Boolean,
    tooltipTop: Boolean,
    tooltipRight: Boolean,
    tooltipLeft: Boolean,
    tooltipIconColor: {
      type: String,
      default: 'grey darken-1',
    },
    tooltip: String,
  },
};
</script>

<style>
</style>