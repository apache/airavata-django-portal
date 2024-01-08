import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ProjectListContainer from "./containers/ProjectListContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
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
      const root = document.getElementById('project-list')
      if (root.dataset.projectsData) {
        this.projectsData = JSON.parse(root.dataset.projectsData);
      }
    },
  })
  globalApp.mount("#project-list");
});
