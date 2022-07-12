<template>
  <div class="mt-11">
    <router-view :key="$route.path" @refetch="refetch" :items="model">
    </router-view>
    <div v-if="$router.currentRoute.name == 'object'">
      <settings-items
        :title="$t('settings.process.objects.add')"
        :subtitle="$t('settings.process.objects.subtitle')"
        icon="cube"
        divider-list
        path="object/add"
      ></settings-items>

      <settings-title>{{ $t('settings.process.objects.list') }}</settings-title>

      <settings-list
        class="mt-4"
        :items="get_object_list"
        item-search="name"
        :fields-ignore="fieldsToIgnore"
        translate-path="form"
      >
        <template #itemList="itemList">
          <settings-list-item-obj
            @remove-obj="remove"
            @edit-obj="edit"
            :obj="itemList.data"
          ></settings-list-item-obj>
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
import SettingsListItemObj from '../../components/settings/SettingsList/SettingsListItemObj.vue';

const LIST_OBJ = gql`
  query LIST_OBJ {
    get_object_list {
      _id
      color_hex
      color_name
      date
      description
      img
      name
      part_number
      parts
      supplier
      variable
    }
  }
`;

const REMOVE_OBJ = gql`
  mutation REMOVE_OBJ($_id: ID!) {
    delete_object(_id: $_id)
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemObj,
    SettingsTitle,
  },
  data() {
    return {
      objToEdit: {},
      editDialog: false,
      fieldsToIgnore: ['__typename', '_id', 'img'],
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
            field: 'part_number',
            value: list.part_number,
            title: 'part_number',
          },
          {
            field: 'supplier',
            value: list.supplier,
            title: 'supplier',
          },
          {
            field: 'parts',
            value: list.parts,
            title: 'parts',
          },
          {
            field: 'unit',
            value: list.unit,
            title: 'unit',
          },
          {
            field: 'color_hex',
            value: list.color_hex,
            title: 'color',
          },
          {
            field: 'color_name',
            value: list.color_name,
            title: 'color',
          },
          {
            field: 'variable',
            value: list.variable,
            title: 'color',
            required: true,
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
    get_object_list: LIST_OBJ,
  },

  methods: {
    refetch() {
      this.$apollo.queries.get_object_list.refetch();
    },

    edit(obj) {
      const newObject = [];

      Object.entries(obj).forEach((a) => {
        if (!this.fieldsToIgnore.includes(a[0])) {
          console.log(a[0], a[1]);
          newObject.push({
            field: a[0],
            value: a[1],
            title: a[0],
          });
          if (this.requireFields.includes(a[0])) newObject.at(-1).required = true;
        }
      });

      this.$router.push({
        name: 'objectEdit',
        params: {
          items: newObject,
          id: obj._id, // or anything you want
        },
      });
    },

    async remove(_id) {
      console.log('remove', _id);
      await this.$apollo
        .mutate({
          mutation: REMOVE_OBJ,
          variables: {
            _id,
          },
        })
        .then(() => {
          // Result
          this.$apollo.queries.get_object_list.refetch();
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
