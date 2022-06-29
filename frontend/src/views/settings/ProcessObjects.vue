<template>
  <div>
    <router-view :key="$route.path"> </router-view>
    <div v-show="$router.currentRoute.name == 'object'">
      <settings-items
        :title="$t('settings.process.objects.addObject')"
        :subtitle="$t('settings.process.objects.subtitle')"
        icon="cube"
        divider-list
        path="object/add"
      ></settings-items>

      <settings-title>{{
        $t('settings.process.objects.listObject')
      }}</settings-title>

      <settings-list
        class="mt-4"
        :items="getObjList"
        item-search="name"
        :fields-ignore="fieldsToIgnore"
        translate-path="form"
      >
        <template #itemList="itemList">
          <settings-list-item-obj
            @remove-obj="edit"
            @edit-obj="remove"
            :obj="itemList.data"
          ></settings-list-item-obj>
          <v-divider></v-divider>
        </template>
      </settings-list>
    </div>
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsTitle from '@/components/settings/SettingsTitle.vue';
import SettingsListItemObj from '../../components/settings/SettingsList/SettingsListItemObj.vue';

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
      fieldsToIgnore: ['__typename', '_id', 'img', {}, []],
      getObjList: [
        {
          _id: '6552818',
          name: 'Ovo Caipira',
          description: 'Ovo Jumbo galinhas livres',
          part_number: '0549654488',
          supplier: 'Meu ovo Favorito',
          parts: 2,
          unit: 'pçs',
          date: 1656447628,
          color: {
            name: 'Vermelho',
            value: '#fffff',
          },
          img: 'https://static8.depositphotos.com/1026550/1072/i/600/depositphotos_10727732-stock-photo-egg-with-clipping-path.jpg',
        },
        {
          _id: '6552818',
          name: 'Ovo Branco',
          description: 'Ovo Jumbo galinhas livres',
          part_number: '9658465421',
          supplier: 'Granja Ovos',
          parts: 4,
          unit: 'mm',
          date: 1656447628,
          color: {
            name: 'Branco',
            value: '#FF0000',
          },
          img: 'https://www.supermercadosaturnino.com.br/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/o/v/ovo_branco.jpg',
        },
        {
          _id: '6552818',
          name: 'Ovo de Codorna',
          description: '',
          part_number: '9658465421',
          supplier: 'Granja de codorna',
          parts: 4,
          unit: 'mm',
          date: 1656447628,
          color: {
            name: 'Manchado',
            value: '',
          },
          img: 'http://img.sitemercado.com.br/produtos/ebce62c05eee918980bec59c386c655c553b828c955c73fe39bedf9483db78ca_full.jpg',
        },
      ],
    };
  },

  methods: {
    updateUser(user) {
      console.log(user);
      this.objToEdit = user;
      this.editDialog = true;
    },

    async remove(_id) {
      console.log('remove', _id);
      //   await this.$apollo
      //     .mutate({
      //       mutation: REMOVE_USER,
      //       variables: {
      //         _id,
      //       },
      //     })
      //     .then(() => {
      //       // Result
      //       this.$apollo.queries.getUsersList.refetch();
      //       this.$alertFeedback(this.$t('alerts.deleteSuccess'), 'success');
      //       // this.isLoading = false;
      //       // this.setSaved(this.selectedTabIndex);
      //     })
      //     .catch((error) => {
      //       // Error
      //       this.isLoading = false;
      //       this.$alertFeedback(this.$t('alerts.deleteFail'), 'error', error);
      //       // We restore the initial user input
      //     });
    },

    async edit(user) {
      console.log('edit', user);
      //   await this.$apollo
      //     .mutate({
      //       mutation: UPDATE_USER,
      //       variables: {
      //         // eslint-disable-next-line no-underscore-dangle
      //         _id: user._id,
      //         username: user.username,
      //         password: user.password,
      //         email: user.email,
      //         first_name: user.first_name,
      //         last_name: user.last_name,
      //         level: user.level,
      //       },
      //     })

      //     .then(() => {
      //       // Result
      //       this.$apollo.queries.getUsersList.refetch();
      //       this.$alertFeedback(this.$t('alerts.updateUserSuccess'), 'success');
      //       this.editDialog = false;
      //     })

      //     .catch((error) => {
      //       // Error
      //       this.isLoading = false;
      //       this.$alertFeedback(this.$t('alerts.updateUserFail'), 'error', error);
      //       // We restore the initial user input
      //     });
    },
  },
};
</script>

<style>
</style>
