import ApplicationCard from "./components/ApplicationCard.vue";
import AutocompleteTextInput from "./components/AutocompleteTextInput.vue";
import ClipboardCopyButton from "./components/ClipboardCopyButton.vue";
import ClipboardCopyLink from "./components/ClipboardCopyLink.vue";
import ConfirmationDialog from "./components/ConfirmationDialog.vue";
import DeleteButton from "./components/DeleteButton.vue";
import DeleteLink from "./components/DeleteLink.vue";
import MainLayout from "./components/MainLayout.vue";
import Pager from "./components/Pager.vue";
import ShareButton from "./components/ShareButton.vue";
import Sidebar from "./components/Sidebar.vue";
import SidebarFeed from "./components/SidebarFeed.vue";
import SidebarHeader from "./components/SidebarHeader.vue";
import UnsavedChangesGuard from "./components/UnsavedChangesGuard.vue";

import GlobalErrorHandler from "./errors/GlobalErrorHandler";
import ValidationErrors from "./errors/ValidationErrors";

import ListLayout from "./layouts/ListLayout.vue";

import VModelMixin from "./mixins/VModelMixin";

import Notification from "./notifications/Notification";
import NotificationList from "./notifications/NotificationList";

import * as utils from "./utils";

import entry from "./entry";

const components = {
  Pager,
  ApplicationCard,
  AutocompleteTextInput,
  ClipboardCopyButton,
  ClipboardCopyLink,
  ConfirmationDialog,
  DeleteButton,
  DeleteLink,
  MainLayout,
  ShareButton,
  Sidebar,
  SidebarFeed,
  SidebarHeader,
  UnsavedChangesGuard
};

const errors = {
  GlobalErrorHandler,
  ValidationErrors
};

const layouts = {
  ListLayout
};

const mixins = {
  VModelMixin
};

const notifications = {
  Notification,
  NotificationList
};

export default {
  components,
  entry,
  errors,
  layouts,
  mixins,
  notifications,
  utils
};

export {
  components,
  entry,
  errors,
  layouts,
  mixins,
  notifications,
  utils
};
