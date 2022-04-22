<template>
  <div>
    <div class="menuList" v-on:keyup.ctrl.s="save">
      <v-btn class="button" color="primary" fab dark small @click="play">
        <v-icon> mdi-play </v-icon>
      </v-btn>
      <v-btn class="button" color="primary" fab dark small @click="stop">
        <v-icon> mdi-pause </v-icon>
      </v-btn>
      <p></p>

      <v-speed-dial
        v-model="fab"
        :top="top"
        :bottom="bottom"
        :right="right"
        :left="left"
        :direction="direction"
        :open-on-hover="hover"
        :transition="transition"
        class="d-flex flex-end"
      >
        <template v-slot:activator>
          <v-btn color="primary" fab dark>
            <v-icon v-if="fab"> mdi-close </v-icon>
            <v-icon dark v-else> mdi-dots-vertical </v-icon>
          </v-btn>
        </template>
        <v-btn
          color="primary"
          class=""
          dark
          v-for="(item, index) in items"
          :key="index"
          @click="findFunction(item.method)"
        >
          <v-icon left dark>{{ item.icon }} </v-icon>{{ item.title }}
        </v-btn>
        <!-- <v-btn color="primary" class="" dark @change="upload"> -->
        <input
          id="fileUpload"
          type="file"
          hidden
          @change="upload"
          accept=".oms,"
        />
        <v-btn color="primary" class="" dark @click="chooseFiles()">
          <v-icon left dark>mdi-upload</v-icon>Upload
        </v-btn>
        <!-- <v-file-input
            hide-input
            truncate-length="15"
            v-model="files"
          ></v-file-input> -->
      </v-speed-dial>
    </div>
    <v-progress-linear
      v-if="isLoading"
      fixed
      indeterminate
      color="cyan"
      bottom
    ></v-progress-linear>
  </div>
</template>

<script>
import { mapState, mapActions, mapGetters } from 'vuex';
import gql from 'graphql-tag';

