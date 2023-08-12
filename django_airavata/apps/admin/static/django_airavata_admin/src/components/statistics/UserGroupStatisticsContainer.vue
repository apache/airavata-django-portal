<template>
    <b-card header="User groups created within a given period">
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
                            <b-button @click="loadGroups" class="ml-auto" variant="primary">
                                Get Statistics
                            </b-button>
                        </div>
                    </template>
                </b-card>
            </div>
        </div>
        <div class="row" v-if="items.length > 0">
            <div class="col">
                <b-card>
                    <b-table :fields="fields" :items="items">
                        <template slot="cell(userGroupName)" slot-scope="data">
                            {{ data.value }}
                        </template>
                        <template slot="cell(noOfUsers)" slot-scope="data">
                            {{ data.value }}
                        </template>
                        <template slot="cell(actions)" slot-scope="data">
                            <b-link @click="showUserGroupDetails(data.item.id)">
                                View Details
                                <i class="far fa-chart-bar" aria-hidden="true"></i>
                            </b-link>
                        </template>
                    </b-table>
                </b-card>
            </div>
        </div>
        <div class="row" v-if="selectedUserGroupId">
            <div class="col">
                <b-card>
                    <b-table :fields="fieldsForGroupDetails" :items="itemsForGroupDetails">
                        <template slot="cell(userName)" slot-scope="data">
                            {{ data.value }}
                        </template>
                        <template slot="cell(permissions)" slot-scope="data">
                            <b-badge class="mr-2" :variant="'success'" v-if="data.item.isMember">MEMBER</b-badge>
                            <b-badge class="mr-2" :variant="'warning'" v-if="data.item.isAdmin">ADMIN</b-badge>
                            <b-badge class="mr-2" :variant="'danger'" v-if="data.item.isOwner">OWNER</b-badge>
                        </template>
                        <template slot="cell(noOfJobs)" slot-scope="data">
                            {{ data.value }}
                        </template>
                    </b-table>
                </b-card>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <b-card header="User Emails Filtered By UserGroup">
                    <b-input-group class="mb-2">
                        <b-form-select v-model="userGroupFilter" :options="userGroupOptions">
                            <template slot="first">
                                <option :value="null" disabled>
                                    Select Group to filter on
                                </option>
                            </template>
                        </b-form-select>
                    </b-input-group>
                    <b-link @click="downloadUsersInActiveGroupEmailCsv">
                        <i class="fas fa-download"></i>
                        Download emails.csv
                    </b-link>
                </b-card>
            </div>
        </div>
    </b-card>
</template>

<script>
import { services } from "django-airavata-api";

import moment from "moment";
export default {
    name: 'user-group-statistics-container',
    data() {
        const fromTime = new Date().fp_incr(0);
        const toTime = new Date().fp_incr(1);
        return {
            fromTime: fromTime,
            toTime: toTime,
            dateRange: [fromTime, toTime],
            dateConfig: {
                mode: "range",
                wrap: true,
                dateFormat: "Y-m-d",
                maxDate: new Date().fp_incr(1),
            },
            userGroups: [],
            selectedUserGroupId: null,
            userGroupsDetails: null, //group Id to details
            allUserEmails: null, //userId to email
            userGroupFilter: null
        };
    },
    created() {
        this.loadGroups();
        this.loadAllUserEmails();
    },
    computed: {
        fields() {
            return [
                {
                    key: "userGroupName",
                    label: "UserGroupName",
                },
                {
                    key: "noOfUsers",
                    label: "No. of Users",
                },
                {
                    key: "actions",
                    label: "Actions"
                }
            ];
        },
        items() {
            if (this.userGroups && this.userGroupsDetails) {
                return this.userGroups.map(({ name, id }) => {
                    const noOfUsers = this.userGroupsDetails.has(id) ? this.userGroupsDetails.get(id).length : "N/A";
                    return {
                        userGroupName: name,
                        noOfUsers,
                        id,
                    }
                });
            } else {
                return [];
            }
        },
        fieldsForGroupDetails() {
            return [
                {
                    key: "userId",
                    label: "UserName",
                },
                {
                    key: "permissions",
                    label: "Permissions",
                },
                {
                    key: "noOfJobs",
                    label: "No. Of Jobs Submitted in last week",
                },
            ];
        },
        itemsForGroupDetails() {
            if (this.selectedUserGroupId && this.userGroupsDetails.has(this.selectedUserGroupId)) {
                return this.userGroupsDetails.get(this.selectedUserGroupId);
            } else {
                return [];
            }
        },
        userGroupOptions() {
            if (this.userGroups) {
                return this.userGroups.map(({ id, name }) => {
                    return {
                        value: id,
                        text: name,
                    }
                })
            } else {
                return [];
            }
        },
    },
    methods: {
        dateRangeChanged(selectedDates) {
            [this.fromTime, this.toTime] = selectedDates;
            if (this.fromTime && this.toTime) {
                this.loadGroups();
            }
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
        loadGroups() {
            let requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            services.GroupService.getGroupsFilteredByCreationDate(requestData).then(
                (userGroups) => {
                    this.userGroups = userGroups;

                    if (this.userGroups) {
                        this.userGroups = this.userGroups.map((userGroup) => {
                            userGroup.ownerId = this.removeAtDefault(userGroup.ownerId);
                            userGroup.admins = userGroup.admins.map((id) => this.removeAtDefault(id));
                            userGroup.members = userGroup.members.map((id) => this.removeAtDefault(id));
                            return userGroup;
                        });
                    }
                }
            );

            //jobs submitted during last week
            requestData = {
                fromTime: new Date().fp_incr(-7).toJSON(),
                toTime: new Date().fp_incr(1).toJSON(),
            }
            services.ExperimentStatisticsService.get(requestData).then(
                (stats) => {
                    const results = stats ? stats.results : {};
                    let allExperiments = "allExperiments" in results ? results["allExperiments"] : [];
                    this.userGroupsDetails = new Map();
                    this.userGroups.forEach(({ id, members, ownerId, admins }) => {
                        if (id) {
                            this.userGroupsDetails.set(id, members.map((userId) => {
                                return {
                                    userId,
                                    isOwner: (ownerId === userId ? true : false),
                                    isMember: true,
                                    isAdmin: ((admins && admins.includes(userId)) ? true : false),
                                    noOfJobs: allExperiments.filter(({ userName }) => userName === userId).length,
                                };
                            }));
                        }
                    });
                }
            );
        },
        loadAllUserEmails() {
            services.UserProfileService.list().then((userProfiles) => {
                this.allUserEmails = new Map();
                userProfiles.forEach(({ userId, email }) => {
                    if (userId && email) this.allUserEmails.set(userId, email);
                });
            });
        },
        showUserGroupDetails(groupId) {
            this.selectedUserGroupId = groupId;
        },
        downloadUsersInActiveGroupEmailCsv() {
            let groupId = this.userGroupFilter;
            let activeUserGroupUserEmails = [];
            if (this.userGroupsDetails.has(groupId)) {
                this.userGroupsDetails.get(groupId).forEach(({ userId }) => {
                    if (this.allUserEmails && this.allUserEmails.has(userId))
                        activeUserGroupUserEmails.push(this.allUserEmails.get(userId));
                });
            }
            this.downloadEmailCsv(activeUserGroupUserEmails);
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
        removeAtDefault(id) {
            const lastAtIndex = id.lastIndexOf("@");
            if (lastAtIndex > 0) {
                return id.substring(0, lastAtIndex);
            }
            return id;
        },
    },
}
</script>