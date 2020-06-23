<template>
  <div>
    <div class="d-flex">
      <slot name="title">
      </slot>
    </div>
    <b-form
      @input="onUserInput"
      novalidate
    >
      <b-form-group
        label="Email Subject"
        label-for="email-subject"
        :invalid-feedback="getValidationFeedback('emailSubject')"
        :state="getValidationState('emailSubject')"
      >
        <b-form-input
          id="email-subject"
          type="text"
          v-model="data.title"
          required
          placeholder="Email Subject"
          :state="getValidationState('emailSubject')"
        ></b-form-input>
      </b-form-group>

      <b-form-group
        label="Email Body"
        label-for="email-body"
        :invalid-feedback="getValidationFeedback('emailBody')"
        :state="getValidationState('emailBody')"
      >
        <b-form-textarea
          id="email-body"
          type="text"
          v-model="data.emailBody"
          required
          placeholder="Email Body"
          :state="getValidationState('emailBody')"
          :rows="3"
        ></b-form-textarea>
      </b-form-group>

      <b-form-group
        label="Publish Date"
        label-for="publish-date"
      >
        <datetime
          type="datetime"
          v-model="inputPublishedTime"
          input-class="my-class"
          value-zone="UTC"
          :format="{ year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }"
          :phrases="{ok: 'Continue', cancel: 'Exit'}"
          :hour-step="1"
          :minute-step="5"
          :min-datetime="today"
          :week-start="7"
          use12-hour
          auto
        ></datetime>
      </b-form-group>

      <b-form-group
        label="Expiration Date"
        label-for="expiration-date"
      >
        <datetime
          type="datetime"
          v-model="inputExpirationTime"
          input-class="my-class"
          value-zone="UTC"
          :format="{ year: 'numeric', month: 'long', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' }"
          :phrases="{ok: 'Continue', cancel: 'Exit'}"
          :hour-step="1"
          :minute-step="5"
          :min-datetime="inputPublishedTime"
          :week-start="7"
          use12-hour
          auto

        ></datetime>
      </b-form-group>

      <b-form-group
        label="Priority"
        label-for="priority"
        :invalid-feedback="getValidationFeedback('priority')"
        :state="getValidationState('priority')"
      >
        <b-form-select
        id = "priority"
        v-model="data.priority"
        :options="select.options"
        :state="getValidationState('priority')"
        >
        </b-form-select>
      </b-form-group>

      <template v-if=!editEmail name="buttons">
        <div class="row">
          <div
            id="col-exp-buttons"
            class="col"
          >
            <b-button
              variant="success"
              @click="saveNewEmail"
              :disabled="isSaveDisabled"
            >
              Save
            </b-button>
            <b-button
              variant="primary"
              @click="cancelNewEmail"
            >
              Cancel
            </b-button>
          </div>
        </div>
      </template>
    </b-form>
  </div>
</template>
<style>
.my-class {
  width: 250px;
}
</style>
<script>
import { models } from "django-airavata-api";
import { mixins, utils } from "django-airavata-common-ui";
import { Datetime } from 'vue-datetime';
import moment from "moment";
import 'vue-datetime/dist/vue-datetime.css'

export default {
  name: "email-editor",
  components: {
    datetime: Datetime
  },
  mixins: [mixins.VModelMixin],
  props: {
    value: {
      type: models.Email,
      required: true
    }
  },
  created() {
    //checks whether the component is used for editing or updating the email
    if(this.value.emailID != null){
      this.editEmail = true;
      this.inputPublishedTime = new moment(this.value.publishedTime.toISOString()).utc().format()
      this.inputExpirationTime = new moment(this.value.expirationTime.toISOString()).utc().format()
      this.data.priority = this.value.priority.name;
      this.today = new moment(this.value.expirationTime.toISOString()).format();
    }
  },
  data() {
    return {
      editEmail: false,
      userBeginsInput: false,
      inputPublishedTime: null,
      inputExpirationTime: null,
      today: new moment().format(),
      select : {
          selected: "LOW",
          options: [
              { text: "LOW", value: "LOW" },
              { text: "NORMAL", value: "NORMAL" },
              { text: "HIGH", value: "HIGH" }
            ]
      }
    };
  },
  computed: {
    valid: function() {
      const validation = this.data.validate();
      return (
        Object.keys(validation).length === 0
      );
    },
    isSaveDisabled: function() {
      return !this.valid;
    }
  },
  methods: {
    onUserInput() {
      this.userBeginsInput = true;
      return this.$emit("userBeginsInput");
    },
    reset() {
      this.userBeginsInput = false;
    },
    getValidationFeedback: function(properties) {
      return utils.getProperty(this.data.validate(), properties);
    },
    getValidationState: function(properties) {
      if (this.userBeginsInput == false){
        return null;
      }
      return this.getValidationFeedback(properties) ? "invalid" : "valid";
    },
    cancelNewEmail() {
      return this.$emit("cancelNewEmail");
    },
    saveNewEmail() {
      return this.$emit("saveNewEmail");
    }
  },
  watch: {
    inputExpirationTime() {
      this.data.expirationTime = this.inputExpirationTime;

    },
    inputPublishedTime() {
      this.data.publishedTime = this.inputPublishedTime;
    }

  }
};
</script>
