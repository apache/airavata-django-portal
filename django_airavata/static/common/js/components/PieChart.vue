<template>
    <Pie :chart-data="chartData" />
</template>

<script>
import { Pie } from 'vue-chartjs/legacy';
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale
} from 'chart.js';

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    ArcElement,
    CategoryScale
);

export default {
    name: 'PieChart',
    props: {
        chartData: {
            required: true,
        },
    },
    components: { Pie },
}
</script>