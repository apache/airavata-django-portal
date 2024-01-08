import { createApp, h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import UserProfileContainer from "./containers/UserProfileContainer.vue";
import createStore from "./store";

entry((globalApp) => {
  const store = createStore(globalApp);
  const app = createApp({
    store,
    render: () => h(components.MainLayout, [h(UserProfileContainer)]),
  })
  app.mount("#user-profile");
});
