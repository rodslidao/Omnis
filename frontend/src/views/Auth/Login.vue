<template>
  <v-row justify="end">
    <v-dialog v-model="dialog" max-width="500px" class="rounded-xl">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          class="mr-4"
          rounded
          dark
          v-bind="attrs"
          v-on="on"
        >
          {{ $t('form.singIn') }}
        </v-btn>
      </template>
      <v-card>
        <v-card-title class="d-flex justify-center">
          <span class="text-h4 my-4">{{ $t('form.singInTitle') }}</span>
        </v-card-title>
        <v-card-text class="pa-10 card-text d-flex flex-column justify-center">
          <v-text-field
            name="username"
            v-model="username"
            :label="$t('form.username')"
            :placeholder="$t('form.username')"
            required
            outlined
            :dense="dense"
            rounded
          ></v-text-field>

          <div class="d-flex justify-center mb-6">
            <div class="text-h5 text-uppercase">
              {{ $t('prepositions.or') }}
            </div>
          </div>

          <v-text-field
            class="mb-2"
            name="e-mail"
            v-model="email"
            :label="$t('form.email')"
            :placeholder="$t('form.email')"
            required
            outlined
            :dense="dense"
            rounded
          ></v-text-field>

          <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show1 ? 'text' : 'password'"
            :label="$t('form.password')"
            rounded
            outlined
            required
            :dense="dense"
            @click:append="show1 = !show1"
          ></v-text-field>
          <div class="d-flex justify-center actions">
            <v-btn
              color="primary"
              class="mr-4"
              large
              rounded
              @click="dialog = false"
            >
              {{ $t('buttons.close') }}
            </v-btn>
            <v-btn
              color="primary"
              large
              rounded
              @click="submit()"
            >
              {{ $t('buttons.login') }}
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    valid: true,
    name: '',
    email: '',
    username: '',
    password: '',
    show1: false,
    checkbox: false,
    dense: false,
  }),

  methods: {
    rules() {
      return {};
    },

    submit() {
      console.log('envia');
      // this.dialog = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.actions {
  width: 100%;
}
.card-text {
  // max-width:500px;
}
</style>>
