<template>
  <div>
    <v-row justify="center">
      <!-- <v-dialog v-model="state.dialogAlert.show" persistent max-width="300"> -->

      <!-- <v-overlay v-model="state.dialogAlert.show"> -->
      <v-overlay>
        <v-alert
          class="alert"
          border="top"
          colored-border
          :type="info.level"
          elevation="3"
        >
          <div class="text-h4 font-weight-thin text-capitalize">
            {{ info.description }}
          </div>

          <div>
            <p class="mt-2">Como Solucionar</p>
            <v-divider></v-divider>
            <p>{{ info.how2solve }}</p>

            <v-divider></v-divider>
          </div>
          <v-row justify="center">
            <v-btn
              x-large
              class="mt-4 mb-3"
              @click="okButtonClick"
            >
              Entendi
              <!-- {{ info.buttonText }} -->
            </v-btn>
          </v-row>
        </v-alert>
      </v-overlay>
    </v-row>
  </div>
</template>

<script>
export default {
  name: 'DialogAlert',
  props: {
    info: {
      type: Object,
      default: () => ({}),
    },
  },

  data() {
    return {};
  },

  methods: {
    okButtonClick() {
      this.$emit('dismiss', true);
      console.log('okButtonClick');
    },
  },

  computed: {},
};
</script>

<style>
.alert {
  max-width: 500px;
}
</style>
