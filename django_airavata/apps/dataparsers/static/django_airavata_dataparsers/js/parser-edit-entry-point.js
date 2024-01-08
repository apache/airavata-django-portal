import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ParserEditContainer from "./containers/ParserEditContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
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
      const root = document.getElementById('edit-parser')

      if (root.dataset.parserId) {
        this.parserId = root.dataset.parserId;
      }
    },
  })
  globalApp.mount("#edit-parser");
});
