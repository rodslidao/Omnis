<template>
  <div class="process">
    <!-- {{ getUsersList }} -->
    <router-view> </router-view>
    <div v-if="$router.currentRoute.name == 'users'">
      <settings-title>{{ $t('settings.users.myAccount') }}</settings-title>
      <settings-items
        :title="$t('settings.users.accountsDetails.title')"
        :subtitle="$t('settings.users.accountsDetails.subtitle')"
        icon="account-details"
        ><template v-slot:expand>
          <div class="account-details ma-6" v-if="user">
            <div class="d-flex align-center">
              <div class="d-flex flex-column align-center">
                <v-avatar color="primary" size="50">
                  <img v-if="user.avatar_image" :src="user.avatar_image" />
                  <!-- <span v-else class="text-uppercase">{{ getInitials }}</span> -->
                </v-avatar>
                <v-chip class="mt-2" small>
                  {{ $t('levels.' + user.level) }}
                </v-chip>
              </div>
              <div class="pl-4 pr-4">
                <div class="text-h6 mb-1">
                  <span class="text-capitalize">{{ user.first_name }}</span>
                  {{ user.last_name }}
                </div>
                <div class="text-body-2">
                  {{ user.email }}
                </div>
                <div class="text-body-2">
                  {{ user.username }}
                </div>
                <div class="text-body-2">
                  {{ $timestampToDate(user.last_access) }}
                </div>
              </div>
              <v-spacer></v-spacer>
              <v-btn icon @click="updateUser(user)"
                ><v-icon>mdi-pencil</v-icon></v-btn
              >
              <edit-user
                v-if="editDialog"
                :user-info="userToEdit"
                @edit-user="edit"
                @cancel-event="editDialog = false"
              ></edit-user>
            </div>
          </div>
        </template>
      </settings-items>
      <div>
        <settings-title>{{
          $t('settings.users.otherAccounts')
        }}</settings-title>
        <settings-items
          v-for="(item, index) in items"
          :key="index"
          :title="$t(item.title)"
          :subtitle="$t(item.subtitle)"
          :icon="item.icon"
          :path="item.path"
        >
          <template
            v-if="item.title == 'settings.users.listUsers.title'"
            v-slot:expand
          >
            <settings-list
              :items="getUsersList"
              item-search="first_name"
              :fields-ignore="fieldsToIgnore"
            >
              <template #itemList="itemList">
                <settings-list-item-user
                  @remove-user="remove"
                  @edit-user="updateUser"
                  :user="itemList.data"
                ></settings-list-item-user>
                <v-divider></v-divider>
              </template>
            </settings-list>
          </template>
        </settings-items>
      </div>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import { mapGetters } from 'vuex';
import { LIST_USER } from '@/graphql';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsListItemUser from '@/components/settings/SettingsList/SettingsListItemUser.vue';
import EditUser from '@/components/settings/EditUser.vue';

const REMOVE_USER = gql`
  mutation REMOVE_USER($_id: ID!) {
    deleteUser(_id: $_id)
  }
`;

const UPDATE_USER = gql`
  mutation UPDATE_USER(
    $_id: ID!
    $username: String
    $password: String
    $email: String
    $first_name: String
    $last_name: String
    $level: String
  ) {
    updateUser(
      _id: $_id
      input: {
        username: $username
        password: $password
        email: $email
        first_name: $first_name
        last_name: $last_name
        level: $level
      }
    )
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsTitle,
    SettingsList,
    SettingsListItemUser,
    EditUser,
  },
  data() {
    return {
      actualPath: '',
      editDialog: false,
      userToEdit: {},
      myAccount: [
        {
          title: 'settings.users.accountsDetails.title',
          subtitle: 'settings.users.accountsDetails.subtitle',
          icon: 'account-details',
        },
      ],
      items: [
        {
          title: 'settings.users.registerUser.title',
          subtitle: 'settings.users.registerUser.subtitle',
          icon: 'account-plus',
          path: 'users/register-user',
        },
        {
          title: 'settings.users.listUsers.title',
          subtitle: 'settings.users.listUsers.subtitle',
          icon: 'account-multiple',
        },
      ],
      fieldsToIgnore: ['__typename', '_id', 'avatar_image', {}, []],
      datailAccountFields: ['first_name', 'last_name'],
      // getUsersList: [
      //   {
      //     first_name: 'Arthur',
      //     last_name: 'dawd',
      //     email: 'rodrig@gmail.com',
      //     last_access: '20120150',
      //     level: 'operador',
      //     avatar_image: 'https://i.pravatar.cc',
      //   },
      //   {
      //     first_name: 'Rodrigo',
      //     last_name: 'dawd',
      //     email: 'rodrig@gmail.com',
      //     last_access: '20120150',
      //     level: 'operador',
      //     avatar_image: 'https://i.pravatar.cc',
      //   },
      //   {
      //     first_name: 'henrique',
      //     last_name: 'dawd',
      //     email: 'rodrig@gmail.com',
      //     last_access: '20120150',
      //     level: 'operador',
      //     avatar_image: 'https://i.pravatar.cc',
      //   },
      // ],
    };
  },

  computed: {
    ...mapGetters({
      user: 'auth/user',
    }),
    getInitials() {
      return (
        this.user?.first_name.charAt(0) +
        this.user?.last_name.split(' ').at(-1).charAt(0)
      );
    },
  },

  methods: {
    updateUser(user) {
      console.log(user);
      this.userToEdit = user;
      this.editDialog = true;
    },

    async remove(_id) {
      await this.$apollo
        .mutate({
          mutation: REMOVE_USER,
          variables: {
            _id,
          },
        })

        .then(() => {
          // Result
          this.$apollo.queries.getUsersList.refetch();
          this.$alertFeedback(this.$t('alerts.deleteSuccess'), 'success');
          // this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(this.$t('alerts.deleteFail'), 'error', error);
          // We restore the initial user input
        });
    },

    async edit(user) {
      console.log('input', user);
      await this.$apollo
        .mutate({
          mutation: UPDATE_USER,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: user._id,
            username: user.username,
            password: user.password,
            email: user.email,
            first_name: user.first_name,
            last_name: user.last_name,
            level: user.level,
          },
        })

        .then(() => {
          // Result
          this.$apollo.queries.getUsersList.refetch();
          this.$alertFeedback(this.$t('alerts.updateUserSuccess'), 'success');
          this.editDialog = false;
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(this.$t('alerts.updateUserFail'), 'error', error);
          // We restore the initial user input
        });
    },
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    getUsersList: LIST_USER,
  },

  // created() {
  //   this.actualPath = this.$router.currentRoute.path;
  //   console.log(this.$router.currentRoute);
  // },
};
</script>

<style lang="scss" scoped>
</style>
