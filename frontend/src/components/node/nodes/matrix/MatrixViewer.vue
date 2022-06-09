/* eslint-disable vue/require-valid-default-prop */
<template>
  <div class="">
    {{ findSize }}
    <div class="main">
      <div class="warp">
        <div class="blister" ref="blister">
          <div
            class="row"
            v-for="index in subdivisions.qtd.y"
            :key="index"
            v-bind:style="styleObject.row"
          >
            <div class="line">
              <div
                class="subdivision"
                v-bind:style="styleObject.subdivision"
                v-for="index in subdivisions.qtd.x"
                :key="index"
              >
                <div
                  class="slotsRow"
                  v-bind:style="styleObject.slotsRow"
                  v-for="index in slots.qtd.x"
                  :key="index"
                >
                  <div
                    class="slots"
                    v-bind:style="styleObject.slots"
                    v-for="index in slots.qtd.y"
                    :key="index"
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from '@vue/composition-api';
import { useElementSize } from '@vueuse/core';

export default {
  setup() {
    const blister = ref(null);
    const { width, height } = useElementSize(blister);

    return {
      blister,
      width,
      height,
    };
  },

  props: {
    slots: Object,
    subdivisions: Object,
  },
  // mounted() {
  //   console.log('mounted', this.slots, this.subdivisions);
  // },

  data: () => ({
    checkbox: true,
    checkboxList: [],

    // slots: {
    //   qtd: {
    //     X: 6,
    //     Y: 5,
    //   },
    //   margin: {
    //     X: 5,
    //     Y: 4.5,
    //   },
    //   size: { X: 38, Y: 38 },
    // },
    // subdivisions: {
    //   // colunas, linhas
    //   qtd: { X: 1, Y: 1 },
    //   // largura, altura
    //   margin: { X: 50, Y: 50 },
    // },
    constant: 1,
  }),

  methods: {},

  computed: {
    styleObject() {
      const updatedStyleObject = {
        slots: {
          height: `${this.slots.size.y * this.constant.x -1}px`,
          width: `${this.slots.size.x * this.constant.x -1}px`,
          marginTop: `${this.slots.margin.y * this.constant.x +1}px`,
        },
        slotsRow: {
          marginLeft: `${this.slots.margin.x * this.constant.x +1}px`,
        },
        subdivision: {
          marginLeft: `${this.subdivisions.margin.x * this.constant.x +1}px`,
        },
        row: {
          marginTop: `${this.subdivisions.margin.y * this.constant.x +1}px`,
        },
      };
      return updatedStyleObject;
    },

    findSize() {
      // constant totalMainSize = this.frameWidth;
      let counts = {
        qtd: { x: 0, y: 0 },
        margin: { x: 0, y: 0 },
        size: { x: 0, y: 0 },
        total: { x: 0, y: 0 },
      };
      Object.keys(counts.qtd).forEach((i) => {
        counts.qtd[i] = this.slots.qtd[i] * this.subdivisions.qtd[i];
        counts.size[i] = counts.qtd[i] * this.slots.size[i];
        counts.margin[i] =
          this.slots.margin[i] * (counts.qtd[i] - 1) +
          this.subdivisions.margin[i] * (this.subdivisions.qtd[i] - 1);
        counts.total[i] = this.width / (counts.size[i] + counts.margin[i]);
        // constant total = size + padding;
      });
      this.constant = counts.total;

      return null;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/main.sass';

div {
  // padding: 8px;
  // border: solid 1px rgb(0, 0, 0);
}
.main {
  padding: 0 1rem;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  // padding: 2%;
  .warp {
    margin-top: 1rem;
    width: 100%;
    padding: 4%;
    box-shadow: 0 0 9px 6px rgb(0 0 0 / 18%);
    background-image: linear-gradient(
      to right top,
      #a1ffff,
      #80ecfc,
      #65d8f9,
      #54c2f4,
      #53acec,
      #509bde,
      #4f8acf,
      #4e79bf,
      #3e6bab,
      #2f5c97,
      #1e4e84,
      #0b4171
    );
    border-radius: 2%;
  }
  .blister {
    // border-color: aqua;
    width: 100%;
    display: block;
    // padding: 1rem;
    .row {
      margin: 0;
      &:first-child {
        margin-top: 0 !important;
        // background-color: rgb(221, 126, 109);
      }
    }
    .line {
      //   border-color: rgb(160, 152, 152);
      display: flex;
      .subdivision {
        // border-color: rgb(243, 243, 243);
        display: flex;
        flex-direction: row;
        &:first-child {
          margin-left: 0 !important;
          margin-top: 0 !important;
          //   background-color: rgb(170, 199, 166);
        }

        .slotsRow {
          display: flex;
          flex-direction: column;
          //   background-color: blue;
          &:first-child {
            margin-left: 0 !important;
            margin-top: 0 !important;
            // background-color: rgb(30, 155, 13);
          }
        }

        .slots {
          &:first-child {
            margin-left: 0 !important;
            margin-top: 0 !important;
            // background-color: rgb(0, 0, 0);
          }
          background-color: #1e1e1e;
          box-shadow: inset 0 0 17px 2px rgb(0 0 0 / 18%);
          border-radius: 8%;
        }
      }
    }
  }
}
</style>
