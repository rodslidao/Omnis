<template>
  <div class="process">
    <router-view> </router-view>
    <div v-if="$router.currentRoute.name == 'process'">
      <settings-title>{{ $t('settings.process.myProcess') }}</settings-title>
      <settings-items
        v-for="(item, index) in myProcess"
        :key="index"
        :title="$t(item.title)"
        :subtitle="$t(item.subtitle)"
        :icon="item.icon"
        divider-list
        :path="item.path"
      >
      </settings-items>
      <settings-title>{{ $t('settings.process.otherSettings') }}</settings-title>
      <settings-items
        v-for="(item, index) in otherSettings"
        :key="index + 'A'"
        :title="$t(item.title)"
        :subtitle="$t(item.subtitle)"
        :icon="item.icon"
        divider-list
        :path="item.path"
      >
      </settings-items>
    </div>
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';

export default {
  components: { SettingsItems, SettingsTitle },
  data() {
    return {
      actualPath: '',
      myProcess: [
        {
          title: 'settings.process.process.title',
          subtitle: 'settings.process.process.subtitle',
          // icon: 'application-brackets',
          icon: 'cube-send',
          path: 'process/myProcess',
        },
      ],
      otherSettings: [
        {
          title: 'settings.process.nodes.title',
          subtitle: 'settings.process.nodes.subtitle',
          // icon: 'application-brackets',
          icon: 'application',
          path: '/node',
        },
        {
          title: 'settings.process.matrix.title',
          subtitle: 'settings.process.matrix.subtitle',
          // icon: 'application-brackets',
          icon: 'grid',
          path: 'process/matrix',
        },
        {
          title: 'settings.process.objects.title',
          subtitle: 'settings.process.objects.subtitle',
          icon: 'cube',
          path: 'process/object',
          // subItens: [
          //   { title: 'buttons.register', path: 'process/object' },
          //   { title: 'buttons.list', path: 'process/object' },
          // ],
        },
        {
          title: 'settings.process.variables.title',
          subtitle: 'settings.process.variables.subtitle',
          icon: 'variable',
          path: 'process/variable',
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
