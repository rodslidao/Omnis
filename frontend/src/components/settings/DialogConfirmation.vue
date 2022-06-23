<template>
  <v-row justify="center">
    <v-dialog
      :dark="dark"
      v-model="visible"
      :persistent="persistent"
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <div v-bind="attrs" v-on="on">
          <slot></slot>
        </div>
      </template>
      <v-card>
        <v-card-title class="text-h5">
          {{ title ? title : $t('dialogs.removeConfirm') }}
        </v-card-title>
        <v-card-text
          >{{
            description
              ? description
              : $t('dialogs.removeDescription', { obj: del })
          }}
          <slot name="description"></slot>
        </v-card-text>
        <v-card-actions v-if="!del">
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('cancel-event')" rounded>
            {{ cancelText ? cancelText : $t('buttons.cancel') }}
          </v-btn>
          <v-btn text @click="$emit('confirm-event')" rounded>
            {{ confirmText ? confirmText : $t('buttons.confirm') }}
          </v-btn>
        </v-card-actions>
        <v-card-actions v-else>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="$emit('cancel-event')" rounded>
            Cancelar
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
    cancelText: String,
    title: String,
    description: String,
    del: String,
    persistent: Boolean,
    dark: Boolean,
    visible: Boolean,
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
