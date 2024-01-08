import { h } from "vue";

import {components, entry} from "django-airavata-common-ui";
import UserStorageContainer from "./containers/UserStorageContainer.vue";
import UserStoragePathViewer from "./components/storage/UserStoragePathViewer.vue";

import VueRouter from "vue-router";

const routes = [
  {
    path: "*",
    component: UserStoragePathViewer,
  },
];
const router = new VueRouter({
  mode: "history",
  base: "/workspace/storage",
  routes: routes,
});
entry((globalApp) => {
  globalApp.use(VueRouter);
  const app = globalApp({
    render() {
      return h(components.MainLayout, [h(UserStorageContainer)]);
    },
    router,
  })
  app.mount("#user-storage");
});
