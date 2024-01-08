import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupCreateContainer from "./containers/GroupCreateContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

 const app = createApp({
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
      if (this.$el.dataset.next) {
        this.next = this.$el.dataset.next;
      }
    },
  })
  app.mount("#group-create");
});
