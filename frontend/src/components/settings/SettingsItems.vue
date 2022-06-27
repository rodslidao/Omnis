<template>
  <v-card
    class="mb-4"
    min-height="100px"
    max-width="900px"
    :link="path != ''"
    :to="path"
    outlined
  >
    <div class="d-flex align-center p-4"  @click="expand()">
      <div>
        <div class="d-flex">
          <v-icon v-if="icon" large>mdi-{{ icon }}</v-icon>
          <div class="pl-4 pr-4">
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
      <div>
        <div v-if="!!this.$slots.end">
          <slot name="end"> </slot>
        </div>
        <div v-if="path != ''">
          <v-btn icon :to="path" alt>
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </div>
        <div v-if="!!this.$slots.expand">
          <v-btn icon>
            <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
          </v-btn>
        </div>
      </div>
    </div>
    <v-expand-transition>
      <div v-show="show" v-if="!!this.$slots.expand">
        <v-divider></v-divider>
        <v-card-text>
          <slot name="expand"> </slot>
        </v-card-text>
      </div>
    </v-expand-transition>
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
    select: {
      type: Array,
      default: () => [],
    },
    selected: {
      type: String,
      default: '',
    },
    itemText: {
      type: String,
      default: '',
    },
    itemValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      selectedValue: null,
      show: false,
    };
  },

  methods: {
    expand() {
      if (!!this.$slots.expand) {
        this.show = !this.show;
      }
    },
    change(value) {
      // this.$emit('selected', value);
      this.$emit('update:selected', this.$event.target.checked);
    },
  },
};
</script>

<style scoped>
</style>