export default {
  name: 'ActionMenuForNodes',
  props: {
    editor: Object,
  },
  components: {},

  data() {
    return {
      direction: 'top',
      fab: false,
      fling: false,
      hover: false,
      tabs: null,
      top: false,
      right: true,
      bottom: true,
      left: false,
      files: null,
      result_: 'Teste',
      transition: 'slide-y-reverse-transition',
      items: [
        {
          title: 'Salvar',
          icon: 'mdi-content-save',
          method: 'saveClicked',
        },
        { title: 'Download', icon: 'mdi-file-download', method: 'download' },
        // { title: 'Upload', icon: 'mdi-file-upload', method: 'upload' },
      ],
      isLoading: false,
    };
  },

  computed: {
    ...mapState('node', {
      selectedTabIndex: (state) => state.selectedTabIndex,
      tabList: (state) => state.tabList,
      selectedTabId: (state) => state.selectedTabId,
    }),

    ...mapGetters('node', [
      'selectedTabName',
      'selectedTabObject', // -> this.getTabName
    ]),
  },

  methods: {
    ...mapActions('node', ['play', 'setSaved']),

    chooseFiles() {
      document.getElementById('fileUpload').click();
      // console.log(this.$alertFeedback);
      // this.$alertFeedback('Uploading...', 'info');
      // this.$alertFeedback('George', 'info');
    },

    async play() {
      console.log('play');
      this.isLoading = true;

      // aconst tabToPlay = this.tabList[this.selectedTabIndex];

      await this.$apollo
        .mutate({
          mutation: gql`
            mutation play($id: ID!) {
              loadConfig(_id: $id)
              startProcess {
                data {
                  error
                }
              }
            }
          `,
          variables: {
            id: '620c0b85b975eb564a701b5e',
            // id: tabToPlay.id,
          },
          update: (store, { data: { startProcess } }) => {
            console.log(startProcess.data);
          },
        })

        .then((data) => {
          // Result
          console.log(data);
          this.$alertFeedback('Programa está sendo executado', 'success');
          this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          console.error('Não foi possível rodar o programa \n', error);
          this.$alertFeedback(
            'Não foi possível rodar programa',
            'error',
            error,
          );

          // We restore the initial user input
        });
    },

    async stop() {
      console.log('stop');
      this.isLoading = true;
      // const tabToSave = this.tabList[this.selectedTabIndex];

      await this.$apollo
        .mutate({
          mutation: gql`
            mutation stopProcess() {
              stopProcess() {
                data {
                  _id
                }num quer
              }
            }
          `,
          update: (store, { data: { loadConfig } }) => {
            console.log(loadConfig.data);
          },
        })

        .then((data) => {
          // Result
          console.log(data);
          this.$alertFeedback('A rotina foi parada', 'success');
          this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          console.error('Não foi possível salvar o arquivo \n', error);
          this.$alertFeedback(
            'Não foi possível parar a rotina',
            'error',
            error,
          );

          // We restore the initial user input
        });
    },

    async pause() {
      console.log('pause');
      const tabToSave = this.tabList[this.selectedTabIndex];
      this.isLoading = true;

      await this.$apollo
        .mutate({
          mutation: gql`
            mutation pauseProcess() {
              pauseProcess() {
                data {
                  _id
                }
              }
            }
          `,
          variables: {
            id: tabToSave.id,
          },
          update: (store, { data: { loadConfig } }) => {
            console.log(loadConfig.data);
          },
        })

        .then((data) => {
          // Result
          console.log(data);
          this.$alertFeedback('Programa está sendo executado', 'success');
          this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })

        .catch((error) => {
          // Error
          this.isLoading = false;
          console.error('Não foi possível salvar o arquivo \n', error);
          this.$alertFeedback(
            'Não foi possível rodar programa',
            'error',
            error,
          );

          // We restore the initial user input
        });
    },

    findFunction(name) {
      this[name]();
    },

    async saveClicked() {
      if (this.tabList[this.selectedTabIndex].saved) {
        await this.update();
      } else {
        await this.save();
      }
    },

    async update() {
      console.log('update');
      this.isLoading = true;
      const tabToSave = this.tabList[this.selectedTabIndex];

      await this.$apollo
        .mutate({
          mutation: gql`
            mutation updateNodeSheet($id: ID!, $name: String, $content: JSON!) {
              updateNodeSheet(_id: $id, name: $name, content: $content) {
                data {
                  _id
                }
              }
            }
          `,
          variables: {
            id: tabToSave.id,
            content: this.editor.save(),
          },
          update: (store, { data: { updateNodeSheet } }) => {
            console.log(updateNodeSheet.data);
          },
        })
        .then((data) => {
          // Result
          console.log(data);
          this.$alertFeedback('Arquivo salvo com sucesso', 'success');
          this.isLoading = false;
          // this.setSaved(this.selectedTabIndex);
        })
        .catch((error) => {
          // Error
          this.isLoading = false;
          console.error('Não foi possível salvar o arquivo \n', error);
          this.$alertFeedback(
            'Não foi possível salvar o arquivo, erro ao conectar com servidor',
            'error',
            error,
          );

          // We restore the initial user input
        });
    },

    async save() {
      console.log('save');
      this.isLoading = true;
      console.log(" :salvo com sucesso!'");

      const tabToSave = this.tabList[this.selectedTabIndex];

      await this.$apollo
        .mutate({
          mutation: gql`
            mutation createNodeSheet(
              $id: ID!
              $name: String
              $saved: Boolean
              $duplicated: Boolean
              $content: JSON!
            ) {
              createNodeSheet(
                _id: $id
                name: $name
                saved: $saved
                duplicated: $duplicated
                content: $content
              ) {
                data {
                  _id
                }
              }
            }
          `,
          variables: {
            id: tabToSave.id,
            name: tabToSave.name,
            saved: tabToSave.saved,
            duplicated: tabToSave.duplicated,
            content: this.editor.save(),
          },
          update: (store, { data: { createNodeSheet } }) => {
            console.log(createNodeSheet);
          },
        })
        .then((data) => {
          // Result
          console.log(data);
          this.$alertFeedback('Arquivo salvo com sucesso', 'success');
          this.isLoading = false;
          this.setSaved({ index: this.selectedTabIndex, value: true });
        })
        .catch((error) => {
          // Error
          this.isLoading = false;
          console.error('Não foi possível salvar o arquivo \n', error);
          this.$alertFeedback(
            'Não foi possível salvar o arquivo, erro ao conectar com servidor',
            'error',
            error,
          );

          // We restore the initial user input
        });
    },

    download() {
      function download(content, fileName, contentType) {
        const a = document.createElement('a');
        const file = new Blob([content], { type: contentType });
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
      }
      const fileName = this.tabList[this.selectedTabIndex].name;
      download(
        JSON.stringify(this.editor.save()),
        `${fileName}.oms`,
        'text/plain',
      );
    },

    out() {
      console.log(this);
    },

    async upload({ target }) {
      this.fab = false;

      if (
        target.files[0].name.split('.').pop() !== 'oms'
        || target.files[0].name.split('.').pop() !== 'json'
      ) {
        this.$alertFeedback(
          'Arquivo inválido, seu arquivo deve ser um .oms',
          'error',
        );

        return;
      }

      // console.log(target.files[0].name.split('.').pop());
      const { files } = target;
      const fr = new FileReader();
      console.log(files);
      if (files.length <= 0) {
        return;
      }

      let json;

      async function loadFile(callback) {
        console.log(callback);
        fr.onload = async (e) => {
          json = JSON.parse(e.target.result);
          await callback();
        };
      }

      this.isLoading = true;

      // Use time out to wait for the file to be read
      fr.readAsText(files[0]);

      loadFile(async () => {
        await this.$apollo
          .mutate({
            mutation: gql`
              mutation createNodeSheet($input: JSON!) {
                createNodeSheet(input: $input) {
                  data {
                    _id
                  }
                }
              }
            `,
            variables: {
              input: json,
            },
            update: (store, { data: { createNodeSheet } }) => {
              // eslint-disable-next-line no-underscore-dangle
              console.log(createNodeSheet.data._id);
            },
          })
          .then((data) => {
            // Result
            console.log(data);
            this.$alertFeedback('Arquivo salvo com sucesso', 'success');
            this.isLoading = false;
          })
          .catch((error) => {
            // Error
            this.isLoading = false;
            console.error(
              'Não foi possível fazer o UPLOAD do arquivo \n',
              error,
            );
            this.$alertFeedback(
              'Não foi possível fazer o upload do arquivo',
              'error',
            );

            // We restore the initial user input
          });
        console.log(json);
      });
    },
  },
};
</script>

<style lang="scss">
.menuList {
  display: flex;
  flex-direction: row;
  align-items: center;

  .button {
    right: 25px;
    bottom: 16px;
    margin-left: 10px;
  }
  .v-speed-dial--direction-top .v-speed-dial__list {
    flex-direction: column-reverse;
    bottom: 100%;
    align-items: flex-end;
  }
}
</style>
