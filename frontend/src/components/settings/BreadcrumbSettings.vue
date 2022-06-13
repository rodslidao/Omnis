<template>
  <!-- <div class=" align-center"> -->
  <div class="d-flex align-center">
    <v-btn icon @click="$router.go(-1)" alt v-if="$route.name !== 'settings'">
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>
    <!-- <div class="text-h4">{{ $route.name }}</div> -->
    <v-breadcrumbs :items="crumbs">
      <template v-slot:item="{ item }" class="text">
        <v-breadcrumbs-item
          :href="item.to"
          :class="$router.currentRoute.name == item.path ? 'text-h5 text--primary' : 'text--grey'"
        >
          {{ item.text.toUpperCase() }}
        </v-breadcrumbs-item>
      </template>
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
  </div>
</template>D

<script>
import { menuList } from '@/components/settings/menuDescription';

export default {
  data() {
    return {
      items: menuList,
      // items: [
      //   {
      //     text: 'Configurações',
      //     href: 'config/system',
      //     disabled: false,
      //   },
      //   {
      //     text: 'Assembly',
      //     href: 'config/network',
      //     disabled: false,
      //   },
      // ],
    };
  },
  computed: {
    crumbs() {
      let pathArray = this.$route.path.split('/');
      pathArray.shift();
      console.log(pathArray);
      let breadcrumbs = pathArray.reduce((breadcrumbArray, path, idx) => {
        breadcrumbArray.push({
          path: path,
          to: breadcrumbArray[idx - 1]
            ? '/' + breadcrumbArray[idx - 1].path + '/' + path
            : '/' + path,
          text: this.$route.matched[idx].meta.breadCrumb || path,
        });
        return breadcrumbArray;
      }, []);
      return breadcrumbs;
    },
  },
};
</script>
<style lang="scss" scoped>
.text a {
  color: rgb(250, 0, 125);
}
</style>