<template>
  <div class="process">
    <!-- {{ getUsersList }} -->
    <router-view> </router-view>
    <div v-if="$router.currentRoute.name !== 'registerUser'">
      <settings-title>{{ $t('settings.users.myAccount') }}</settings-title>
      <settings-items
        v-for="(item, index) in myAccount"
        :key="index"
        :title="$t(item.title)"
        :subtitle="$t(item.subtitle)"
        :icon="item.icon"
        :path="item.path"
        ><template v-slot:expand>
          <div class="account-details">
            <div class="d-flex align-center">
              <v-avatar color="primary" size="50">
                <img v-if="user.avatar_image" :src="user.avatar_image" />
                <span v-else class="text-capitalize"
                  >{{ user.first_name.charAt(0)
                  }}{{ user.last_name.split(' ')[0].charAt(0) }}</span
                >
              </v-avatar>
              <!-- <div class="pl-4 pr-4">
              <div class="text-h6 mb-1">
                <span class="text-capitalize">{{ user.first_name }}</span>
                {{ user.last_name }}
              </div>
              <div class="text-body-2">
                {{ user.username }} <span class="mx-2">|</span> {{ user.email }}
              </div>
              <div class="text-body-2">
                {{ $timestampToDate(user.last_access) }}
              </div>
            </div> -->
            </div>
            <div class="d-flex align-center">
              <!-- <v-hover v-slot="{ hover }"> -->
              {{ $t('settings.users.fields.first_name') }}:
              <div class="text-h6 mb-1">
                <span class="text-capitalize">{{ user.first_name }}</span>
                {{ user.last_name }}
              </div>
              <!-- </v-hover> -->
            </div>
          </div>
        </template>
      </settings-items>
    </div>
    <div>
      <div v-if="$router.currentRoute.name !== 'registerUser'">
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

const REMOVE_USER = gql`
  mutation REMOVE_USER($_id: ID!) {
    deleteUser(_id: $_id)
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsTitle,
    SettingsList,
    SettingsListItemUser,
  },
  data() {
    return {
      actualPath: '',
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
      fieldsToIgnore: ['__typename', '_id', 'avatar_image'],
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
  },

  methods: {
    refetch() {
      console.log('entrou');
      this.$apollo.queries.getUsersList.refetch();
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
          this.$alertFeedback(
            this.$t('alerts.deleteSuccess', {
              obj: this.$t('settings.users.user'),
            }),
            'success'
          );
          // this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(
            this.$t('alerts.deleteFail', {
              obj: this.$t('settings.users.user'),
            }),
            'error',
            error
          );
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
