import { createApp, h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ParsersManageContainer from "./containers/ParsersManageContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;

  const app = createApp({
    render: () => h(components.MainLayout, [h(ParsersManageContainer)]),
  })
  app.mount("#parsers-manage");
});
