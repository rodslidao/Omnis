<template>
  <div class="container mt-6 pr-4">
    <v-form
      v-model="isValid"
      ref="form"
      rounded
      max-width="700px"
      lazy-validation
    >
      <div class="d-flex mb-2">
        <v-text-field
          v-model="user.first_name"
          :rules="[rules().required]"
          :error-messages="errorMessages"
          :label="$t('form.name')"
          :placeholder="$t('form.name')"
          outlined
          required
          name="first_name"
          :dense="dense"
          rounded
        ></v-text-field>
        <v-text-field
          class="ml-2"
          name="last_name"
          v-model="user.last_name"
          :rules="[rules().required]"
          :error-messages="errorMessages"
          :label="$t('form.lastName')"
          :placeholder="$t('form.name')"
          outlined
          required
          :dense="dense"
          rounded
        ></v-text-field>
      </div>
      <div class="d-flex">
        <v-text-field
          class="mb-2"
          name="username"
          v-model="user.username"
          :rules="[rules().required]"
          :error-messages="errorMessages"
          :label="$t('form.username')"
          :placeholder="$t('form.username')"
          required
          outlined
          :dense="dense"
          rounded
        ></v-text-field>
        <v-select
          class="select ml-2"
          rounded
          :label="$t('levels.name')"
          v-model="user.level"
          :rules="[rules().required]"
          dense
          :items="levels"
          outlined
          required
          item-text="text"
          item-value="lang"
        ></v-select>
      </div>

      <v-text-field
        class="mb-2"
        name="e-mail"
        v-model="user.email"
        :rules="[rules().validEmail]"
        :error-messages="errorMessages"
        :label="$t('form.email')"
        :placeholder="$t('form.email')"
        required
        outlined
        :dense="dense"
        rounded
      ></v-text-field>
      <div class="d-flex">
        <v-text-field
          v-model="user.password"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules().required]"
          :type="show1 ? 'text' : 'password'"
          :label="$t('form.password')"
          :hint="$t('form.minCharacters', { count: 8 })"
          rounded
          outlined
          required
          :dense="dense"
          @click:append="show1 = !show1"
        ></v-text-field>
        <v-text-field
          class="ml-4"
          v-model="passwordConfirmation"
          :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules().required, rules().passwordMatch]"
          :type="show2 ? 'text' : 'password'"
          :label="$t('form.confirmPassword')"
          :hint="$t('form.minCharacters', { count: 8 })"
          rounded
          required
          :dense="dense"
          outlined
          @click:append="show2 = !show2"
        ></v-text-field>
      </div>
      <v-divider class="mt-4"></v-divider>
      <div class="d-flex mt-4">
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="singUpUser" rounded>
          {{ $t('buttons.register') }}
        </v-btn>
      </div>
    </v-form>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => ({
    isValid: false,
    dense: true,
    errorMessages: '',
    user: {
      first_name: '',
      last_name: '',
      email: '',
      username: '',
      password: '',
      level: '',
    },
    passwordConfirmation: '',
    formHasErrors: false,
    show1: false,
    show2: true,
  }),

  computed: {
    levels() {
      return [
        {
          text: this.$t('levels.operator'),
          value: 'operator',
        },
        {
          text: this.$t('levels.manager'),
          value: 'manager',
        },
      ];
    },
  },
  // computed: {
  //   form() {
  //     return {
  //       first_name: this.first_name,
  //       last_name: this.last_name,
  //       email: this.email,
  //       username: this.username,
  //       password: this.password,
  //       passwordConfirmation: this.passwordConfirmation,
  //     };
  //   },
  // },

  // watch: {
  //   first_name() {
  //     this.errorMessages = '';
  //   },
  // },

  methods: {
    ...mapActions({
      registerUser: 'auth/registerUser',
    }),
    rules() {
      return {
        required: (value) => !!value || 'Required.',

        min: (v) =>
          v.length >= 8 || this.$t('form.minCharacters', { count: 8 }),
        validEmail: (v) => /.+@.+\..+/.test(v) || this.$t('form.validEmail'),

        passwordMatch: (value) =>
          value === true || this.$t('form.passwordMatch'),
          // value === this.user.password || this.$t('form.passwordMatch'),
      };
    },

    singUpUser() {
      this.$refs.form.validate();
      if (this.isValid) {
        this.registerUser(this.user);
      } else {
        this.formHasErrors = true;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0;
  padding: 0;
}
.select {
  max-width: 20rem;
}
</style>
