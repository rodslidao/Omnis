<template>
  <div class="mt-11">
    <!-- {{get_matrix_list}} -->
    {{ model }}
    <router-view :key="$route.path" @refetch="refetch()">
    </router-view>
    <div v-show="$router.currentRoute.name == 'matrix'">
      <settings-items
        :title="$t('settings.process.process.add')"
        :subtitle="$t('settings.process.process.subtitle')"
        icon="cube"
        divider-list
        path="matrix/add"
      ></settings-items>

      <settings-title>{{ $t('settings.process.matrix.list') }}</settings-title>

      <settings-list
        class="mt-4"
        :items="get_matrix_list"
        item-search="name"
        :fields-ignore="fieldsToIgnore"
        translate-path="form"
      >
        <template #itemList="itemList">
          <settings-list-item-matrix
            @remove="remove"
            @edit="edit"
            :obj="itemList.data"
          ></settings-list-item-matrix>
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
import SettingsListItemMatrix from '@/components/settings/SettingsList/SettingsListItemMatrix.vue';

const LIST_MATRIX = gql`
  query LIST_MATRIX {
    get_matrix_list {
      _id
      name
      description
      slots
      subdivisions
      origin
      part_number
    }
  }
`;

const REMOVE_MATRIX = gql`
  mutation REMOVE_MATRIX($_id: ID!) {
    delete_matrix(_id: $_id)
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemMatrix,
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
    get_matrix_list: LIST_MATRIX,
  },

  methods: {
    refetch() {
      this.$apollo.queries.get_matrix_list.refetch();
    },

    edit(obj) {
      this.$router.push({
        name: 'matrixEdit',
        params: {
          items: obj, // or anything you want
        },
      });
    },

    async remove(_id) {
      console.log('remove', _id);
      await this.$apollo
        .mutate({
          mutation: REMOVE_MATRIX,
          variables: {
            _id,
          },
        })
        .then(() => {
          // Result
          this.$apollo.queries.get_matrix_list.refetch();
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
