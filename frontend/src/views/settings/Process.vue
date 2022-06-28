<template>
  <div class="process">
    <router-view :key="$route.path"> </router-view>
    <div v-if="$router.currentRoute.name == 'process'">
      <settings-items
        v-for="(item, index) in items"
        :key="index"
        :title="$t(item.title)"
        :subtitle="$t(item.subtitle)"
        :icon="item.icon"
        divider-list
        :path="item.path"
      >
        <template v-slot:expand>
          <div v-for="(subItem, index) in item.subItens" :key="index">
            <settings-list-item-expand
              :title="$t(subItem.title)"
              :path="subItem.path"
            ></settings-list-item-expand>
            <!-- <v-list>
            <v-list-item>
              <v-list-item-title>{{ subItem.title }}</v-list-item-title>
              <v-list-item-action>
                <v-btn :to="subItem.path" icon
                  ><v-icon>mdi-chevron-right</v-icon></v-btn
                >
              </v-list-item-action>
            </v-list-item>
          </v-list> -->
          </div>
        </template>
      </settings-items>
    </div>
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemExpand from '@/components/settings/SettingsList/SettingsListItemExpand.vue';

export default {
  components: { SettingsItems, SettingsTitle, SettingsListItemExpand },
  data() {
    return {
      actualPath: '',
      items: [
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
          subItens: [
            { title: 'buttons.register', path: 'process/matrix-add' },
            { title: 'buttons.list', path: 'process/matrix-list' },
          ],
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
          title: 'settings.process.process.title',
          subtitle: 'settings.process.process.subtitle',
          icon: 'variable',
          subItens: [
            { title: 'Cadastrar', path: 'process/matrix-add' },
            { title: 'Listar', path: 'process/matrix-list' },
          ],
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
