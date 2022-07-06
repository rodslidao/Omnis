<template>
  <div class="mt-11">
    <!-- {{get_matrix_list}} -->
    <router-view :key="$route.path" @refetch="refetch()" :items="model"> </router-view>
    <div v-if="$router.currentRoute.name == 'matrix'">
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
            @remove-obj="remove"
            @edit-obj="updateObj"
            :obj="itemList.data"
          ></settings-list-item-matrix>
          <v-divider></v-divider>
        </template>
      </settings-list>

      <matrix-edit
        v-if="editDialog"
        :items="model"
        @edit-obj="edit"
        @cancel-event="editDialog = false"
      ></matrix-edit>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemMatrix from '@/components/settings/SettingsList/SettingsListItemMatrix.vue';
import MatrixEdit from '@/components/settings/process/MatrixEdit.vue';

const LIST_PROCESS = gql`
  query LIST_PROCESS {
    get_matrix_list {
      _id
      name
      description
      slots
      subdivisions
    }
  }
`;

const REMOVE_MATRIX = gql`
  mutation REMOVE_MATRIX($_id: ID!) {
    delete_matrix(_id: $_id)
  }
`;

const UPDATE_PROCESS = gql`
  mutation UPDATE_PROCESS(
    $_id: ID!
    $description: String
    $name: String
    $slots: JSON
    $subdivisions: JSON
  ) {
    update_process(
      _id: $_id
      input: {
        description: $description
        name: $name
        subdivisions: $subdivisions
        slots: $slots
      }
    )
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemMatrix,
    SettingsTitle,
    MatrixEdit,
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
          // {
          //   field: 'slots',
          //   value: list.slots,
          //   title: 'slots',
          // },
          // {
          //   field: 'subdivisions',
          //   value: list.subdivisions,
          //   title: 'subdivisions',
          // },
          {
            field: 'origemX',
            value: list.origem_x,
            title: 'origemX',
          },
          {
            field: 'origemY',
            value: list.origem_y,
            title: 'origemY',
          },
          {
            field: 'subdivisionsX',
            // value: list.subdivisions.qtd.x,
            title: 'subdivisionsX',
          },
          {
            field: 'subdivisionsY',
            // value: list.subdivisions.qtd.y,
            title: 'subdivisionsY',
          },
          {
            field: 'slotsX',
            // value: list.slots.qtd.x,
            title: 'slotsX',
          },
          {
            field: 'slotsY',
            // value: list.slots.qtd.y,
            title: 'slotsY',
          },
          {
            field: 'slotsMarginX',
            // value: list.slots.qtd.x,
            title: 'slotsMarginX',
          },
          {
            field: 'slotsMarginY',
            // value: list.slots.qtd.y,
            title: 'slotsMarginY',
          },
          {
            field: 'subdivisionsMarginX',
            // value: list.slots.qtd.x,
            title: 'subdivisionsMarginX',
          },
          {
            field: 'subdivisionsMarginY',
            // value: list.slots.qtd.y,
            title: 'subdivisionsMarginY',
          },
          {
            field: 'slotsSizeX',
            // value: list.slots.qtd.y,
            title: 'slotsSizeX',
          },
          {
            field: 'slotsSizeY',
            // value: list.slots.qtd.y,
            title: 'slotsSizeY',
          },
        ];
        return objList;
      }
      return [];
    },
  },

  apollo: {
    // Simple query that will update the 'hello' vue property
    get_matrix_list: LIST_PROCESS,
  },

  methods: {
    refetch() {
      this.$apollo.queries.get_matrix_list.refetch();
    },

    updateObj(obj) {
      this.objToEdit = obj;
      this.editDialog = true;
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
          this.$apollo.queries.get_matrix_list.refetch();
          this.$alertFeedback(
            this.$t('alerts.updateMatrixSuccess'),
            'success',
          );
          this.editDialog = false;
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(
            this.$t('alerts.updateMatrixFail'),
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
