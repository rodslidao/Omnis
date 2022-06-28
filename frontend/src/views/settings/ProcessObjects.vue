<template>
  <div>
    <settings-items
      :title="$t('settings.process.objects.addObject')"
      :subtitle="$t('settings.process.objects.subtitle')"
      icon="cube"
      divider-list
      path="process/object/add"
    ></settings-items>

    <settings-title>{{
      $t('settings.process.objects.listObject')
    }}</settings-title>

    <settings-list
      :items="getObjList"
      item-search="first_name"
      :fields-ignore="fieldsToIgnore"
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
  </div>
</template>

<script>
import SettingsItems from '@/components/settings/SettingsItems.vue';
import SettingsList from '@/components/settings/SettingsList/SettingsList.vue';
import SettingsListItemObj from '../../components/settings/SettingsList/SettingsListItemObj.vue';

export default {
  components: { SettingsItems, SettingsList, SettingsListItemObj },
  data() {
    return {
      fieldsToIgnore: ['__typename', '_id', 'avatar_image', {}, []],
      getObjList: [
        {
          _id: '6552818',
          name: 'Caneta',
          description: 'Caneta para uso interno',
          part_number: '0549654488',
          supplier: 'MontBlanc',
          parts: 2,
          unit: 'unit',
          date: 1656447628,
          color: {
            name: 'preto',
            value: '#fffff',
          },
          img: 'https://www.palmasbrindes.com.br/media/catalog/product/cache/1/small_image/256x/9df78eab33525d08d6e5fb8d27136e95/1/1/1116am_verde.jpg',
        },
        {
          _id: '6552818',
          name: 'caneca',
          description: 'Caneca do mario',
          part_number: '9658465421',
          supplier: 'canecaria',
          parts: 4,
          unit: 'unit',
          date: 1656447628,
          color: {
            name: 'vermelho',
            value: '#FF0000',
          },
          img: 'https://socd.vteximg.com.br/arquivos/ids/177774-1310-1310/caneca-vermelha-magica-fosca.jpg?v=637280078550630000',
        },
      ],
    };
  },
};
</script>

<style>
</style>
