import { createApp, h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import EditExperimentContainer from "./containers/EditExperimentContainer.vue";
import "../../scss/styles.scss";

// Expect a template with id "edit-experiment" and experiment-id data attribute
//
//   <div id="edit-experiment" data-experiment-id="..expid.."/>

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
    render() {
      return h(components.MainLayout, [
        h(EditExperimentContainer, {
          props: {
            experimentId: this.experimentId,
          },
        }),
      ]);
    },
    data() {
      return {
        experimentId: null,
      };
    },
    beforeMount() {
      this.experimentId = this.$el.dataset.experimentId;
    },
  })
  app.mount("#edit-experiment");
});
