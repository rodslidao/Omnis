<template>
  <div class="p-2 button-list">
    <div v-for="(button, index) in buttonList" :key="index">
      <v-btn
        class="button"
        v-haptic
        :show="button.show"
        :disabled="button.disabled"
        rounded
        dark
        x-large
        :color="button.color"
        @click="moveButton(button)"
      >
        <v-icon v-for="(icon, index) in button.icons" :key="index">
          mdi-{{ icon }}
        </v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      scale: '1',
      buttonList: [
        {
          name: 'x-left',
          text: 'X',
          command: 'G91 \n G0 -X',
          moveStep: 1,
          icons: ['arrow-left', 'minus', 'alpha-x'],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
        {
          name: 'x-right',
          text: 'X',
          command: 'G91 \n G0 X',
          moveStep: 1,
          icons: [ 'plus', 'alpha-x', 'arrow-right',],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
        {
          name: 'y-up',
          text: 'Y',
          command: 'G91 \n G0 Y',
          moveStep: 1,
          icons: ['arrow-up', 'plus', 'alpha-y'],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
        {
          name: 'y-down',
          text: 'Y',
          command: 'G91 \n G0 -Y',
          moveStep: 1,
          icons: ['arrow-down', 'minus', 'alpha-y'],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
        {
          name: 'z-up',
          text: 'Z',
          command: 'G91 \n G0 Z',
          moveStep: 1,
          icons: ['arrow-up', 'plus', 'alpha-z'],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
        {
          name: 'z-down',
          text: 'Z',
          command: 'G91 \n G0 -Z',
          moveStep: 1,
          icons: ['arrow-down', 'minus', 'alpha-z'],
          color: 'primary',
          disabled: false,
          show: true,
          isMoveButton: true,
        },
      ],
    };
  },

  methods: {
    moveButton(button) {
      console.log(button.command.concat(this.scale));
    },
  },
};
</script>

<style lang="scss" scoped>
.button-list {
  display: flex;
  flex-wrap: wrap;
  padding-left: 0;
  padding: 3.4%;
  .button {
    list-style: none;
    flex: 0 0 30%;
  }
}
</style>