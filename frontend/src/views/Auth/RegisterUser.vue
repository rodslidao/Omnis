<template>
  <div class="pt-4">
    <v-form v-model="isValid" ref="form" rounded max-width="700px">
      <div class="d-flex mb-2">
        <v-text-field
          v-model="firstName"
          :rules="[rules().required]"
          :error-messages="errorMessages"
          :label="$t('form.name')"
          :placeholder="$t('form.name')"
          outlined
          name="first_name"
          :dense="dense"
          rounded
        ></v-text-field>
        <v-text-field
          class="ml-2"
          name="last_name"
          v-model="lastName"
          :rules="[rules().required]"
          :error-messages="errorMessages"
          :label="$t('form.lastName')"
          :placeholder="$t('form.name')"
          outlined
          :dense="dense"
          rounded
        ></v-text-field>
      </div>
      <div class="d-flex">
        <v-text-field
          class="mb-2"
          name="username"
          v-model="username"
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
          v-model="selectedLevel"
          dense
          :items="levels"
          outlined
          item-text="text"
          item-value="lang"
        ></v-select>
      </div>

      <v-text-field
        class="mb-2"
        name="e-mail"
        v-model="email"
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
          v-model="password"
          :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules().required, rules().passwordMatch]"
          :type="show1 ? 'text' : 'password'"
          :label="$t('form.password')"
          :hint="$t('form.minCharacters', { count: 8 })"
          rounded
          outlined
          :dense="dense"
          @click:append="show1 = !show1"
        ></v-text-field>
        <v-text-field
          class="ml-4"
          v-model="passwordConfirmation"
          :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
          :rules="[rules().required, rules().passwordMatch]"
          :type="show2 ? 'text' : 'password'"
          :label="$t('form.password')"
          :hint="$t('form.minCharacters', { count: 8 })"
          rounded
          :dense="dense"
          outlined
          @click:append="show2 = !show2"
        ></v-text-field>
      </div>
      <v-divider class="mt-12"></v-divider>
      <v-btn text> Cancel </v-btn>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click="submit"> Submit </v-btn>
    </v-form>
  </div>
</template>

<script>
import { managers } from 'socket.io-client';
export default {
  data: () => ({
    isValid: false,
    dense: true,
    errorMessages: '',
    firstName: '',
    lastName: '',
    email: '',
    username: '',
    password: '',
    passwordConfirmation: '',
    formHasErrors: false,
    show1: false,
    show2: true,
    selectedLevel: '',
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
  //       firstName: this.firstName,
  //       lastName: this.lastName,
  //       email: this.email,
  //       username: this.username,
  //       password: this.password,
  //       passwordConfirmation: this.passwordConfirmation,
  //     };
  //   },
  // },

  // watch: {
  //   firstName() {
  //     this.errorMessages = '';
  //   },
  // },

  methods: {
    rules() {
      return {
        required: (value) => !!value || 'Required.',

        min: (v) =>
          v.length >= 8 || this.$t('form.minCharacters', { count: 8 }),
        validEmail: (v) =>
          !v ||
          /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) ||
          this.$t('form.validEmail'),

        passwordMatch: (value) =>
          value === this.passwordConfirmation || this.$t('form.passwordMatch'),
      };
    },

    resetForm() {
      this.errorMessages = [];
      this.formHasErrors = false;

      Object.keys(this.form).forEach((f) => {
        this.$refs[f].reset();
      });
    },

    submit() {
      this.$refs.form.validate();
      if (this.isValid) {
        console.log('Form is valid');
        // this.$store.dispatch('registerUser', this.form).then(() => {
        //   this.$router.push('/auth/login');
        // });
      } else {
        this.formHasErrors = true;
      }
    },
  },
};
</script>

<style scoped>
.select {
  max-width: 20rem;
}
</style>