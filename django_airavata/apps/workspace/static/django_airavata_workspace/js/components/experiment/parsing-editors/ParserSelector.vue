<template>
  <div>
    <b-form-group>
      <b-form-checkbox-group
        v-model="selected"
        :options="templateOptions"
        name="flavour-2a"
        stacked
      ></b-form-checkbox-group>
    </b-form-group>

  </div>
</template>

<script>

import { services } from "django-airavata-api";

export default {
  name: "parser-selector",
  props: {
    appId: {
      type: String,
      required: true
    }
  },

  mounted() {
    services.ParsingTemplateService.getTemplatesForApplication(
      { lookup: this.appId }
    ).then(templates => {
      for (var temp in templates) {
        this.templateOptions.push({ text: templates[temp].id , value: temp.id });
      }
    });
  },

  data() {
    return {
      selected: [], // Must be an array reference!
      templateOptions: []
    }
  },
}

</script>