<template>
  <div class="mt-11">
    <router-view @refetch="refetch()" :items="model"> </router-view>
    <div v-if="$router.currentRoute.name == 'myProcess'">
      <settings-items
        :title="$t('settings.process.process.add')"
        :subtitle="$t('settings.process.process.subtitle')"
        icon="cube"
        divider-list
        path="myProcess/add"
      ></settings-items>

      <settings-title>{{ $t('settings.process.process.list') }}</settings-title>

      <settings-list
        class="mt-4"
        :items="get_process_list"
        item-search="name"
        :fields-ignore="fieldsToIgnore"
        translate-path="form"
      >
        <template #itemList="itemList">
          <settings-list-item-process
            @remove-obj="remove"
            @edit-obj="updateObj"
            :obj="itemList.data"
          ></settings-list-item-process>
          <v-divider></v-divider>
        </template>
      </settings-list>

      <process-edit
        v-if="editDialog"
        :items="model"
        @edit-obj="edit"
        @cancel-event="editDialog = false"
      ></process-edit>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemProcess from '@/components/settings/SettingsList/SettingsListItemProcess.vue';
import ProcessEdit from '@/components/settings/process/ProcessEdit.vue';

const LIST_PROCESS = gql`
  query LIST_PROCESS {
    get_process_list {
      _id
      created_at
      created_by
      date
      description
      edited_by
      img
      last_played
      name
      sketch
      updated_at
    }
  }
`;

const REMOVE_PROCESS = gql`
  mutation REMOVE_PROCESS($_id: ID!) {
    delete_process(_id: $_id)
  }
`;

const UPDATE_PROCESS = gql`
  mutation UPDATE_PROCESS(
    $_id: ID!
    $description: String
    $img: String
    $name: String
    $sketch: JSON
  ) {
    update_process(
      _id: $_id
      input: {
        description: $description
        img: $img
        name: $name
        sketch: $sketch
      }
    )
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemProcess,
    SettingsTitle,
    ProcessEdit,
  },
  data() {
    return {
      objToEdit: {},
      editDialog: false,
      fieldsToIgnore: ['__typename', '_id', 'img', {}, []],
    };
  },

  computed: {
    model() {
      const list = this.objToEdit;
      if (list) {
        // console.log('lista', list);
        const objList = [
          {
            field: 'name',
            value: list.name,
            title: 'name',
            required: true,
          },
          {
            field: 'description',
            value: list.description,
            title: 'description',
          },
          {
            field: 'sketch',
            value: list.sketch,
            title: 'sketch',
          },
          {
            field: 'img',
            value: list.img,
            title: 'img',
          },
        ];
        return objList;
      }
      return [];
    },
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_process_list: LIST_PROCESS,
  },

  methods: {
    refetch() {
      this.$apollo.queries.get_process_list.refetch();
    },

    updateObj(obj) {
      this.objToEdit = obj;
      this.editDialog = true;
    },

    async remove(_id) {
      console.log('remove', _id);
      await this.$apollo
        .mutate({
          mutation: REMOVE_PROCESS,
          variables: {
            _id,
          },
        })
        .then(() => {
          // Result
          this.$apollo.queries.get_process_list.refetch();
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

    async edit(obj) {
      console.log('edit2', obj);
      await this.$apollo
        .mutate({
          mutation: UPDATE_PROCESS,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.objToEdit._id,
            description: obj.description,
            img: obj.img,
            name: obj.name,
            sketch: obj.sketch,
          },
        })

        .then(() => {
          // Result
          this.$apollo.queries.get_process_list.refetch();
          this.$alertFeedback(
            this.$t('alerts.updateProcessSuccess'),
            'success',
          );
          this.editDialog = false;
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(
            this.$t('alerts.updateProcessFail'),
            'error',
            error,
          );
          // We restore the initial user input
        });
    },
  },
};
</script>

<style>
</style>
