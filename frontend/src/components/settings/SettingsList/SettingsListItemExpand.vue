<template>
  <v-list-item class="v-list-item" :to="path">
    <v-list-item-title class="pl-4">{{ title }}</v-list-item-title>
    <v-list-item-action>
      <v-btn :to="path" icon><v-icon>mdi-chevron-right</v-icon></v-btn>
    </v-list-item-action>
  </v-list-item>
</template>

<script>
export default {
  props: {
    title: String,
    path: String,
  },
};
</script>

<style scoped>
::v-deeper .v-list-item {
  padding-left: 28px;
}
</style>
