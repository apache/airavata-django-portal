import { createApp } from "vue";
import { BootstrapVue } from "bootstrap-vue";
import GlobalErrorHandler from "./errors/GlobalErrorHandler";
import AsyncComputed from "vue-async-computed";
import mitt from "mitt";

GlobalErrorHandler.init();

// This is imported globally on the website (see main.js) so no need to include
// it again in this view
// import 'bootstrap/dist/css/bootstrap.css'
import "bootstrap-vue/dist/bootstrap-vue.css";

/**
 * Common entry point function. Sets up common entry point functionality and
 * then calls the passed function with the Vue class as the first argument.
 *
 * @param {Function} entryPointFunction
 */
export default function entry(entryPointFunction) {
  // Common Vue configuration
  const globalApp = createApp({
    compatConfig: {
      RENDER_FUNCTION: false
    },
  });
  globalApp.use(BootstrapVue);
  globalApp.use(AsyncComputed);
    // Used for eventbus
  // Replaces $on, $off, $once deprecated api
  const emitter = mitt()
  globalApp.config.globalProperties.emitter = emitter


  entryPointFunction(globalApp);
}
