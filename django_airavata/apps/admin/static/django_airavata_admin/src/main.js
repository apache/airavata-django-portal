import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import VueResource from "vue-resource";
import VueRouter from "vue-router";
import VueFlatPickr from "vue-flatpickr-component";
import App from "./App.vue";
import router from "./router";

import "flatpickr/dist/flatpickr.css";
import createStore from "./store";

entry((globalApp) => {
  globalApp.config.productionTip = false;

  globalApp.use(VueResource);
  globalApp.use(VueRouter);
  globalApp.use(VueFlatPickr);

  const store = createStore(globalApp);

  globalApp.mixin({
    store,
    render: () => h(components.MainLayout, [h(App)]),
    router,
  })
  globalApp.mount("#app");
});
