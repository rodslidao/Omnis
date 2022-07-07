<template>
  <div class="mt-11">
    <router-view :key="$route.path" @refetch="refetch" :items="model"> </router-view>
    <div v-if="$router.currentRoute.name == 'object'">
      <settings-items
        :title="$t('settings.process.objects.add')"
        :subtitle="$t('settings.process.objects.subtitle')"
        icon="cube"
        divider-list
        path="object/add"
      ></settings-items>

      <settings-title>{{
        $t('settings.process.objects.list')
      }}</settings-title>

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
            @edit-obj="updateObj"
            :obj="itemList.data"
          ></settings-list-item-obj>
          <v-divider></v-divider>
        </template>
      </settings-list>

      <object-edit
        v-if="editDialog"
        :items="model"
        @edit-obj="edit"
        @cancel-event="editDialog = false"
      ></object-edit>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemObj from '../../components/settings/SettingsList/SettingsListItemObj.vue';
import ObjectEdit from '../../components/settings/process/ObjectEdit.vue';

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
    }
  }
`;

const REMOVE_OBJ = gql`
  mutation REMOVE_OBJ($_id: ID!) {
    delete_object(_id: $_id)
  }
`;

const UPDATE_OBJ = gql`
  mutation UPDATE_OBJ(
    $_id: ID!
    $color_hex: String
    $color_name: String
    $description: String
    $img: String
    $name: String!
    $part_number: String
    $parts: Int
    $supplier: String
  ) {
    update_object(
      _id: $_id
      input: {
        color_hex: $color_hex
        color_name: $color_name
        description: $description
        img: $img
        name: $name
        part_number: $part_number
        parts: $parts
        supplier: $supplier
      }
    )
  }
`;

export default {
  components: {
    SettingsItems,
    SettingsList,
    SettingsListItemObj,
    SettingsTitle,
    ObjectEdit,
  },
  data() {
    return {
      objToEdit: {},
      editDialog: false,
      fieldsToIgnore: ['__typename', '_id', 'img', {}, []],
      // model: [
      //   {
      //     field: 'name',
      //     value: this.get_object_list.name,
      //     title: 'name',
      //     required: true,
      //   },
      //   {
      //     field: 'description',
      //     value: this.get_object_list.description,
      //     title: 'description',
      //   },
      //   {
      //     field: 'part_number',
      //     value: this.get_object_list.part_number,
      //     title: 'part_number',
      //   },
      //   {
      //     field: 'supplier',
      //     value: this.get_object_list.supplier,
      //     title: 'supplier',
      //   },
      //   {
      //     field: 'parts',
      //     value: this.get_object_list.parts,
      //     title: 'parts',
      //   },
      //   {
      //     field: 'unit',
      //     value: this.get_object_list.unit,
      //     title: 'unit',
      //   },
      //   {
      //     field: 'color_hex',
      //     value: this.get_object_list.color_hex,
      //     title: 'color',
      //   },
      //   {
      //     field: 'color_name',
      //     value: this.get_object_list.color_name,
      //     title: 'color',
      //   },
      //   {
      //     field: 'img',
      //     value: this.get_object_list.img,
      //     title: 'img',
      //   },
      // ],
      // get_object_list: [
      //   {
      //     _id: '6552818',
      //     name: 'Ovo Caipira',
      //     description: 'Ovo Jumbo galinhas livres',
      //     part_number: '0549654488',
      //     supplier: 'Meu ovo Favorito',
      //     parts: 2,
      //     unit: 'pçs',
      //     date: 1656447628,
      //     color: {
      //       name: 'Vermelho',
      //       value: '#fffff',
      //     },
      //     img: 'https://static8.depositphotos.com/1026550/1072/i/600/depositphotos_10727732-stock-photo-egg-with-clipping-path.jpg',
      //   },
      //   {
      //     _id: '6552818',
      //     name: 'Ovo Branco',
      //     description: 'Ovo Jumbo galinhas livres',
      //     part_number: '9658465421',
      //     supplier: 'Granja Ovos',
      //     parts: 4,
      //     unit: 'mm',
      //     date: 1656447628,
      //     color: {
      //       name: 'Branco',
      //       value: '#FF0000',
      //     },
      //     img: 'https://www.supermercadosaturnino.com.br/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/o/v/ovo_branco.jpg',
      //   },
      //   {
      //     _id: '6552818',
      //     name: 'Ovo de Codorna',
      //     description: '',
      //     part_number: '9658465421',
      //     supplier: 'Granja de codorna',
      //     parts: 4,
      //     unit: 'mm',
      //     date: 1656447628,
      //     color: {
      //       name: 'Manchado',
      //       value: '',
      //     },
      //     img: 'http://img.sitemercado.com.br/produtos/ebce62c05eee918980bec59c386c655c553b828c955c73fe39bedf9483db78ca_full.jpg',
      //   },
      // ],
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

    updateObj(obj) {
      this.objToEdit = obj;
      this.editDialog = true;
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

    async edit(obj) {
      console.log('edit2', obj);
      await this.$apollo
        .mutate({
          mutation: UPDATE_OBJ,
          variables: {
            // eslint-disable-next-line no-underscore-dangle
            _id: this.objToEdit._id,
            color_hex: obj.color_hex,
            color_name: obj.color_name,
            date: obj.date,
            description: obj.description,
            img: obj.img,
            name: obj.name,
            part_number: obj.part_number,
            parts: obj.parts,
            supplier: obj.supplier,
          },
        })

        .then(() => {
          // Result
          this.$apollo.queries.get_object_list.refetch();
          this.$alertFeedback(this.$t('alerts.updateObjSuccess'), 'success');
          this.editDialog = false;
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          this.$alertFeedback(this.$t('alerts.updateObjFail'), 'error', error);
          // We restore the initial user input
        });
    },
  },
};
</script>

<style>
</style>
