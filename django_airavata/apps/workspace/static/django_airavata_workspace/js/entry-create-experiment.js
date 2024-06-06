import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import CreateExperimentContainer from "./containers/CreateExperimentContainer.vue";
import "../../scss/styles.scss";

entry((globalApp) => {
  globalApp.mixin({
    render() {
      return h(components.MainLayout, [
        h(CreateExperimentContainer, {
          props: {
            appModuleId: this.appModuleId,
            userInputValues: this.userInputValues,
            experimentDataDir: this.experimentDataDir,
          },
        }),
      ]);
    },
    data() {
      return {
        appModuleId: null,
        userInputValues: null,
      };
    },
    beforeMount() {
      const root = document.getElementById('create-experiment')
      if (root.dataset.appModuleId) {
        this.appModuleId = root.dataset.appModuleId;
      }
      if (root.dataset.userInputValues) {
        this.userInputValues = JSON.parse(root.dataset.userInputValues);
      }
      if (root.dataset.experimentDataDir) {
        this.experimentDataDir = root.dataset.experimentDataDir;
      }
    },
  })
  globalApp.mount("#create-experiment");
});
