import { createApp, h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import DashboardContainer from "./containers/DashboardContainer.vue";
import RecentExperimentsContainer from "./containers/RecentExperimentsContainer.vue";

entry((globalApp) => {
  //use globalApp to satisfy compiler
  globalApp;


  const app = createApp({
    render() {
      return h(components.MainLayout, [
        h(DashboardContainer),
        h(RecentExperimentsContainer, {
          props: {
            viewAllExperiments: this.viewAllExperiments,
            username: this.username,
          },
          slot: "sidebar",
        }),
      ]);
    },
    data() {
      return {
        viewAllExperiments: null,
        username: null,
      };
    },
    beforeMount() {
      this.viewAllExperiments = this.$el.dataset.viewAllExperiments;
      this.username = this.$el.dataset.username;
    },
  })
  app.mount("#dashboard");
});
