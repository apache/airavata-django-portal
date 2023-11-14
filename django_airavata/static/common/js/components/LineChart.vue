<template>
    <Line :chart-data="chartData" />
</template>

<script>
import { Line } from 'vue-chartjs/legacy';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
} from 'chart.js';

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
);

export default {
    name: 'LineChart',
    props: {
        chartData: {
            required: true,
        },
    },
    components: { Line },
}

</script>