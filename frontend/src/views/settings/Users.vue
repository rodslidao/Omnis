<template>
  <div class="process">
    <router-view> </router-view>
    <settings-items
      v-for="(item, index) in items"
      :key="index"
      :title="$t(item.title)"
      :subtitle="$t(item.subtitle)"
      :icon="item.icon"
      :path="item.path"
    ></settings-items>
  </div>
</template>

<script>
import SettingsItems from '../../components/settings/SettingsItems.vue';

export default {
  components: { SettingsItems },
  data() {
    return {
      actualPath: '',
      items: [
        {
          title: 'settings.users.registerUser.title',
          subtitle: 'settings.users.registerUser.subtitle',
          icon: 'account-plus',
          path: 'users/register-user',
        },
      ],
    };
  },

  // created() {
  //   this.actualPath = this.$router.currentRoute.path;
  //   console.log(this.$router.currentRoute);
  // },
};
</script>

<style lang="scss" scoped>
</style>
