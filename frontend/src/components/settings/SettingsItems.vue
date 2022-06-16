<template>
  <v-card class="d-flex align-center p-4" link :to="path" outlined >
    <div>
      <div class="d-flex">
        <v-icon v-if="icon" large>mdi-{{ icon }}</v-icon>
        <div class="ml-4">
          <div class="font-weight-bold">
            {{ title }}
          </div>
          <div class="text-body-2">
            {{ subtitle }}
          </div>
        </div>
      </div>
    </div>
    <v-spacer></v-spacer>
    <div class="">
      <v-btn icon :to="path" alt>
        <v-icon>mdi-chevron-right</v-icon>
      </v-btn>
    </div>
  </v-card>
</template>

<script>
export default {
  props: {
    title: {
      type: String,
      default: '',
    },
    subtitle: {
      type: String,
      default: '',
    },
    icon: {
      type: String,
      default: '',
    },
    path: {
      type: String,
      default: '',
    },
  },
};
</script>

<style>
</style>