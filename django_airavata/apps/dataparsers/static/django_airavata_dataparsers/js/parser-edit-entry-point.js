import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ParserEditContainer from "./containers/ParserEditContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
    render() {
      return h(components.MainLayout, [
        h(ParserEditContainer, {
          props: {
            parserId: this.parserId,
          },
        }),
      ]);
    },
    data() {
      return {
        parserId: null,
      };
    },
    beforeMount() {
      if (this.$el.dataset.parserId) {
        this.parserId = this.$el.dataset.parserId;
      }
    },
  })
  app.mount("#edit-parser");
});
