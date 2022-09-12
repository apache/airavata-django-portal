
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
        <b-button>         <b-card-text :value="experimentStatistics.runningExperimentCount" :states="runningStates"  @click="selectExperiments('runningExperiments')">Running : {{experimentStatistics.runningExperimentCount || 0}}</b-card-text></b-button>
      <b-button>  <b-card-text :value ="experimentStatistics.allExperimentCount" @click="selectExperiments('allExperiments')">All : {{experimentStatistics.allExperimentCount || 0}}</b-card-text> </b-button>
        <b-button>   <b-card-text :value="experimentStatistics.cancelledExperimentCount" :states="canceledStates" @click="selectExperiments('cancelledExperiments')">Cancelled :{{experimentStatistics.cancelledExperimentCount || 0}}</b-card-text> </b-button>
          <b-button>   <b-card-text :value="experimentStatistics.failedExperimentCount" :states="failedStates" @click="selectExperiments('failedExperiments')">Failed : {{experimentStatistics.failedExperimentCount || 0}}</b-card-text> </b-button>
            <b-button>  <b-card-text :value="experimentStatistics.completedExperimentCount" :states="completedStates" @click="selectExperiments('completedExperiments')">Completed : {{experimentStatistics.completedExperimentCount || 0}}</b-card-text> </b-button>
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
  <div class="row" v-if="items.length > 0">
            <div class="col">
              <b-card>
                <b-table :fields="fields" :items="items">
                  <template slot="cell(executionId)" slot-scope="data">
                    <application-name :application-interface-id="data.value" />
                  </template>
                  <template slot="cell(actions)" slot-scope="data">
                    <b-link
                      @click="showExperimentDetails(data.item.experimentId)"
                    >
                      View Details
                      <i class="far fa-chart-bar" aria-hidden="true"></i>
                    </b-link>
                  </template>
                </b-table>
              </b-card>
              <pager
                v-if="experimentStatistics.allExperimentCount > 0"
                :paginator="experimentStatisticsPaginator"
                @next="experimentStatisticsPaginator.next()"
                @previous="experimentStatisticsPaginator.previous()"
              ></pager>
            </div>
          </div>

  <div class="mt-3">
    <b-card-group deck class="mb-3">
      <b-card border-variant="dark" header="No of user with single job" class="text-center">
        <b-card-text :value="uniqueUsersWithJob">
          Unique users with atleast single job : {{uniqueUsersWithJob}}
        </b-card-text>
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
import { models, services, session, utils } from "django-airavata-api";
import BarChart from './AdminDashboardContainer.vue';
import ExperimentDetailsView from "../statistics/ExperimentDetailsView.vue";
import ExperimentStatisticsCard from "../statistics/ExperimentDetailsView.vue";
import { components } from "django-airavata-common-ui";

