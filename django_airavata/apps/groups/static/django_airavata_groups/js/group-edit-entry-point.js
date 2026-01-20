import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupEditContainer from "./containers/GroupEditContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
    render() {
      return h(components.MainLayout, [
        h(GroupEditContainer, {
          props: {
            groupId: this.groupId,
            next: this.next,
          },
        }),
      ]);
    },
    data() {
      return {
        groupId: null,
        next: "/groups/",
      };
    },
    beforeMount() {
      const root = document.getElementById('group-edit')
      if (root.dataset.groupId) {
        this.groupId = root.dataset.groupId;
      }
      if (root.dataset.next) {
        this.next = root.dataset.next;
      }
    },
  })
  globalApp.mount("#group-edit");
});
