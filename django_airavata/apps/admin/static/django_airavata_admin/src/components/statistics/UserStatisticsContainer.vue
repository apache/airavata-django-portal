<template>
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
                            <b-button @click="loadStatistics" class="ml-auto" variant="primary">Get
                                Statistics</b-button>
                        </div>
                    </template>
                </b-card>
            </div>
        </div>
        <div class="row">
            <div class="col">
                <b-card><b-card-text>Number of users: {{ countOfUsers }}</b-card-text>
                    <b-link @click="downloadUserEmailCsv">
                        <i class="fas fa-download"></i>
                        Download emails.csv
                    </b-link></b-card>
            </div>
        </div>
    </b-card>
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
            countOfUsers: 0,
            userEmailList: [],
            userProfiles: [],
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
                userProfiles = [
                    { userId: "machrist@iu.edu", email: "machrist@iu.edu" },
                    { userId: "mccalm@rpi.edu", email: "mccalm@rpi.edu" },
                    { userId: "eroma2016", email: "eroma2016.iu.edu" },
                    { userId: "sauravkumar", email: "ims@gmail.com" },
                ];
                this.userProfiles = userProfiles;
            });
            const requestData = {
                fromTime: this.fromTime.toJSON(),
                toTime: this.toTime.toJSON(),
            };
            return services.ExperimentStatisticsService.get(requestData).then(
                (stats) => {
                    stats = {
                        "count": 11,
                        "next": null,
                        "previous": null,
                        "results": {
                            "allExperimentCount": 11,
                            "completedExperimentCount": 7,
                            "cancelledExperimentCount": 0,
                            "failedExperimentCount": 4,
                            "createdExperimentCount": 0,
                            "runningExperimentCount": 0,
                            "allExperiments": [
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Apr_27,_2023_9:12_AM_37ff0545-41d5-45ea-9a25-5d120e427ae9",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-06-06T17:01:27.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Gaussian16 on Apr 27, 2023 9:12 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "Bridges2_2f297e9d-fe9e-4edb-af0d-ec3ad43241e9",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-06-06T17:33:42.749000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Apr_27%2C_2023_9%3A12_AM_37ff0545-41d5-45ea-9a25-5d120e427ae9/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_28,_2023_1:04_PM_efd04866-c737-4b38-bea0-1168a49f51b0",
                                    "projectId": "Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-28T17:08:19.000000Z",
                                    "userName": "mccalm@rpi.edu",
                                    "name": "Gaussian16 on Apr 28, 2023 1:04 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-28T17:13:41.893000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_28%2C_2023_1%3A04_PM_efd04866-c737-4b38-bea0-1168a49f51b0/",
                                    "project": "https://testdrive.airavata.org/api/projects/Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_27,_2023_9:12_AM_62778744-76d8-4e2f-af4c-7858639e8495",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-27T13:13:45.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Gaussian16 on Apr 27, 2023 9:12 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "Bridges2_2f297e9d-fe9e-4edb-af0d-ec3ad43241e9",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-27T13:45:31.287000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_27%2C_2023_9%3A12_AM_62778744-76d8-4e2f-af4c-7858639e8495/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Mar_30,_2023_12:23_PM_6f624870-a1ee-41f0-ad3f-268c7117c3da",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-27T05:18:59.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Clone of Gaussian16 on Mar 30, 2023 12:23 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-27T05:31:40.908000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Mar_30%2C_2023_12%3A23_PM_6f624870-a1ee-41f0-ad3f-268c7117c3da/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                },
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Sep_14,_2022_11:03_AM_c89868d4-fa56-46f4-b731-c4ef5a41c871",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-26T19:41:31.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Clone of Gaussian16 on Sep 14, 2022 11:03 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-26T19:47:41.775000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Sep_14%2C_2022_11%3A03_AM_c89868d4-fa56-46f4-b731-c4ef5a41c871/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_20,_2023_1:31_PM_0b38e94b-0555-4782-be21-a0e6e70c060e",
                                    "projectId": "Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-20T17:33:01.000000Z",
                                    "userName": "mccalm@rpi.edu",
                                    "name": "Gaussian16 on Apr 20, 2023 1:31 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-20T17:39:54.343000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_20%2C_2023_1%3A31_PM_0b38e94b-0555-4782-be21-a0e6e70c060e/",
                                    "project": "https://testdrive.airavata.org/api/projects/Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6/"
                                },
                                {
                                    "experimentId": "Clone_of_Clone_of_Clone_of_Clone_of_Echo_jambo_b846cbdf-9a41-4f32-95a7-63308f24d619",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-19T20:59:35.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-04-19T21:05:30.346000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Clone_of_Clone_of_Echo_jambo_b846cbdf-9a41-4f32-95a7-63308f24d619/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Clone_of_Clone_of_Echo_jambo_e5c60f0c-c83e-456b-895a-f13f1ad2abd3",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-19T20:59:09.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-04-19T21:03:49.377000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Clone_of_Echo_jambo_e5c60f0c-c83e-456b-895a-f13f1ad2abd3/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Mar_30,_2023_12:23_PM_77f335f3-5dcb-4f6a-a4a5-61e59f630431",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T16:24:00.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Gaussian16 on Mar 30, 2023 12:23 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-03-30T16:59:26.848000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Mar_30%2C_2023_12%3A23_PM_77f335f3-5dcb-4f6a-a4a5-61e59f630431/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                },
                                {
                                    "experimentId": "Clone_of_Clone_of_Echo_jambo_46c0fe6b-527e-4062-995f-3f0934b365ab",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T16:11:43.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-03-30T16:16:22.487000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Echo_jambo_46c0fe6b-527e-4062-995f-3f0934b365ab/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Echo_jambo_4d6b0b49-d5fc-4538-951a-0dd37239a76d",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T15:30:54.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-03-30T15:35:34.762000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Echo_jambo_4d6b0b49-d5fc-4538-951a-0dd37239a76d/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                }
                            ],
                            "completedExperiments": [
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Apr_27,_2023_9:12_AM_37ff0545-41d5-45ea-9a25-5d120e427ae9",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-06-06T17:01:27.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Gaussian16 on Apr 27, 2023 9:12 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "Bridges2_2f297e9d-fe9e-4edb-af0d-ec3ad43241e9",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-06-06T17:33:42.749000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Apr_27%2C_2023_9%3A12_AM_37ff0545-41d5-45ea-9a25-5d120e427ae9/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_28,_2023_1:04_PM_efd04866-c737-4b38-bea0-1168a49f51b0",
                                    "projectId": "Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-28T17:08:19.000000Z",
                                    "userName": "mccalm@rpi.edu",
                                    "name": "Gaussian16 on Apr 28, 2023 1:04 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-28T17:13:41.893000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_28%2C_2023_1%3A04_PM_efd04866-c737-4b38-bea0-1168a49f51b0/",
                                    "project": "https://testdrive.airavata.org/api/projects/Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_27,_2023_9:12_AM_62778744-76d8-4e2f-af4c-7858639e8495",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-27T13:13:45.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Gaussian16 on Apr 27, 2023 9:12 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "Bridges2_2f297e9d-fe9e-4edb-af0d-ec3ad43241e9",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-27T13:45:31.287000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_27%2C_2023_9%3A12_AM_62778744-76d8-4e2f-af4c-7858639e8495/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Mar_30,_2023_12:23_PM_6f624870-a1ee-41f0-ad3f-268c7117c3da",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-27T05:18:59.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Clone of Gaussian16 on Mar 30, 2023 12:23 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-27T05:31:40.908000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Mar_30%2C_2023_12%3A23_PM_6f624870-a1ee-41f0-ad3f-268c7117c3da/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                },
                                {
                                    "experimentId": "Clone_of_Gaussian16_on_Sep_14,_2022_11:03_AM_c89868d4-fa56-46f4-b731-c4ef5a41c871",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-26T19:41:31.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Clone of Gaussian16 on Sep 14, 2022 11:03 AM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-26T19:47:41.775000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Gaussian16_on_Sep_14%2C_2022_11%3A03_AM_c89868d4-fa56-46f4-b731-c4ef5a41c871/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Apr_20,_2023_1:31_PM_0b38e94b-0555-4782-be21-a0e6e70c060e",
                                    "projectId": "Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-20T17:33:01.000000Z",
                                    "userName": "mccalm@rpi.edu",
                                    "name": "Gaussian16 on Apr 20, 2023 1:31 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-04-20T17:39:54.343000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Apr_20%2C_2023_1%3A31_PM_0b38e94b-0555-4782-be21-a0e6e70c060e/",
                                    "project": "https://testdrive.airavata.org/api/projects/Default_Project_2f9c6b1e-7aad-4df0-824f-f4dc8624b9d6/"
                                },
                                {
                                    "experimentId": "Gaussian16_on_Mar_30,_2023_12:23_PM_77f335f3-5dcb-4f6a-a4a5-61e59f630431",
                                    "projectId": "Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T16:24:00.000000Z",
                                    "userName": "eroma2016",
                                    "name": "Gaussian16 on Mar 30, 2023 12:23 PM",
                                    "description": null,
                                    "executionId": "Gaussian16_375f2e15-5cb8-4484-ab44-07c8b6e50c57",
                                    "resourceHostId": "expanse_34f71d6b-765d-4bff-be2e-30a74f5c8c32",
                                    "experimentStatus": "COMPLETED",
                                    "statusUpdateTime": "2023-03-30T16:59:26.848000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Gaussian16_on_Mar_30%2C_2023_12%3A23_PM_77f335f3-5dcb-4f6a-a4a5-61e59f630431/",
                                    "project": "https://testdrive.airavata.org/api/projects/Test_March_2023_Deployment_5c016a52-c557-4176-944d-3afd87dcd550/"
                                }
                            ],
                            "failedExperiments": [
                                {
                                    "experimentId": "Clone_of_Clone_of_Clone_of_Clone_of_Echo_jambo_b846cbdf-9a41-4f32-95a7-63308f24d619",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-19T20:59:35.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-04-19T21:05:30.346000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Clone_of_Clone_of_Echo_jambo_b846cbdf-9a41-4f32-95a7-63308f24d619/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Clone_of_Clone_of_Echo_jambo_e5c60f0c-c83e-456b-895a-f13f1ad2abd3",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-04-19T20:59:09.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-04-19T21:03:49.377000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Clone_of_Echo_jambo_e5c60f0c-c83e-456b-895a-f13f1ad2abd3/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Clone_of_Echo_jambo_46c0fe6b-527e-4062-995f-3f0934b365ab",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T16:11:43.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-03-30T16:16:22.487000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Clone_of_Echo_jambo_46c0fe6b-527e-4062-995f-3f0934b365ab/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                },
                                {
                                    "experimentId": "Clone_of_Echo_jambo_4d6b0b49-d5fc-4538-951a-0dd37239a76d",
                                    "projectId": "DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831",
                                    "gatewayId": "default",
                                    "creationTime": "2023-03-30T15:30:54.000000Z",
                                    "userName": "machrist@iu.edu",
                                    "name": "Clone of Echo jambo",
                                    "description": null,
                                    "executionId": "Echo_23d67491-1bef-47bd-a0f5-faf069e09773",
                                    "resourceHostId": "testdrive.vc.airavata.org_0db358cf-d37b-40f2-9e14-1a626ea11884",
                                    "experimentStatus": "FAILED",
                                    "statusUpdateTime": "2023-03-30T15:35:34.762000Z",
                                    "url": "https://testdrive.airavata.org/api/experiments/Clone_of_Echo_jambo_4d6b0b49-d5fc-4538-951a-0dd37239a76d/",
                                    "project": "https://testdrive.airavata.org/api/projects/DefaultProject_a78ca27b-3918-45f6-bea9-47d61e782831/"
                                }
                            ],
                            "cancelledExperiments": [],
                            "createdExperiments": [],
                            "runningExperiments": []
                        },
                        "limit": 50,
                        "offset": 0
                    };
                    let results = stats ? stats.results : {};
                    const allExperiments = "allExperiments" in results ? results["allExperiments"] : [];
                    const userSet = new Set();
                    allExperiments.forEach(({ userName }) => {
                        const userEmail = this.userProfiles.find(({ userId }) => userId === userName)?.email;
                        if (userEmail) userSet.add(userEmail);
                    });

                    this.userEmailList = Array.from(userSet);
                    this.countOfUsers = this.userEmailList.length;
                }
            );
        },
        downloadUserEmailCsv() {
            const csvContent = "data:text/csv;charset=utf-8,"
                + this.userEmailList.join("\n");
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