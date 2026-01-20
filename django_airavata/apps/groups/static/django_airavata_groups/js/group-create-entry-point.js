import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupCreateContainer from "./containers/GroupCreateContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
    render() {
      return h(components.MainLayout, [
        h(GroupCreateContainer, {
          props: {
            next: this.next,
          },
        }),
      ]);
    },
    data() {
      return {
        next: "/groups/",
      };
    },
    beforeMount() {
      const root = document.getElementById('group-create')
      if (root.dataset.next) {
        this.next = root.dataset.next;
      }
    },
  })
  globalApp.mount("#group-create");
});
