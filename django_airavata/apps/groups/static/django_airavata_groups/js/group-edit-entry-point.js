import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupEditContainer from "./containers/GroupEditContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
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
      if (this.$el.dataset.groupId) {
        this.groupId = this.$el.dataset.groupId;
      }
      if (this.$el.dataset.next) {
        this.next = this.$el.dataset.next;
      }
    },
  })
  app.mount("#group-edit");
});
