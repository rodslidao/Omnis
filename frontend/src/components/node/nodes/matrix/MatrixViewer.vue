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
            :class="selectedClass"
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
    edit: String,
  },

  data: () => ({
    checkbox: true,
    checkboxList: [],
    constant: 1,
  }),

  methods: {},

  computed: {
    selectedClass() {
      const list = {
        quantityX: 'item-x',
        quantityY: 'item-y',
        sizeX: 'item-size-x',
        sizeY: 'item-size-y',
        marginX: 'item-margin-x',
        marginY: 'item-margin-y',
        sub_quantityX: 'sub-x',
        sub_quantityY: 'sub-y',
        sub_marginX: 'sub-margin-x',
        sub_marginY: 'sub-margin-y',
        originX: 'origin',
        originY: 'origin',
      };
      return `highlight-${list[this.edit]}`;
    },

    styleObject() {
      const updatedStyleObject = {
        slots: {
          height: `${this.slots.size.y * this.constant.x - 1}px`,
          width: `${this.slots.size.x * this.constant.x - 1}px`,

          marginTop: `${this.slots.margin.y * this.constant.x + 1}px`,
        },
        slotsRow: {
          marginLeft: `${this.slots.margin.x * this.constant.x + 1}px`,
        },
        subdivision: {
          marginLeft: `${this.subdivisions.margin.x * this.constant.x + 1}px`,
        },
        row: {
          marginTop: `${this.subdivisions.margin.y * this.constant.x + 1}px`,
        },
      };
      return updatedStyleObject;
    },

    findSize() {
      // constant totalMainSize = this.frameWidth;
      const counts = {
        qtd: { x: 0, y: 0 },
        margin: { x: 0, y: 0 },
        size: { x: 0, y: 0 },
        total: { x: 0, y: 0 },
      };
      Object.keys(counts.qtd).forEach((i) => {
        counts.qtd[i] = this.slots.qtd[i] * this.subdivisions.qtd[i];
        counts.size[i] = counts.qtd[i] * this.slots.size[i];
        counts.margin[i] = this.slots.margin[i] * (counts.qtd[i] - 1)
          + this.subdivisions.margin[i] * (this.subdivisions.qtd[i] - 1);
        counts.total[i] = this.width / (counts.size[i] + counts.margin[i]);
        // constant total = size + padding;
      });
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.constant = counts.total;

      return null;
    },
  },
};
</script>

<style lang="scss" scoped>
@import '~vuetify/src/styles/main.sass';

$border-radius: 2px;
$border-size: 2px;
$color-x: red;
$color-y: rgb(0, 255, 0);
$border-x: $border-size solid $color-x;
$border-y: $border-size solid $color-y;

.highlight {
  &-x {
    border-top: $border-x;
  }
  &-y {
    border-left: $border-y;
  }

  &-origin:first-child
    > .line:first-child
    > .subdivision:first-child
    > .slotsRow
    > .slots:first-child {
    border: $border-x;
  }

  &-item-x:first-child
    > .line:first-child
    > .subdivision:first-child
    > .slotsRow
    > .slots:first-child {
    border: $border-x;
  }

  &-item-y:first-child
    > .line:first-child
    > .subdivision:first-child
    > .slotsRow:first-child
    > .slots {
    border: $border-y;
  }

  &-item-size-x:first-child
    > .line:first-child
    > .subdivision:first-child
    > .slotsRow:first-child
    > .slots:first-child {
    border-top: $border-x;
  }

  &-item-size-y:first-child
    > .line:first-child
    > .subdivision:first-child
    > .slotsRow:first-child
    > .slots:first-child {
    border-left: $border-y;
  }

  &-item-margin-x {
    &:first-child
      > .line:first-child
      > .subdivision:first-child
      > .slotsRow:nth-child(2)
      > .slots:first-child {
      border-left: $border-x;
    }
    &:first-child
      > .line:first-child
      > .subdivision:first-child
      > .slotsRow:nth-child(1)
      > .slots:first-child {
      border-right: $border-x;
    }
  }

  &-item-margin-y {
    &:first-child
      > .line:first-child
      > .subdivision:first-child
      > .slotsRow:nth-child(1)
      > .slots:first-child {
      border-bottom: $border-y;
    }
    &:first-child
      > .line:first-child
      > .subdivision:first-child
      > .slotsRow:first-child
      > .slots:nth-child(2) {
      border-top: $border-y;
    }
  }

  &-sub-margin-x {
    &:first-child > .line:first-child > .subdivision:first-child {
      box-shadow: $border-size 0px 0px $color-x;
    }
    &:first-child > .line:first-child > .subdivision:nth-child(2) {
      box-shadow: (-1 * $border-size) 0px 0px 0px $color-x;
    }
  }

  &-sub-margin-y {
    &:first-child {
      // box-shadow: 0px $border-size 0px $color-y,
      box-shadow: 0px $border-size 0px $color-y;
    }
    &:nth-child(2) {
      box-shadow: 0px (-1 * $border-size) 0px 0px $color-y;
    }
  }

  &-sub-x:first-child > .line > .subdivision {
    outline: $border-x;
    border-radius: $border-radius;
  }

  &-sub-y > .line > .subdivision:first-child {
    outline: $border-y;
    border-radius: $border-radius;
  }
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
    border-radius: 4 * $border-radius;
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
          background-color: #00000085;
          box-shadow: inset 0 0 17px 2px rgb(0 0 0 / 18%);
          border-radius: $border-radius;
        }
      }
    }
  }
}
</style>
