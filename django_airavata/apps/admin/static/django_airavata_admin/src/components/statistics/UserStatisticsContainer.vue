<template>
    <div>
        <b-card header="Users who submitted at least a single job">
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
                                <b-button @click="loadStatistics" class="ml-auto" variant="primary">
                                    Get Statistics
                                </b-button>
                            </div>
                        </template>
                    </b-card>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <b-card>
                        <b-card-text>
                            Number of users who submitted at least a single job: {{ countOfUsersWithAtLeastSingleJob }}
                        </b-card-text>
                        <b-link @click="downloadUsersWithAtLeastSingleJobEmailCsv">
                            <i class="fas fa-download"></i>
                            Download emails.csv
                        </b-link>
                    </b-card>
                </div>
            </div>
        </b-card>
        <b-card header="All Users">
            <div class="row">
                <div class="col">
                    <b-card>
                        <b-card-text>Total number of unique users: {{ countOfAllUsers }}</b-card-text>
                        <b-link @click="downloadAllUserEmailCsv">
                            <i class="fas fa-download"></i>
                            Download emails.csv
                        </b-link>
                    </b-card>
                </div>
            </div>
        </b-card>
        <b-card header="User Registration Trends">
            <div class="row">
                <div class="col-md-5">
                    <b-card header="Monthwise User Registration Trend">
                        <PieChart :chart-data="userGroupedByCreationMonth" />
                    </b-card>
                </div>
                <div class="col-md-2"></div>
                <div class="col-md-5">
                    <b-card header="Yearwise User Registration Trend">
                        <b-card-text>Only years with atleast 1 registration are shown</b-card-text>
                        <BarChart :chart-data="userGroupedByCreaionYear" />
                    </b-card>
                </div>
            </div>
            <div class="row">
                <div class="col-md-5">
                    <b-card header="Organizationwise User Registration Trend">
                        <b-card-text>Only organizations with atleast 1 registration are shown</b-card-text>
                        <PieChart :chart-data="userGroupedByHomeOrg" />
                    </b-card>
                </div>
                <div class="col-md-2"></div>
                <div class="col-md-5">
                    <b-card header="Countrywise User Registration Trend">
                        <b-card-text>Only countries with atleast 1 registration are shown</b-card-text>
                        <BarChart :chart-data="userGroupedByCountry" />
                    </b-card>
                </div>
            </div>
        </b-card>
        <b-card header="CPU hours used by user within the selected period">
            <div class="w-50">
                <BarChart :chart-data="cpuHoursConsumedByUser" />
            </div>
        </b-card>
    </div>
</template>

<script>
import { services } from "django-airavata-api";
import { components } from "django-airavata-common-ui";

import moment from "moment";

