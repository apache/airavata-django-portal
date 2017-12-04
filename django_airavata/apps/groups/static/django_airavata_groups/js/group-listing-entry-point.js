import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import GroupsManageContainer from './groups_components/GroupsManageContainer.vue'
// This is imported globally on the website so no need to include it again in this view
// import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);

new Vue({
  el: "#groups-owners-manage",
  template: '<groups-manage-container></groups-manage-container>',
  data: {
      groupsOwnersData: null,
  },
  components: {
      GroupsManageContainer
  },
  beforeMount: function () {
      if (this.$el.dataset.groupsOwnersData) {
          this.groupsOwnersData = JSON.parse(this.$el.dataset.groupsOwnersData);
      }
  }
})
