import { h } from "vue";
import { components, entry } from "django-airavata-common-ui";
import DashboardContainer from "./containers/DashboardContainer.vue";
import RecentExperimentsContainer from "./containers/RecentExperimentsContainer.vue";

entry((globalApp) => {
  globalApp.mixin({
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
      const root = document.getElementById('dashboard')
      this.viewAllExperiments = root.dataset.viewAllExperiments;
      this.username = root.dataset.username;
    },
  })
  globalApp.mount("#dashboard");
});
