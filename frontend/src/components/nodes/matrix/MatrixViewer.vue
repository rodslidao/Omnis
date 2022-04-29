<template>
  <div class="main">
    <div class="blister">
      <div class="row" v-for="index in subdivisions.quantityLine" :key="index"  v-bind:style="styleObject.row">
        <div class="line">
          <div
            class="subdivision"
            v-bind:style="styleObject.subdivision"
            v-for="index in subdivisions.quantityColumn"
            :key="index"
          >
            <div
              class="slotRow"
              v-bind:style="styleObject.slotRow"
              v-for="index in slot.quantityColumn"
              :key="index"
            >
              <div
                class="slot"
                v-bind:style="styleObject.slot"
                v-for="index in slot.quantityLine"
                :key="index"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    checkbox: true,
    checkboxList: [],
    slot: {
      quantityLine: 5,
      quantityColumn: 3,
      offsetLeft: 1,
      offsetHeight: 1,
      height: 0,
      width: 0,
    },
    subdivisions: {
      quantityLine: 3,
      quantityColumn: 3,
      offsetLeft: 20,
      offsetHeight: 26,
    },
  }),
  methods: {},

  computed: {
    styleObject() {
      return {
        slot: {
          height: `${this.slot.height}px`,
          width: `${this.slot.width}px`,
          marginTop: `${this.slot.offsetHeight}px`,
        },
        slotRow: {
          marginLeft: `${this.slot.offsetLeft}px`,
        },
        subdivision: {
          marginLeft: `${this.subdivisions.offsetLeft}px`,
        },
        row: {
          marginTop: `${this.subdivisions.offsetHeight}px`,
        },
      };
    },
  },
};
</script>

<style lang="scss" scoped>
div {
  padding: 8px;
  border: solid 1px rgb(0, 0, 0);
}
.main {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 2%;
  .blister {
    border-color: aqua;
    .row {
      &:first-child {
        margin-top: 0 !important;
        // background-color: rgb(221, 126, 109);
      }
    }
    .line {
      border-color: rgb(160, 152, 152);
      display: flex;
      .subdivision {
        border-color: rgb(243, 243, 243);
        display: flex;
        flex-direction: row;
        &:first-child {
          margin-left: 0 !important;
          margin-top: 0 !important;
          background-color: rgb(170, 199, 166);
        }

        .slotRow {
          display: flex;
          flex-direction: column;
          background-color: blue;
          &:first-child {
            margin-left: 0 !important;
            margin-top: 0 !important;
            background-color: rgb(30, 155, 13);
          }
        }

        .slot {
          &:first-child {
            margin-left: 0 !important;
            margin-top: 0 !important;
            background-color: rgb(0, 0, 0);
          }
          border-color: rgb(255, 0, 85);
        }
      }
    }
  }
}
</style>
