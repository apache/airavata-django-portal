import { h } from "vue";

import { components, entry } from "django-airavata-common-ui";
import GroupsManageContainer from "./containers/GroupsManageContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
    render: () => h(components.MainLayout, [h(GroupsManageContainer)]),
  })
  globalApp.mount("#group-list");
});
