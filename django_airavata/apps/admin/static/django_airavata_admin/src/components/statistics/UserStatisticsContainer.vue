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
                        <b-link @click="downloadUserWithAtLeastSingleJobEmailCsv">
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
                    </b-card>
                    <b-link @click="downloadAllUserEmailCsv">
                        <i class="fas fa-download"></i>
                        Download emails.csv
                    </b-link>
                </div>
            </div>
        </b-card>
    </div>
</template>

<script>
import { services } from "django-airavata-api";

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
    methods: {
        dateRangeChanged(selectedDates) {
            [this.fromTime, this.toTime] = selectedDates;
            if (this.fromTime && this.toTime) {
                this.loadStatistics();
            }
        },
        loadStatistics() {
            services.UserProfileService.list().then((userProfiles) => {
                this.userProfiles = userProfiles;
                this.countOfAllUsers = this.userProfiles.length;
                this.userProfiles.forEach(({ email }) => {
                    if (email) this.allUserEmailList.push(email);
                });
            });
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
        downloadUserWithAtLeastSingleJobEmailCsv() {
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
    }
};
</script>