export default {
  components: {
    BarChart,
    ExperimentDetailsView,
    ExperimentStatisticsCard,
    "application-name": components.ApplicationName,
    "compute-resource-name": components.ComputeResourceName,
    "human-date": components.HumanDate,
    "experiment-status-badge": components.ExperimentStatusBadge,
    pager: components.Pager,
  },
  name: "admin-dashboard-container",
  computed: {
    experimentStatistics() {
      return this.experimentStatisticsPaginator
        ? this.experimentStatisticsPaginator.results
        : {};
    },
    allExperimentStatisticsFetcher() {
      return this.allExperimentStatisticsPaginator
        ? this.allExperimentStatisticsPaginator.results
        : {};
    },
    createdStates() {
      // TODO: moved to ExperimentStatistics model
      return [models.ExperimentState.CREATED, models.ExperimentState.VALIDATED];
    },
    runningStates() {
      return [
        models.ExperimentState.SCHEDULED,
        models.ExperimentState.LAUNCHED,
        models.ExperimentState.EXECUTING,
      ];
    },
    completedStates() {
      return [models.ExperimentState.COMPLETED];
    },
    canceledStates() {
      return [
        models.ExperimentState.CANCELING,
        models.ExperimentState.CANCELED,
      ];
    },
    failedStates() {
      return [models.ExperimentState.FAILED];
    },
    fields() {
      return [
        {
          key: "name",
          label: "Name",
        },
        {
          key: "userName",
          label: "Owner",
        },
        {
          key: "executionId",
          label: "Application",
        },
        {
          key: "resourceHostId",
          label: "Resource",
        },
        {
          key: "creationTime",
          label: "Creation Time",
        },
        {
          key: "experimentStatus",
          label: "Status",
        },
        {
          key: "actions",
          label: "Actions",
        },
      ];
    },
    items() {
      if (this.selectedExperimentSummaries) {
        return this.selectedExperimentSummaries;
      } else {
        return [];
      }
    },
    fromTimeDisplay() {
      return moment(this.fromTime).format("MMM Do YYYY");
    },
    toTimeDisplay() {
      return moment(this.toTime).format("MMM Do YYYY");
    },
    selectedExperimentSummaries() {
      if (
        this.selectedExperimentSummariesKey &&
        this.experimentStatistics &&
        this.selectedExperimentSummariesKey in this.experimentStatistics
      ) {
        return this.experimentStatistics[this.selectedExperimentSummariesKey];
      } else {
        return [];
      }
    },
    applicationNameOptions() {
      if (this.appInterfaces) {
        const options = this.appInterfaces.map((appInterface) => {
          return {
            value: appInterface.applicationInterfaceId,
            text: appInterface.applicationName,
          };
        });
        return utils.StringUtils.sortIgnoreCase(options, (o) => o.text);
      } else {
        return [];
      }
    },
    hostnameOptions() {
      if (this.computeResourceNames) {
        const options = this.computeResourceNames.map((name) => {
          return {
            value: name.host_id,
            text: name.host,
          };
        });
        return utils.StringUtils.sortIgnoreCase(options, (o) => o.text);
      } else {
        return [];
      }
    },
    selectedExperimentsTabTitle() {
      if (this.selectedExperimentSummariesKey === "allExperiments") {
        return "All Experiments";
      } else if (this.selectedExperimentSummariesKey === "createdExperiments") {
        return "Created Experiments";
      } else if (this.selectedExperimentSummariesKey === "runningExperiments") {
        return "Running Experiments";
      } else if (
        this.selectedExperimentSummariesKey === "completedExperiments"
      ) {
        return "Completed Experiments";
      } else if (
        this.selectedExperimentSummariesKey === "cancelledExperiments"
      ) {
        return "Cancelled Experiments";
      } else if (this.selectedExperimentSummariesKey === "failedExperiments") {
        return "Failed Experiments";
      } else {
        return "Experiments";
      }
    },
  },
  data() {
    const fromTime = new Date().fp_incr(0);
    const toTime = new Date().fp_incr(1);
    return {
      experimentStatisticsPaginator: null,
      allExperimentStatisticsPaginator: null,
      selectedExperimentSummariesKey: null,
      allExperimentStatisticsList: [],
      uniqueUsersWithJob: 0,
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
      experimentDetails: [],
    }
  },
  created() {
    this.uniqueUserProfileCount(this.fromTime, this.toTime);
    this.loadStatistics(this.fromTime, this.toTime);
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
    async dateRangeChanged(selectedDates) {
      [this.fromTime, this.toTime] = selectedDates;
      if (this.fromTime && this.toTime) {
        await this.uniqueUserProfileCount(this.fromTime, this.toTime);
        await this.loadStatistics(this.fromTime, this.toTime);
        await this.allExperimentStatistics(this.fromTime, this.toTime);
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
    async loadStatistics(from, to) {
       const requestData = {
        fromTime: from.toJSON(),
        toTime:to.toJSON(),
      };
      let result =  await services.ExperimentStatisticsService.get(requestData).then(
        (stats) => {
          this.experimentStatisticsPaginator = stats;
        }
      );
      return result;
    },

    async allExperimentStatistics(from, to) {
      const requestData = {
        fromTime: from.toJSON(),
        toTime:to.toJSON(),
      };
      let results =  await services.ExperimentStatisticsService.get(requestData).then(
        (stats) => {
          console.log(stats);
          this.allExperimentStatisticsPaginator = stats;
        }
      );      
      while (this.allExperimentStatisticsPaginator._next) {
        this.allExperimentStatisticsFetcher.allExperiments.map((item) =>  this.allExperimentStatisticsList.push(item));
        await this.allExperimentStatisticsPaginator.next();
      }
      if (this.allExperimentStatisticsPaginator._next == null) {
        this.allExperimentStatisticsFetcher.allExperiments.map((item) =>  this.allExperimentStatisticsList.push(item));
      }

      let uniqueUsers = new Set();
      
      this.allExperimentStatisticsList.forEach((item) => {
        uniqueUsers.add(item.userName);
      });

      this.uniqueUsersWithJob = uniqueUsers.size;
      console.log("Unique Job", this.uniqueUsersWithJob);
      return results;
    },

    showExperimentDetails(experimentId) {
      const expDetailsIndex = this.getExperimentDetailsIndex(experimentId);
      if (expDetailsIndex >= 0) {
        this.selectExperimentDetailsTab(experimentId);
      } else {
        // TODO: maybe don't need to load the experiment first since ExperimentDetailsView will load FullExperiment?
        services.ExperimentService.retrieve({
          lookup: experimentId,
        }).then((exp) => {
          this.experimentDetails.push(exp);
          this.selectExperimentDetailsTab(experimentId);
          this.scrollTabsIntoView();
        });
      }
    },
    selectExperimentDetailsTab(experimentId) {
      const expDetailsIndex = this.getExperimentDetailsIndex(experimentId);
      // Note: running this in $nextTick doesn't work, but setTimeout does
      // (see also https://github.com/bootstrap-vue/bootstrap-vue/issues/1378#issuecomment-345689470)
      setTimeout(() => {
        // Add 1 to the index because the first tab has the overall statistics
        this.activeTabIndex = expDetailsIndex + 1;
      }, 1);
    },
    getExperimentDetailsIndex(experimentId) {
      return this.experimentDetails.findIndex(
        (e) => e.experimentId === experimentId
      );
    },
    removeExperimentDetails(experimentId) {
      const index = this.getExperimentDetailsIndex(experimentId);
      this.experimentDetails.splice(index, 1);
    },
    scrollTabsIntoView() {
      this.$refs.tabs.$el.scrollIntoView({ behavior: "smooth" });
    },
    selectExperiments(experimentSummariesKey) {
      if (
        this.experimentStatisticsPaginator &&
        this.experimentStatisticsPaginator.offset > 0
      ) {
        this.loadStatistics(this.fromTime, this.toTime);
      }
      this.selectedExperimentSummariesKey = experimentSummariesKey;
    },
  },
};

</script>
<style>
.temp{
  width:206px;
}
</style>
