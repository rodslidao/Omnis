<template>
  <v-row justify="center">
    <v-dialog
      :dark="dark"
      v-model="dialog"
      :persistent="persistent"
      :max-width="maxWidth"
      scrollable
    >
      <v-card max-height="80vh" :loading="loading">
        <template v-slot:activator="{ on, attrs }">
          <div v-bind="attrs" v-on="on">
            <slot></slot>
          </div>
        </template>

        <v-card-title class="text-h5 wb">
          {{ title ? title : $t('dialogs.removeConfirm') }}
        </v-card-title>
        <v-card-text class="wb"
          >{{
            description
              ? description
              : $t('dialogs.removeDescription', { obj: del })
          }}
          <slot name="description"></slot>
        </v-card-text>
        <v-divider></v-divider>

        <v-card-actions v-if="!del">
          <v-spacer></v-spacer>
          <div v-if="!this.$slots.actions">
            <v-btn color="primary" text @click="$emit('cancel-event')" rounded :disabled="cancelDisable">
              {{ cancelText ? cancelText : $t('buttons.cancel') }}
            </v-btn>
            <v-btn text @click="$emit('confirm-event')" rounded :disabled="confirmDisable">
              {{ confirmText ? confirmText : $t('buttons.confirm') }}
            </v-btn>
          </div>
          <slot name="actions"></slot>
        </v-card-actions>
        <v-card-actions v-else>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('cancel-event')" rounded>
            {{$t('buttons.cancel')}}
          </v-btn>
          <v-btn
            text
            rounded
            v-on:keyup.enter="$emit('confirm-event')"
            @click="$emit('confirm-event')"
          >
            Confirmar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  props: {
    confirmText: String,
    confirmDisable: Boolean,
    cancelText: String,
    cancelDisable: Boolean,
    title: String,
    description: String,
    del: String,
    loading: Boolean,
    persistent: { type: Boolean, default: true },
    dark: Boolean,
    visible: Boolean,
    timer: Number,
    maxWidth: {
      type: String,
      default: '400',
    },
  },

  data() {
    return {
      dialog: true,
    };
  },
  methods: {
    confirm() {
      this.dialog = true;
    },
  },
};
</script>
<style lang="scss" scoped>
.wb{
  word-break:normal;
}
</style>
