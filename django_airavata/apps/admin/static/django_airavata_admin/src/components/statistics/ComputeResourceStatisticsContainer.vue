<template>
    <b-card header="Compute Resource with Atleast one Job Submitted">
        <div class="row" v-if="items.length > 0">
            <div class="col">
                <b-card>
                    <b-table :fields="fields" :items="items">
                        <template slot="cell(resourceHostId)" slot-scope="data">
                            <compute-resource-name :compute-resource-id="data.value" />
                        </template>
                        <template slot="cell(numberOfJobs)" slot-scope="data">
                            {{ data.value }}
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

export default {
    name: 'compute-resource-statistics-container',
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
    watch: {
        fromTime() {
            this.reloadAfterPropsChange();
        },
        toTime() {
            this.reloadAfterPropsChange();
        }
    },
    data() {
        return {
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
                    label: "Resource",
                },
                {
                    key: "numberOfJobs",
                    label: "NumberOfJobs",
                },
            ];
        }
    },
    methods: {
        reloadAfterPropsChange() {
            if(this.fromTime && this.toTime) {
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
                        cnt.set(resourceHostId, cnt.has(resourceHostId) ? cnt.get(resourceHostId) + 1 : 1);
                    });
                    this.items = [];
                    cnt.forEach((numberOfJobs, resourceHostId) => {
                        this.items.push({ numberOfJobs, resourceHostId });
                    });
                }
            );
        },
    }
};
</script>