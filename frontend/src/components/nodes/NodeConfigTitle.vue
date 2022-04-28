<template>
  <div>
    <v-row class="mb-5">
      <v-col
        ><div class="text-h6 text-uppercase text--darken--primary">
          {{ title }}
        </div>
        <p>{{ description }}</p></v-col
      >
      <v-col>
        <slot></slot>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    description: String,
  },
};
</script>

<style>
</style>