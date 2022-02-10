<template>
  <section class="uk-section">
    <div class="uk-container uk-container-small">
      <h2>Photo Album</h2>

      <div class="uk-margin">
        <input type="file" accept="image/*" @change="uploadPhoto" />
      </div>

      <div class="uk-grid uk-child-width-1-3@m">
        <div class="uk-margin" v-for="(photo, index) in allPhotos" :key="index">
          <div class="uk-card uk-card-default">
            <div class="uk-card-media-top">
              <img :src="photo.path" />
            </div>
            <div class="uk-card-body">{{ photo.filename }}</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ALL_PHOTOS from '../graphql/AllPhotos';
import UPLOAD_PHOTO from '../graphql/UploadPhoto';

export default {
  name: 'UploadFileDialog',
  apollo: {
    allPhotos: ALL_PHOTOS,
  },

  methods: {
    async uploadPhoto({ target }) {
      console.log(target.files);
      await this.$apollo.mutate({
        mutation: UPLOAD_PHOTO,
        variables: {
          photo: target.files[0],
        },
        update: (store, { data: { uploadPhoto } }) => {
          const data = store.readQuery({ query: ALL_PHOTOS });

          data.allPhotos.push(uploadPhoto);

          store.writeQuery({ query: ALL_PHOTOS, data });
        },
      });
    },
  },
};
</script>
