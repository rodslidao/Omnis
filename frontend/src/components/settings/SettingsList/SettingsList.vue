<template>
  <div>
    <div class="d-flex align-">
      <v-autocomplete
        v-model="search"
        :items="items"
        @update:search-input.sync="filter()"
        auto-select-first
        cache-items
        :item-text="itemSearch"
        @change="filter()"
        class="mx-4 mb-4 search"
        rounded
        filled
        dense
        prepend-inner-icon="mdi-magnify"
        hide-no-data
        hide-details
        placeholder="Pesquisar"
      ></v-autocomplete>
      <div class="d-flex justify-center align-center">
        <div class="">
          {{ $t('list.sortBy') }}:<span>{{ dropdown.text }}</span>
        </div>
        <v-menu bottom offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn small text icon v-bind="attrs" v-on="on">
              <v-icon>mdi-chevron-down</v-icon>
            </v-btn>
          </template>

          <v-list>
            <v-list-item
              @click="sort(item)"
              link
              v-for="(item, index) in Object.keys(items[0])"
              :key="index"
              v-show="!fieldsIgnore.includes(item)"
            >
              <v-list-item-title>{{
                $t('settings.users.fields.' + item)
              }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>
    <div v-for="(item, index) in itemsCopy" :key="index">
        <slot name="itemList" :data="item"></slot>
    </div>
  </div>
</template>

<script>
// import SettingsListItemUser from './SettingsListItemUser.vue';

export default {
//   components: { SettingsListItemUser },
  props: {
    items: {
      type: Array,
      default: () => [],
    },
    itemSearch: {
      type: String,
      default: 'title',
    },
    fieldsIgnore: {
      type: Array,
      default: () => [],
    },
  },

  data() {
    return {
      search: null,
      show: false,
      itemsCopy: [],
      dropdown: {
        value: '',
        text: '',
      },
    };
  },

  watch: {
    items() {
      this.itemsCopy = this.items;
    },
  },

  created() {
    this.itemsCopy = this.items;
    // console.log(this.itemsCopy);
  },

  methods: {
    filter() {
      if (this.itemsCopy.length !== 0) {
        this.itemsCopy = this.items.filter((value) => {
          console.log(value);
          return value[this.itemSearch] === this.search;
        });
      } else {
        this.itemsCopy = this.items;
      }
    },

    sort(item) {
      this.dropdown.value = item;
      this.dropdown.text = this.$t(`settings.users.fields.${item}`);
      this.items.sort((a, b) => {
        return a[item] - b[item];
      });
    },

    change(value) {
      // this.$emit('selected', value);
      this.$emit('update:selected', this.$event.target.checked);
    },
  },
};
</script>

<style scoped>
.search {
  max-width: 200px;
}
</style>
