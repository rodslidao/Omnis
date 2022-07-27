<template>
  <div v-if="value">
    <v-col class="d-flex flex-wrap justify-center align-center mb-n8">
      <div class="text mr-4">A</div>
      <v-icon dark>mdi-{{value.icon}}</v-icon>
      <div class="ml-4 text">B</div>
    </v-col>
  </div>
</template>

<script>
export default {
  props: ['option', 'node', 'value'],
  data: () => ({}),

  created() {},

  methods: {},
};
</script>
<style lang="scss" scoped>
</style>