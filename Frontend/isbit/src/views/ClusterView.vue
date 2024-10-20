<template>
  <main>
    <LabelBox :alternatives="['a', 'b', 'c']" />
    <ClusterPlot />
  </main>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import LabelBox from '../components/label_menu/LabelBox.vue';
import ClusterPlot from "@/components/label_menu/ClusterPlot.vue";


</script>
