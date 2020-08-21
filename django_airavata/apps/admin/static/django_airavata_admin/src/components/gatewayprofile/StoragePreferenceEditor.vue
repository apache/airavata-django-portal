<template>
  <div>
    <b-form-group label="Login username" label-for="login-username">
      <b-form-input id="login-username" v-model="data.loginUserName" type="text" />
    </b-form-group>
    <b-form-group label="User Storage Quota (in GB)" label-for="user-storage-quota">
      <b-form-input id="user-storage-quota" v-model="data.userStorageQuota" type="number" v-on:keypress = "handleTypedInput" v-on:paste= "handlePastedInput" />
    </b-form-group>
    <b-form-group label="File System Root Location" label-for="filesystem-root-location">
      <b-form-input id="filesystem-root-location" v-model="data.fileSystemRootLocation" type="text" />
    </b-form-group>
    <b-form-group label="Resource Specific SSH Credential" label-for="default-credential-store-token" description="This is the SSH credential that will be used for to move data to/from this storage resource.">
      <ssh-credential-selector id="default-credential-store-token" v-model="data.resourceSpecificCredentialStoreToken"
        :null-option-default-credential-token="defaultCredentialStoreToken" :null-option-disabled="!defaultCredentialStoreToken">
        <template slot="null-option-label" slot-scope="nullOptionLabelScope">
          <span v-if="nullOptionLabelScope.defaultCredentialSummary">
            Use the gateway's default SSH credential ({{ nullOptionLabelScope.defaultCredentialSummary.description }})
          </span>
          <span v-else>
            Select a SSH credential
          </span>
        </template>
      </ssh-credential-selector>
    </b-form-group>
  </div>
</template>

<script>
import { mixins } from "django-airavata-common-ui";
import SSHCredentialSelector from "../credentials/SSHCredentialSelector.vue";

export default {
  name: "storage-preference-editor",
  mixins: [mixins.VModelMixin],
  components: {
    "ssh-credential-selector": SSHCredentialSelector
  },
  props: {
    defaultCredentialStoreToken: {
      type: String,
      required: true
    }
  },
  methods: {
    handleTypedInput(event) {
      const charCode = event.which || event.keyCode;
      if ((charCode >= 48 && charCode <= 57) || charCode === 46)
        return true;
      event.preventDefault();
    },
    handlePastedInput(event) {
      const num = Number(event.clipboardData.getData('text/plain'));
      if (num >= 0)
        return true;
      event.preventDefault();
    },
  }
};
</script>
