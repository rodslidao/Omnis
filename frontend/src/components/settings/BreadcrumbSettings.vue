<template>
  <!-- <div class=" align-center"> -->
  <div class="d-flex align-center">
    <v-btn
      icon
      large
      class="mr-n4"
      @click="$router.back()"
      alt
      v-if="$router.currentRoute.name !== 'default'"
    >
      <v-icon>mdi-chevron-left</v-icon>
    </v-btn>
    <!-- <div class="text-h4">{{ $route.name }}</div> -->
    <v-breadcrumbs :items="crumbs">
      <template v-slot:item="{ item }" class="text">
        <v-breadcrumbs-item :href="item.to">
          <span
            :class="
              $router.currentRoute.name == item.path
                ? 'text-h4 text--primary'
                : 'text-h6 text--grey'
            "
            >{{ item.text }}</span
          >
        </v-breadcrumbs-item>
      </template>
      <template v-slot:divider>
        <v-icon>mdi-chevron-right</v-icon>
      </template>
    </v-breadcrumbs>
    <div></div>
  </div>
</template>

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
      const pathArray = this.$route.path.split('/');
      pathArray.shift();
      console.log(pathArray);
      const breadcrumbs = pathArray.reduce((breadcrumbArray, path, idx) => {
        breadcrumbArray.push({
          path,
          to: breadcrumbArray[idx - 1]
            ? `/${breadcrumbArray[idx - 1].path}/${path}`
            : `/${path}`,
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
</style>
