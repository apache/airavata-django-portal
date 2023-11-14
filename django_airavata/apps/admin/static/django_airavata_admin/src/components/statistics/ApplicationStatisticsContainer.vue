<template>
    <div>
        <b-card header="Experiments count grouped by applications within the selected period">
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

export default {
    name: 'application-statistics-container',
    props: {
        fromTime: {
            type: Date,
            required: true,
        },
        toTime: {
            type: Date,
            required: true,
        }
    },
    data() {
        return {
            items: [],
            appInterfaces: null,
            cpuUsages: null,
        };
    },
    components: {
        BarChart: components.BarChart,
    },
    created() {
        this.loadAppInterfaces();
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
            const keys = cpuUsageSortedList.map(({applicationInterfaceId}) => appInterfaceNameMap.get(applicationInterfaceId) ? appInterfaceNameMap.get(applicationInterfaceId) : applicationInterfaceId);
            const values = cpuUsageSortedList.map(({cpuHours}) => cpuHours);
            return this.mapToBarChartData(keys, values);
        },
    },
    watch: {
        fromTime() {
            this.reloadAfterPropsChange();
        },
        toTime() {
            this.reloadAfterPropsChange();
        }
    },
    methods: {
        reloadAfterPropsChange() {
            if (this.fromTime && this.toTime) {
                this.loadCpuUsages();
                this.loadStatistics();
            }
        },
        loadAppInterfaces() {
            services.ApplicationInterfaceService.list().then(
                (appInterfaces) => {
                    this.appInterfaces = appInterfaces;
                }
            );
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
                    const runningExperiments = "runningExperiments" in results ? results["runningExperiments"] : [];
                    const completedExperiments = "completedExperiments" in results ? results["completedExperiments"] : [];
                    const failedExperiments = "failedExperiments" in results ? results["failedExperiments"] : [];
                    const cancelledExperiments = "cancelledExperiments" in results ? results["cancelledExperiments"] : [];
                    const createdExperiments = "createdExperiments" in results ? results["createdExperiments"] : [];
                    this.items = this.appInterfaces ? this.appInterfaces.map(({ applicationInterfaceId, applicationName }) => {
                        return {
                            applicationName,
                            allExperimentCount: allExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            runningExperimentCount: runningExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            completedExperimentCount: completedExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            failedExperimentCount: failedExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            cancelledExperimentCount: cancelledExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                            createdExperimentCount: createdExperiments.filter(({ executionId }) => executionId === applicationInterfaceId).length,
                        }
                    }) : [];

                }
            );
        },
        loadCpuUsages() {
            const requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            services.CpuUsageService.get(requestData).then(
                (cpuUsages) => {
                    this.cpuUsages = cpuUsages;
                }
            );
        },
        mapToBarChartData(keys, values) {
            return {
                labels: keys,
                datasets: [
                    {
                        label: 'CPU Hours',
                        data: values,
                        backgroundColor: '#FFC0CB'
                    }
                ]
            };
        },
    }
}
</script>