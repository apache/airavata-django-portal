import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import ParsersManageContainer from "./containers/ParsersManageContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
    render: () => h(components.MainLayout, [h(ParsersManageContainer)]),
  })
  globalApp.mount("#parsers-manage");
});
