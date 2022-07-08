<template>
  <div class="mt-11">
    <router-view :key="$route.path" @refetch="refetch()">
    </router-view>
    <div v-show="$router.currentRoute.name == 'variable'">
      <settings-items
        :title="$t('settings.process.variables.add')"
        :subtitle="$t('settings.process.variables.subtitle')"
        icon="cube"
        divider-list
        path="variable/add"
      ></settings-items>

      <settings-title>{{ $t('settings.process.variables.list') }}</settings-title>

      <settings-list
        class="mt-4"
        :items="get_variable_list"
        item-search="name"
        :fields-ignore="fieldsToIgnore"
        translate-path="form"
      >
        <template #itemList="itemList">
          <settings-list-item-variable
            @remove="remove"
            @edit="edit"
            :obj="itemList.data"
          ></settings-list-item-variable>
          <v-divider></v-divider>
        </template>
      </settings-list>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemVariable from '@/components/settings/SettingsList/SettingsListItemVariable.vue';

const LIST_VARIABLE = gql`
  query LIST_VARIABLE {
    get_variable_list {
      _id
      name
    }
  }
`;

const REMOVE_VARIABLE = gql`
  mutation REMOVE_VARIABLE($_id: ID!) {
    delete_variable(_id: $_id)
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemVariable,
    SettingsTitle,
  },
  data() {
    return {
      fieldsToIgnore: ['__typename', '_id', 'img', {}, []],
    };
  },

  computed: {
    model() {
      const obj = this.objToEdit;
      return obj;
    },
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_variable_list: LIST_VARIABLE,
  },

  methods: {
    refetch() {
      this.$apollo.queries.get_variable_list.refetch();
    },

    edit(obj) {
      this.$router.push({
        name: 'variableEdit',
        params: {
          items: obj, // or anything you want
        },
      });
    },

    async remove(_id) {
      console.log('remove', _id);
      await this.$apollo
        .mutate({
          mutation: REMOVE_VARIABLE,
          variables: {
            _id,
          },
        })
        .then(() => {
          // Result
          this.refetch();
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
  },
};
</script>

<style>
</style>
