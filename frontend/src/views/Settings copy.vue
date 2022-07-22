<template>
  <section class="content d-flex justify-start align-start">
    <v-expansion-panels multiple>
      <Assembly />
      <Controls />
      <Statistics />
      <Advanced-settings />
      <Infos />
      <router-link to="/dashboard">
        <v-btn
          class="ma-3 mt-10"
          outlined
          rounded
          color="warning"
          v-if="$route.name != 'dashboard'"
        >
          <v-icon class="ma-2" small dark>mdi-chart-line</v-icon>
          Dashboard
        </v-btn>
      </router-link>
      <router-link to="/node">
        <v-btn
          class="ma-3 mt-10"
          outlined
          rounded
          color="warning"
          v-if="$route.name != 'dashboard'"
        >
          <v-icon class="ma-2" small dark>mdi-code-tags</v-icon>
          Editor node
        </v-btn>
      </router-link>
    </v-expansion-panels>
  </section>
</template>

<script>
import Infos from '@/components/settings/Infos.vue';
import AdvancedSettings from '@/components/settings/AdvancedSettings.vue';
import Statistics from '@/components/settings/Statistics.vue';
import Controls from '@/components/settings/controls/Controls.vue';
import Assembly from '@/components/settings/assembly/Assembly.vue';

export default {
  components: { AdvancedSettings, Infos, Statistics, Controls, Assembly },
  name: 'settings',
  methods: {},
  created: function () {},
};
</script>

<style lang="scss" scoped>
.content {
  // margin-top: 48px;
}

.v-expansion-panels {
  padding: 1em;
  max-width: 800px;
  margin: 0 auto;
}

v-card {
  padding: 1em;
}
</style>
