<template>
  <div>
    <div class="row">
      <div class="col">
        <h1 class="h4 mb-4">Manage Emails</h1>
      </div>
    </div>
    <div class="row">
      <div class="col">
        <div class="card">
          <div class="card-body">
            <list-layout @add-new-item="addNewEmail" title="Email"
              new-item-button-text="New Email" :new-button-disabled="!isGatewayAdmin">
              <template slot="new-item-editor">
                <b-card v-if="showNewItemEditor">
                  <email-editor
                    v-model="newEmail"
                    ref="emailEditor"
                    @cancelNewEmail="cancelNewEmail"
                    @saveNewEmail="saveNewEmail"
                  >
                  <template slot="title">
                    <h1 class="h4 mb-4 mr-auto">
                      New Email
                    </h1>
                  </template>
                  </email-editor>
                </b-card>
              </template>
              <template slot="item-list" slot-scope="slotProps">
                <b-table hover :fields="fields" :items="items">
                  <template slot="publishedTime" slot-scope="data">
                    <human-date :date="data.value"/>
                  </template>row
                  <template slot="expirationTime" slot-scope="data">
                    <human-date :date="data.value"/>
                  </template>
                  <template slot="action" slot-scope="data">
                    <template v-if="data.item.userHasWriteAccess">
                      <b-link class="action-link" @click="toggleDetails(data)">
                        Edit
                        <i class="fa fa-edit" aria-hidden="true"></i>
                      </b-link>
                      <delete-link @delete="deleteEmail(data.item.emailId)">
                        Are you sure you want to delete the email?
                      </delete-link>
                    </template>
                  </template>
                  <template slot="row-details" slot-scope="row">
                    <b-card>
                      <email-editor :value="row.item" v-model="updatedEmail" @userBeginsInput="isUserBeginInput = false">
                        <template slot="title">
                          <h1 class="h4 mb-4 mr-auto">
                            Update Email
                          </h1>
                        </template>
                      </email-editor>
                      <b-button variant="success" size="sm" @click="updateEmail()" :disabled="isUserBeginInput">Send Update</b-button>
                      <b-button variant="primary" size="sm" @click="toggleDetails(row)">Close</b-button>
                    </b-card>
                  </template>
                </b-table>
              </template>
            </list-layout>
          </div>
        </div>
      </div>
    </div>
  </div> 
</template>

<script>
import { models, services, session } from "django-airavata-api";
import { components, layouts } from "django-airavata-common-ui";
import SendEmailEditor from "./SendEmailEditor";


export default {
  name: "email-management-container",
  data() {
    return {
      emails: null,
      isUserBeginInput: true,
      showNewItemEditor: false,
      showingDetails: {},
    };
  },
  components: {
    'human-date': components.HumanDate,
    "delete-link": components.DeleteLink,
    "list-layout": layouts.ListLayout,
    EmailEditor,
  },
  created() {
    
  },
  computed: {
    fields() {
      return [
        {
          label: "Type",
          key: 'type'
        },
        {
          label: "Email Subject",
          key: "emailSubject"
        },
        {
          label: "Users/Groups",
          key: "users"
        },
        {
          label: "Email Body",
          key: "emailBody"
        },
        {
          label: "Publish Date",
          key: "publishedTime"
        },
        {
          label: "Expiry Date",
          key: "expirationTime"
        },
        {
          label: "Priority",
          key: "priority.name"
        },
        {
          label: "Action",
          key: "action"
        }

      ];
    },
    items() {
      return this.emails
        ? this.emails
        : [];
    },
    isGatewayAdmin() {
      return session.Session.isGatewayAdmin;
    }
  },
  methods: {
    cancelNewEmail() {
      this.showNewItemEditor = false;
    },
    addNewEmail() {
      this.showNewItemEditor = true;
    },
  }
};
</script>
