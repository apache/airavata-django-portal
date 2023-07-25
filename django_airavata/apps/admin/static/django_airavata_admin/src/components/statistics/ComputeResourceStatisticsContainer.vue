<template>
    <b-card header="Compute Resource with Atleast one Job Submitted">
        <div class="row">
            <div class="col">
                <b-card header="Filter Options">
                    <b-input-group class="w-100 mb-2">
                        <b-input-group-prepend is-text>
                            <i class="fa fa-calendar-week" aria-hidden="true"></i>
                        </b-input-group-prepend>
                        <flat-pickr :value="dateRange" :config="dateConfig" @on-change="dateRangeChanged"
                            class="form-control" />
                        <b-input-group-append>
                            <b-button @click="getPast24Hours" variant="outline-secondary">Past 24 Hours</b-button>
                            <b-button @click="getPastWeek" variant="outline-secondary">Past Week</b-button>
                        </b-input-group-append>
                    </b-input-group>
                    <template slot="footer">
                        <div class="d-flex justify-content-end">
                            <b-button @click="loadStatistics" class="ml-auto" variant="primary">Get
                                Statistics</b-button>
                        </div>
                    </template>
                </b-card>
            </div>
        </div>
        <div class="row" v-if="items.length > 0">
            <div class="col">
                <b-card>
                    <b-table :fields="fields" :items="items">
                        <template slot="cell(resourceHostId)" slot-scope="data">
                            <compute-resource-name :compute-resource-id="data.value" />
                        </template>
                        <template slot="cell(numberOfJobs)" slot-scope="data">
                            {{ data.item.numberOfJobs }}
                        </template>
                    </b-table>
                </b-card>
            </div>
        </div>
    </b-card>
</template>

<script>
import { services } from "django-airavata-api";
import { components } from "django-airavata-common-ui";

import moment from "moment";

export default {
    name: 'compute-resource-statistics-container',
    data() {
        const fromTime = new Date().fp_incr(0);
        const toTime = new Date().fp_incr(1);
        return {
            fromTime: fromTime,
            toTime: toTime,
            dateRange: [fromTime, toTime],
            items: [],
            dateConfig: {
                mode: "range",
                wrap: true,
                dateFormat: "Y-m-d",
                maxDate: new Date().fp_incr(1),
            },
        };
    },
    created() {
        this.loadStatistics();
    },
    components: {
        "compute-resource-name": components.ComputeResourceName,
    },
    computed: {
        fields() {
            return [
                {
                    key: "resourceHostId",
                    label: "ResourceHostId",
                },
                {
                    key: "numberOfJobs",
                    label: "NumberOfJobs",
                },
            ];
        }
    },
    methods: {
        dateRangeChanged(selectedDates) {
            [this.fromTime, this.toTime] = selectedDates;
            if (this.fromTime && this.toTime) {
                this.loadStatistics();
            }
        },
        loadStatistics() {
            const requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            return services.ExperimentStatisticsService.get(requestData).then(
                (stats) => {
                    let results = stats ? stats.results : {};
                    const allExperiments = "allExperiments" in results ? results["allExperiments"] : [];
                    const allresourceHostIds = allExperiments.map(item => item.resourceHostId);
                    const cnt = new Map();
                    allresourceHostIds.forEach(resourceHostId => {
                        cnt.has(resourceHostId) ? cnt.set(resourceHostId, cnt.get(resourceHostId) + 1) : cnt.set(resourceHostId, 1);
                    });
                    this.items = [];
                    cnt.forEach((numberOfJobs, resourceHostId) => {
                        this.items.push({ "resourceHostId": resourceHostId, "numberOfJobs": numberOfJobs });
                    });
                }
            );
        },
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
    }
};
</script>