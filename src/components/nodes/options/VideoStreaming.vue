<template>
  <div class="warpper">
    <h4>{{ value }}</h4>
    <!-- <img src="https://zudesign.com.br/images/logo.svg" alt="alternative" /> -->
    <img src="https://philco.vteximg.com.br/arquivos/ids/176473/Maquina-de-Costura-PMC33B_058301004--4-.jpg?v=637153254507230000" alt="alternative" />
        <p>{{ node.id }}</p>
  </div>
</template>

<script>
export default {
  data: () => ({
    nodeCopy: null,
    valueCopy: null,
  }),
  props: ["option", "node", "value"],

  mounted(){
      console.log("created")
  },

  methods: {
    beautifulJson(jsonString) {
        let beautifulJsonString = JSON.stringify(
            jsonString,
            null,
            2
        );
        console.log(beautifulJsonString);
        return beautifulJsonString;
    }
  },
};
</script>

<style lang="scss" scoped>
.warpper {
  img {
    width: 100%;
    height: 50px;
  }
}
</style>