export default {
    name: 'user-statistics-container',
    data() {
        const fromTime = new Date().fp_incr(0);
        const toTime = new Date().fp_incr(1);
        return {
            fromTime: fromTime,
            toTime: toTime,
            dateRange: [fromTime, toTime],
            countOfUsersWithAtLeastSingleJob: null,
            userWithAtLeastSingleJobEmailList: [],
            userProfiles: [],
            countOfAllUsers: null,
            allUserEmailList: [],
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
        PieChart: components.PieChart,
        BarChart: components.BarChart,
    },
    computed: {
        userGroupedByCreationMonth() {
            let countOfUserCreatedEachMonth = new Array(12).fill(0);
            if (this.userProfiles) {
                this.userProfiles.forEach(({ creationTime }) => {
                    const idx = (new Date(creationTime)).getMonth();
                    if (idx) countOfUserCreatedEachMonth[idx]++;
                });
            }
            return {
                labels: this.getMonthNameList(),
                datasets: [
                    {
                        data: countOfUserCreatedEachMonth,
                        backgroundColor: this.getBackgroundColorListForMonths(),
                    }
                ],
            };
        },
        userGroupedByCreaionYear() {
            let userCountMap = new Map();
            if (this.userProfiles) {
                this.userProfiles.forEach(({ creationTime }) => {
                    const year = (new Date(creationTime)).getFullYear();
                    if (year) {
                        userCountMap.set(year, 1 +
                            (userCountMap.has(year) ? userCountMap.get(year) : 0));
                    }
                });
            }
            const keys = Array.from(userCountMap.keys()).sort();
            const values = keys.map((key) => userCountMap.get(key))
            return this.mapToBarChartData(keys, values);
        },
        userGroupedByCountry() {
            let userCountMap = new Map();
            if (this.userProfiles) {
                this.userProfiles.forEach(({ country }) => {
                    if (country) {
                        userCountMap.set(country, 1 +
                            (userCountMap.has(country) ? userCountMap.get(country) : 0));
                    }
                });
            }
            const keys = Array.from(userCountMap.keys());
            const values = keys.map((key) => userCountMap.get(key))
            return this.mapToBarChartData(keys, values);
        },
        userGroupedByHomeOrg() {
            let userCountMap = new Map();
            if (this.userProfiles) {
                this.userProfiles.forEach(({ homeOrganization }) => {
                    if (homeOrganization) {
                        userCountMap.set(homeOrganization, 1 +
                            (userCountMap.has(homeOrganization) ? userCountMap.get(homeOrganization) : 0));
                    }
                });
            }
            const keys = Array.from(userCountMap.keys());
            const values = keys.map((key) => userCountMap.get(key))
            return this.mapToBarChartData(keys, values);
        },
        cpuHoursConsumedByUser() {
            let cpuUsageMap = new Map();
            if(this.userProfiles) this.userProfiles.forEach(({userId}) => cpuUsageMap.set(userId, 0));
            if(this.cpuUsages){
                this.cpuUsages.forEach(({userName, cpuHours}) => {
                    cpuUsageMap.set(userName, cpuHours + (cpuUsageMap.has(userName) ? cpuUsageMap.get(userName) : 0));
                });
            }

            let cpuUsageSortedList = Array.from(cpuUsageMap.keys()).map((userId) => {
                return {
                    userId,
                    cpuHours: cpuUsageMap.get(userId),
                };
            }).sort((a, b) => b.cpuHours - a.cpuHours);

            if(cpuUsageSortedList.length > 11){
                const firstTenUsers = cpuUsageSortedList.slice(0, 10);
                const remainingUsers = cpuUsageSortedList.slice(10, cpuUsageSortedList.length);
                const average = arr => arr.reduce( ( p, c ) => p + c, 0 ) / arr.length;
                const remainingAvgUsage = Math.floor(average(remainingUsers.map(({cpuHours}) => cpuHours)));
                cpuUsageSortedList = [...firstTenUsers, {userId: "Avg of other " + remainingUsers.length + " users", cpuHours: remainingAvgUsage}]
            }
            
            const keys = cpuUsageSortedList.map(({userId}) => userId);
            const values = cpuUsageSortedList.map(({cpuHours}) => cpuHours);
            return this.mapToBarChartData(keys, values);
        },
    },
    created() {
        this.loadAllUserProfiles();
        this.loadCpuUsages();
        this.loadStatistics();
    },
    methods: {
        dateRangeChanged(selectedDates) {
            [this.fromTime, this.toTime] = selectedDates;
            if (this.fromTime && this.toTime) {
                this.loadStatistics();
            }
        },
        loadAllUserProfiles() {
            services.UserProfileService.list().then((userProfiles) => {
                this.userProfiles = userProfiles;
                this.countOfAllUsers = this.userProfiles.length;
                this.userProfiles.forEach(({ email }) => {
                    if (email) this.allUserEmailList.push(email);
                });
            });
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
                    const userWithAtLeastSingleJobSet = new Set();
                    allExperiments.forEach(({ userName }) => {
                        const userEmail = this.userProfiles.find(({ userId }) => userId === userName)?.email;
                        if (userEmail) userWithAtLeastSingleJobSet.add(userEmail);
                    });

                    this.userWithAtleastSingleJobEmailList = Array.from(userWithAtLeastSingleJobSet);
                    this.countOfUsersWithAtLeastSingleJob = this.userWithAtleastSingleJobEmailList.length;
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
        downloadUsersWithAtLeastSingleJobEmailCsv() {
            this.downloadEmailCsv(this.userWithAtLeastSingleJobEmailList);
        },
        downloadAllUserEmailCsv() {
            this.downloadEmailCsv(this.allUserEmailList);
        },
        downloadEmailCsv(emailList) {
            const csvContent = "data:text/csv;charset=utf-8,"
                + emailList.join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "emails.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        },
        getPast24Hours() {
            this.fromTime = new Date().fp_incr(0);
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
        getMonthNameList() {
            return ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
            ];
        },
        getBackgroundColorListForMonths() {
            return ['#FF0000', '#FFA500', '#FFFF00', '#008000', '#0000FF', '#4B0082',
                '#EE82EE', '#FFC0CB', '#800000', '#808080', '#FFFFFF', '#000000'];
        },
        mapToBarChartData(keys, values) {
            return {
                labels: keys,
                datasets: [
                    {
                        label: 'No. of Users',
                        data: values,
                        backgroundColor: '#FFC0CB'
                    }
                ]
            };
        },
    }
};
</script>