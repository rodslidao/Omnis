<template>
  <div class="process">
    <!-- {{ getUsersList }} -->
    <router-view> </router-view>
    <settings-title>{{ $t('settings.users.myAccount') }}</settings-title>
    <settings-items
      v-for="(item, index) in myAccount"
      :key="index"
      :title="$t(item.title)"
      :subtitle="$t(item.subtitle)"
      :icon="item.icon"
      :path="item.path"
      ><template v-slot:expand> oi </template>
    </settings-items>
    <div>
      <settings-title>{{ $t('settings.users.otherAccounts') }}</settings-title>
      <div v-if="$router.currentRoute.name !== 'registerUser'">
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
import { LIST_USER } from '@/graphql';

import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsListItemUser from '@/components/settings/SettingsList/SettingsListItemUser.vue';

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
