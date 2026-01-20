import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import EditProjectContainer from "./containers/EditProjectContainer.vue";

// Expect a template with id "edit-project" and project-id data attribute
//
//   <div id="edit-project" data-project-id="..projectID.."/>

entry((globalApp) => {
  globalApp.mixin({
    render() {
      return h(components.MainLayout, [
        h(EditProjectContainer, {
          props: {
            projectId: this.projectId,
          },
        }),
      ]);
    },
    data() {
      return {
        projectId: null,
      };
    },
    beforeMount() {
      const root = document.getElementById('edit-project')
      this.projectId = root.dataset.projectId;
    },
  })
  globalApp.mount("#edit-project");
});
