
<template>
  <div>
    <div class="row">
      <div class="col">
        <h1 class="h4 mb-4">Admin Dashboard</h1>
      </div>
    </div> 
    <div>
  <div>
    <b-card >
      <div>
        <h1 class ="h4 mb-4 ">Duration</h1>
      </div>
      <b-input-group class="w-100 mb-2">
      <b-input-group-prepend is-text>
        <i class="fa fa-calendar-week" aria-hidden="true"></i>
      </b-input-group-prepend>
      <flat-pickr
        :value="dateRange"
        :config="dateConfig"
        @on-change="dateRangeChanged"
        class="form-control"
      />
      <b-input-group-append>
        <b-button
          @click="getPast24Hours"
          variant="outline-secondary"
          >Past 24 Hours</b-button
        >
        <b-button @click="getPastWeek" variant="outline-secondary"
          >Past Week</b-button
        >
      </b-input-group-append>
    </b-input-group>

      <b-button>Submit</b-button>
    </b-card>
  </div>
  <div>
    <b-card header="Load experiment details by experiment id">
      <b-form-group>
        <b-input-group>
          <b-form-input
            v-model="experimentId"
            placeholder="Experiment ID"
            
          />
          <b-input-group-append>
            <b-button
              :disabled="!experimentId"
              
              variant="primary"
              >Load</b-button
            >
          </b-input-group-append>
        </b-input-group>
      </b-form-group>
    </b-card>
  </div>
  <div>
    <b-card-group deck>
      <b-card
        border-variant="primary"
        header="Cpu hour used by the user"
        header-bg-variant="primary"
        header-text-variant="black"
        align="center"
      >
      <bar-chart/>
    
  
        <b-card-text>xxx</b-card-text>
      </b-card>

      <b-card
        border-variant="secondary"
        header="CPU hours by application"
        header-border-variant="secondary"
        align="center"
      >
        <b-card-text></b-card-text>
      </b-card>

      <b-card border-variant="success" header="Experiments by Experiment status" align="center">
        <b-card-text></b-card-text>
      </b-card>
    </b-card-group>
  </div>
  <div class="mt-3">
    <b-card-group deck>
      <b-card border-variant="info" header="Group with job per user" align="center">
        <b-card-text></b-card-text>
      </b-card>

      <b-card
        border-variant="warning"
        header="User registration trend per day"
        header-bg-variant="transparent"
        align="center"
      >
        <b-card-text></b-card-text>
      </b-card>

      <b-card
        border-variant="danger"
        header="Total no of unique users"
        header-border-variant="danger"
        header-text-variant="danger"
        align="center"
      >
        <b-card-text :value="uniqueUsersCount">
          {{uniqueUsersCount}} 
        </b-card-text>
      </b-card>
    </b-card-group>
  </div>
  <div class="mt-3">
    <b-card-group deck class="mb-3">
      <b-card border-variant="light" header="No of user with single job" class="text-center">
        <b-card-text></b-card-text>
      </b-card>

      <b-card border-variant="dark" header="Job with different status" align="center">
        <b-card-text></b-card-text>
      </b-card>
    </b-card-group>
  </div>
</div>
   
  </div>
</template>

<script>

import moment from "moment";
import { services, session, utils } from "django-airavata-api";
import BarChart from './AdminDashboardContainer.vue';

export default {
  components: { BarChart },
  name: "admin-dashboard-container",
  data() {
    const fromTime = new Date().fp_incr(0);
    const toTime = new Date().fp_incr(1);
    return {
      fromTime: fromTime,
      toTime: toTime,
      dateRange: [fromTime, toTime],
      uniqueUsersCount: 0,
      dateConfig: {
        mode: "range",
        wrap: true,
        dateFormat: "Y-m-d",
        maxDate: new Date().fp_incr(1),
      },
    }
  },
  created() {
    this.uniqueUserProfileCount(this.fromTime, this.toTime);
  },
  methods: {
    getPast24Hours() {
      this.fromTime = new Date().fp_incr(0);
      //this.fromTime = new Date(this.fromTime.setHours(0,0,0));
      this.toTime = new Date().fp_incr(1);
      this.updateDateRange();
    },
    getPastWeek() {
      this.fromTime = new Date().fp_incr(-7);
      this.toTime = new Date().fp_incr(1);
      this.updateDateRange();
    },
    updateDateRange() {
      this.dateRange = [
        moment(this.fromTime).format("YYYY-MM-DD"),
        moment(this.toTime).format("YYYY-MM-DD"),
      ];
    },
    daysAgo(days) {
      return new Date(Date.now() - days * 24 * 60 * 60 * 1000);
    },
    fromTimeDisplay() {
      return moment(this.fromTime).format("MMM Do YYYY");
    },
    toTimeDisplay() {
      return moment(this.toTime).format("MMM Do YYYY");
    },
    dateRangeChanged(selectedDates) {
      [this.fromTime, this.toTime] = selectedDates;
      if (this.fromTime && this.toTime) {
        this.uniqueUserProfileCount(this.fromTime, this.toTime);
      }
    },
    uniqueUserCountDisplay() {
      return String(this.userCount)
    }, 
    async uniqueUserProfileCount(from, to) {
      let fromTime = from.toJSON();
      let toTime = to.toJSON();
      const response = await services.UserProfileService.list();
      let filteredUsers = new Set();
      fromTime = new Date(Date.parse(fromTime)).getTime();
      toTime = new Date(Date.parse(toTime)).getTime();
      response.forEach((user) => {
        var uct = user.creationTime.getTime();
        if (uct == undefined) {
          uct = new Date();
        }
        if (uct < toTime && uct > fromTime) {
          filteredUsers.add(user.userId);
        }
      });
      this.uniqueUsersCount = filteredUsers.size;
    },
  },
};

</script>
<style>
.temp{
  width:206px;
}
</style>
