import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import ParserDetailsContainer from "./containers/ParserDetailsContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
    render() {
      return h(components.MainLayout, [
        h(ParserDetailsContainer, {
          props: {
            parserId: this.parserId,
          },
        }),
      ]);
    },
    data() {
      return {
        parserId: null,
        launching: false,
      };
    },
    beforeMount() {
      const root = document.getElementById('parser-details')
      if (root.dataset.parserId) {
        this.parserId = root.dataset.parserId;
      }
    },
  })
  globalApp.mount("#parser-details");
});
