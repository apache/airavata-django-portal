<template>
    <div>
        <b-card header="Experiments count grouped by applications">
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
                            <template slot="cell(applicationName)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(allExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(runningExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(completedExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(cancelledExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(failedExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                            <template slot="cell(createdExperimentCount)" slot-scope="data">
                                {{ data.value }}
                            </template>
                        </b-table>
                    </b-card>
                </div>
            </div>
        </b-card>
        <b-card header="CPU hours used by application within the selected period">
            <div class="w-50">
                <BarChart :chart-data="cpuHoursConsumedByApplication" />
            </div>
        </b-card>
    </div>
</template>

<script>
import { services } from "django-airavata-api";
import { components } from "django-airavata-common-ui";

import moment from "moment";

export default {
    name: 'application-statistics-container',
    data() {
        const fromTime = new Date().fp_incr(0);
        const toTime = new Date().fp_incr(1);
        return {
            fromTime: fromTime,
            toTime: toTime,
            dateRange: [fromTime, toTime],
            items: [],
            appInterfaces: null,
            cpuUsages: null,
            dateConfig: {
                mode: "range",
                wrap: true,
                dateFormat: "Y-m-d",
                maxDate: new Date().fp_incr(1),
            },
        };
    },
    components: {
        BarChart: components.BarChart,
    },
    created() {
        this.loadappInterfaces();
        this.loadCpuUsages();
        this.loadStatistics();
    },
    computed: {
        fields() {
            return [
                {
                    key: "applicationName",
                    label: "Application",
                },
                {
                    key: "allExperimentCount",
                    label: "All Experiment",
                },
                {
                    key: "runningExperimentCount",
                    label: "Running Experiment",
                },
                {
                    key: "completedExperimentCount",
                    label: "Completed Experiment",
                },
                {
                    key: "cancelledExperimentCount",
                    label: "Cancelled Experiment",
                },
                {
                    key: "failedExperimentCount",
                    label: "Failed Experiment",
                },
                {
                    key: "createdExperimentCount",
                    label: "Created Experiment",
                },
            ];
        },
        cpuHoursConsumedByApplication() {
            let cpuUsageMap = new Map();
            if(this.appInterfaces) this.appInterfaces.forEach(({applicationInterfaceId}) => cpuUsageMap.set(applicationInterfaceId, 0));
            if(this.cpuUsages){
                this.cpuUsages.forEach(({executionId, cpuHours}) => {
                    cpuUsageMap.set(executionId, cpuHours + (cpuUsageMap.has(executionId) ? cpuUsageMap.get(executionId) : 0));
                });
            }

            let cpuUsageSortedList = Array.from(cpuUsageMap.keys()).map((applicationInterfaceId) => {
                return {
                    applicationInterfaceId,
                    cpuHours: cpuUsageMap.get(applicationInterfaceId),
                };
            }).sort((a, b) => b.cpuHours - a.cpuHours);

            if(cpuUsageSortedList.length > 11){
                const firstTenApplications = cpuUsageSortedList.slice(0, 10);
                const remainingApplications = cpuUsageSortedList.slice(10, cpuUsageSortedList.length);
                const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
                const remainingAvgUsage = Math.floor(average(remainingApplications.map(({cpuHours}) => cpuHours)));
                cpuUsageSortedList = [...firstTenApplications, {applicationInterfaceId: "Avg of other " + remainingApplications.length + " applications", cpuHours: remainingAvgUsage}]
            }
            let appInterfaceNameMap = new Map();
            if (this.appInterfaces)
                this.appInterfaces.forEach(({applicationInterfaceId, applicationName}) => appInterfaceNameMap.set(applicationInterfaceId, applicationName));
            const keys = cpuUsageSortedList.map(({applicationInterfaceId}) => appInterfaceNameMap.get(applicationInterfaceId));
            const values = cpuUsageSortedList.map(({cpuHours}) => cpuHours);
            return this.mapToBarChartData(keys, values);
        },
    },
    methods: {
        dateRangeChanged(selectedDates) {
            [this.fromTime, this.toTime] = selectedDates;
            if (this.fromTime && this.toTime) {
                this.loadStatistics();
            }
        },
        loadappInterfaces() {
            services.ApplicationInterfaceService.list().then(
                (appInterfaces) => {
                    this.appInterfaces = appInterfaces;
                }
            );
        },
        loadStatistics() {
            let appInterfaceList = this.appInterfaces ? this.appInterfaces : [];
            
            const requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            return services.ExperimentStatisticsService.get(requestData).then(
                (stats) => {
                    let results = stats ? stats.results : {};
                    const allExperiments = "allExperiments" in results ? results["allExperiments"] : [];
                    const runningExperiments = "runningExperiments" in results ? results["runningExperiments"] : [];
                    const completedExperiments = "completedExperiments" in results ? results["completedExperiments"] : [];
                    const failedExperiments = "failedExperiments" in results ? results["failedExperiments"] : [];
                    const cancelledExperiments = "cancelledExperiments" in results ? results["cancelledExperiments"] : [];
                    const createdExperiments = "createdExperiments" in results ? results["createdExperiments"] : [];
                    this.items = appInterfaceList.map(({ applicationInterfaceId, applicationName }) => {
                        return {
                            applicationName,
                            allExperimentCount: allExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            runningExperimentCount: runningExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            completedExperimentCount: completedExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            failedExperimentCount: failedExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            cancelledExperimentCount: cancelledExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            createdExperimentCount: createdExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                        }
                    });

                }
            );
        },
        loadCpuUsages() {
            const requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            services.CpuUsageService.getCpuUsages(requestData).then(
                (cpuUsages) => {
                    this.cpuUsages = cpuUsages;
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
        mapToBarChartData(keys, values) {
            return {
                labels: keys,
                datasets: [
                    {
                        label: 'No. of Applications',
                        data: values,
                        backgroundColor: '#FFC0CB'
                    }
                ]
            };
        },
    }
}
</script>