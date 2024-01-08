import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ExperimentListContainer from "./containers/ExperimentListContainer.vue";
import VueFlatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";

entry((globalApp) => {
  globalApp.use(VueFlatPickr);
  globalApp.mixin({
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
      const root = document.getElementById('experiment-list')
      if (root.dataset.experimentsData) {
        this.experimentsData = JSON.parse(root.dataset.experimentsData);
      }
    },
  })
  globalApp.mount("#experiment-list");
});
