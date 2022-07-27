<template>
  <div class="system">
    <settings-title>{{
      $t('settings.system.languageAndData.name')
    }}</settings-title>
    <router-view> </router-view>
    <settings-items
      v-for="(item, index) in items"
      :key="index"
      :title="$t(item.title)"
      :subtitle="$t(item.subtitle)"
      :icon="item.icon"
      :path="item.path"
    >
      <template v-slot:end>
        <v-select
          class="select"
          rounded
          v-model="lang"
          dense
          :items="item.select"
          @change="changeLanguage(lang)"
          outlined
          item-text="text"
          item-value="lang"
        ></v-select>
      </template>
    </settings-items>
    {{ items[0].selected }}
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';

export default {
  components: { SettingsItems, SettingsTitle },
  data() {
    const lang = localStorage.getItem('lang') || 'en';
    return {
      actualPath: '',
      lang,
      items: [
        {
          title: 'settings.system.languageAndData.exhibitionLanguage.title',
          subtitle:
            'settings.system.languageAndData.exhibitionLanguage.subtitle',
          icon: 'web',
          path: '',
          select: [
            { text: 'Português', lang: 'pt' },
            { text: 'English', lang: 'en' },
          ],
        },
      ],
    };
  },
  methods: {
    changeLanguage(language) {
      localStorage.setItem('lang', language);
      window.location.reload();
    },
  },
};
</script>

<style lang="scss" scoped>
.system {
  .select {
    max-width: 16rem;
  }
}
</style>
