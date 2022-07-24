<template>
  <div>
    <div class="row">
      <div class="col">
        <h1 class="h4 mb-4">Admin Dashboard</h1>
      </div>
    </div> 
  </div>
</template>
<script>
import { models, services, utils } from "django-airavata-api";
import { components } from "django-airavata-common-ui";
import ExperimentStatisticsCard from "./ExperimentStatisticsCard";
import ExperimentDetailsView from "./ExperimentDetailsView";

import moment from "moment";

export default {
  name: "admin-dashboard-container",
};
</script>
