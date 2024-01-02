import { createApp, h }from "vue";
import GatewayNoticesContainer from "./components/GatewayNoticesContainer";

const app = createApp({
  render() {
    return h(GatewayNoticesContainer, {
      unreadCount: this.unreadCount,
      notices: this.notices,
    })
  },
  data() {
    return {
      unreadCount: null,
      notices: null,
    };
  },
  beforeMount() {
    const root = document.getElementById('gateway-notices')
    this.unreadCount = parseInt(root.dataset.unreadCount);
    this.notices = JSON.parse(root.dataset.notices);
  },
});
app.mount("#gateway-notices");
