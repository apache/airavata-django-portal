<template>
    <Bar :chart-data="chartData" />
</template>

<script>
import { Bar } from 'vue-chartjs/legacy';
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement, CategoryScale, LinearScale
} from 'chart.js';

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
);

export default {
    name: 'BarChart',
    props: {
        chartData: {
            required: true,
        },
    },
    components: { Bar },
}
</script>