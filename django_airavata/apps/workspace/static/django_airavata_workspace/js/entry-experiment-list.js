import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ExperimentListContainer from "./containers/ExperimentListContainer.vue";
import VueFlatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";

entry((globalApp) => {
  globalApp.use(VueFlatPickr);
  const app = createApp({
    render() {
      return h(components.MainLayout, [
        h(ExperimentListContainer, {
          props: {
            initialExperimentsData: this.experimentsData,
          },
        }),
      ]);
    },
    data() {
      return {
        experimentsData: null,
      };
    },
    beforeMount() {
      if (this.$el.dataset.experimentsData) {
        this.experimentsData = JSON.parse(this.$el.dataset.experimentsData);
      }
    },
  })
  app.mount("#experiment-list");
});
