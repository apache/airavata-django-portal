
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
      <div>
  <b-dropdown id="dropdown-1" text="week" class="m-md-2">
    <b-dropdown-item>week</b-dropdown-item>
    <b-dropdown-item>Month</b-dropdown-item>
    <b-dropdown-item>15 days</b-dropdown-item>
  </b-dropdown>
</div>
<span>Start Date:</span>
     <b-form-datepicker class="m-md-2 temp"
      id="ex-disabled-readonly"
      :disabled="disabled"
      :readonly="readonly"
    ></b-form-datepicker>
    <span>End Date:</span>
     <b-form-datepicker class="m-md-2 temp" 
      id="ex-disabled-readonly"
      :disabled="disabled"
      :readonly="readonly"
    ></b-form-datepicker>
    <button>Submit</button>
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
        <b-card-text></b-card-text>
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

import BarChart from './AdminDashboardContainer.vue';
export default {
  components: { BarChart },
  name: "admin-dashboard-container",
};

</script>
<style>
.temp{
  width:206px;
}
</style>
