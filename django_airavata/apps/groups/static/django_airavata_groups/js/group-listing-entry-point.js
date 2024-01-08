import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupsManageContainer from "./containers/GroupsManageContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
    render: () => h(components.MainLayout, [h(GroupsManageContainer)]),
  })
  app.mount("#group-list");
});
