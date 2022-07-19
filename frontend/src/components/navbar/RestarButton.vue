<template>
  <div>
    <v-btn icon @click="restartDialog = true">
      <v-icon dark>mdi-restart</v-icon>
    </v-btn>

    <v-dialog v-model="restartDialog" max-width="400">
      <v-card>
        <v-card-title class="text-h5">
          {{ online ? dilogText.title : isDisconected.title }}
        </v-card-title>

        <v-card-text>
          {{ online ? dilogText.description : isDisconected.description }}
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn text @click="restartDialog = false">
            {{ online ? dilogText.button : isDisconected.button }}
          </v-btn>

          <v-btn v-if="online" color="red darken-1" text v-on:click="request()">
            reiniciar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
export default {
  name: 'RestartButton',

  data: () => ({
    restartDialog: false,
    dilogText: {
      title: 'Tem certeza que quer reiniciar o sistema?',
      description:
        'Isso pode ajudar a resolver alguns problemas! Esse processo levará cerca de 1 min.',
      button: 'cancelar',
    },

    isDisconected: {
      title: 'Tablet desconectado!',
      description:
        'Não foi possível acessar o servidor! Caso queira reiniciar, faça a operação manualmente. Desligando e e religando no botão físico na maquina!',
      button: 'entendi',
    },
  }),

  props: {
    online: Boolean,
  },

  methods: {
    request() {
      fetch(
        `http://${this.configuration.informations.ip}:${this.configuration.informations.portStream}/exit`
      );
    },
  },
};
</script>

<style>
</style>
