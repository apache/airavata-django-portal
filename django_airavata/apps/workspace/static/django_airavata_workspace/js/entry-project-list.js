import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ProjectListContainer from "./containers/ProjectListContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
    render() {
      return h(components.MainLayout, [
        h(ProjectListContainer, {
          props: {
            initialProjectsData: this.projectsData,
          },
        }),
      ]);
    },
    data() {
      return {
        projectsData: null,
      };
    },
    beforeMount() {
      if (this.$el.dataset.projectsData) {
        this.projectsData = JSON.parse(this.$el.dataset.projectsData);
      }
    },
  })
  app.mount("#project-list");
});
