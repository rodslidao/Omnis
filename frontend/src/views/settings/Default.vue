<template >
  <div>
    <div v-for="item in items">
      <b-nav-item :to="item.path">
        {{ item.name }}
      </b-nav-item>
    </div>
  </div>
</template>

<script>
export default {
  created() {
    this.$router.options.routes.forEach((route) => {
      this.items.push({
        name: route.name,
        path: route.path,
      });
    });
    console.log(this.$router.options);
  },
  data() {
    return {
      items: [],
    };
  },
};
</script>

<style>
</style>
