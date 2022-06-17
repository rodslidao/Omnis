<template>
  <v-card class="d-flex align-center p-4" min-height="100px" :link="path != ''" :to="path" outlined>
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
      <div v-if="select">
        <v-select
        class="select"
          rounded
          dense
          :items="select"
          v-model="selectedValue"
          @change="$emit('selected', selectedValue)"
          outlined
        ></v-select>
      </div>
      <div v-else>
        <v-btn icon :to="path" alt>
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>
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
    select:{
      type: Array,
      default: [],
    },
    selected: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      selectedValue: null,
    };
  },
};
</script>

<style scoped>
.select {
  max-width: 12rem;
}
</style>