<template>
  <div>
    <div v-if="!isAuth">
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
            <div class="d-flex justify-end">
              <v-btn icon @click="dialog = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
            <v-card-title class="d-flex justify-center">
              <span class="text-h4 my-4">{{ $t('form.singInTitle') }}</span>
            </v-card-title>
            <v-card-text
              class="pa-10 card-text d-flex flex-column justify-center"
            >
              <v-text-field
                name="username"
                v-model="user.username"
                :label="$t('form.username')"
                :placeholder="$t('form.username')"
                required
                outlined
                :dense="dense"
                rounded
                @keyup.enter="authenticateUser()"
              ></v-text-field>

              <div class="d-flex justify-center mb-6">
                <div class="text-h5 text-uppercase">
                  {{ $t('prepositions.or') }}
                </div>
              </div>

              <v-text-field
                class="mb-2"
                name="e-mail"
                v-model="user.email"
                :label="$t('form.email')"
                :placeholder="$t('form.email')"
                required
                outlined
                :dense="dense"
                rounded
              ></v-text-field>

              <v-text-field
                v-model="user.password"
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
                  large
                  rounded
                  :loading="loading && isAuth"
                  @click="authenticateUser()"
                >
                  {{ $t('buttons.login') }}
                </v-btn>
              </div>
            </v-card-text>
            <!-- <v-progress-linear
              color="primary"
              indeterminate
              height="6"
            ></v-progress-linear> -->
          </v-card>
        </v-dialog>
      </v-row>
    </div>
    <div v-else>
      {{ $t('greetings.hello') }},
      <span class="text-h6 text-capitalize"> {{ user.first_name }}</span>
      <v-menu open-on-hover bottom offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn small text icon v-bind="attrs" v-on="on">
            <v-icon>mdi-chevron-down</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item link v-for="(item, index) in items" :key="index">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item link  @click="logoutUser()">
            <v-list-item-title
              ><span>
                {{ $t('buttons.logout') }}
              </span></v-list-item-title
            >
          </v-list-item>
        </v-list>
      </v-menu>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data: () => ({
    dialog: false,
    valid: true,
    loading: false,
    items: [],
    // items: [{ title: 'Click Me' }, { title: 'buttons.logout' }],
    show1: false,
    checkbox: false,
    dense: false,
  }),

  computed: {
    ...mapGetters({
      isAuth: 'auth/isAuth',
      user: 'auth/user',
    }),
  },

  methods: {
    ...mapActions({
      loginUser: 'auth/loginUser',
      logoutUser: 'auth/logoutUser',
    }),

    async authenticateUser() {
      this.loading = true;
      await this.loginUser(this.user);
    },
    rules() {
      return {};
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
