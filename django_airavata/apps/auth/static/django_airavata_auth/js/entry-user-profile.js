import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import UserProfileContainer from "./containers/UserProfileContainer.vue";
import createStore from "./store";

entry((globalApp) => {
  const store = createStore(globalApp);
  globalApp.mixin({
    store,
    render: () => h(components.MainLayout, [h(UserProfileContainer)]),
  })
  globalApp.mount("#user-profile");
});
