import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import { mapActions } from "vuex";
import ExperimentSummary from "./components/experiment/ExperimentSummary.vue";
import createStore from "./store";

entry((globalApp) => {
  const store = createStore(globalApp);
  globalApp.mixin({
    store,
    render() {
      return h(components.MainLayout, [h(ExperimentSummary)]);
    },
    async beforeMount() {
      const root = document.getElementById('view-experiment')
      const fullExperimentData = JSON.parse(
        root.dataset.fullExperimentData
      );
      this.setInitialFullExperimentData({ fullExperimentData });
      if ("launching" in root.dataset) {
        const launching = JSON.parse(root.dataset.launching);
        this.setLaunching({ launching });
      }
    },
    methods: {
      ...mapActions("viewExperiment", [
        "setInitialFullExperimentData",
        "setLaunching",
      ]),
    },
  })
  globalApp.mount("#view-experiment");
});
