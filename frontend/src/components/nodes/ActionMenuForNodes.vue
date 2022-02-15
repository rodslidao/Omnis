<template>
  <div>
    <div class="menuList">
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
          <v-btn :loading="isLoading" color="primary" fab dark>
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
          <input id="fileUpload" type="file" hidden @change="upload"  accept=".oms," />
          <v-btn color="primary" class="" dark @click="chooseFiles()">
            <v-icon left dark>mdi-upload</v-icon>Upload
          </v-btn>
          <!-- <v-file-input
            hide-input
            truncate-length="15"
            v-model="files"
          ></v-file-input> -->
        </v-btn>
      </v-speed-dial>
    </div>
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
          method: 'save',
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
    ...mapActions('node', ['play']),

    chooseFiles() {
      document.getElementById('fileUpload').click();
      // console.log(this.$alertFeedback);
      // this.$alertFeedback('Uploading...', 'info');
      // this.$alertFeedback('George', 'info');
    },

    stop() {
      this.sendMessage({ command: 'process_stop', args: this.editor.save() });
    },

    pause() {
      this.sendMessage({ command: 'process_pause', args: this.editor.save() });
    },

    findFunction(name) {
      this[name]();
    },

    save() {
      const editedNode = this.editor.save();
      console.log(this.selectedTabId);
      console.log(this.getSelectedTabName);

      editedNode.id = this.selectedTabId;

      editedNode.sketchName = this.getSelectedTabName;
      editedNode.saved = false;

      this.updateTabById(editedNode);

      console.log(" :salvo com sucesso!'");
      console.log(this.editor.save());
      this.SEND_MESSAGE({
        type: 'SAVE_NODE',
        payload: editedNode,
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
      const fileName = this.tabList[this.selectedTabIndex].sketchName;
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
        target.files[0].name.split('.').pop() !== 'oms' ||
        target.files[0].name.split('.').pop() !== 'json'
      ) {
        this.$alertFeedback(
          'Arquivo inválido, seu arquivo deve ser um .oms',
          'error'
        );

        return;
      }

      // console.log(target.files[0].name.split('.').pop());
      const { files } = target;
      const fr = new FileReader();
      console.log(files);
      if (files.length <= 0) {
        return false;
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
              error
            );
            this.$alertFeedback(
              'Não foi possível fazer o upload do arquivo',
              'error'
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