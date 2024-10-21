<script setup lang="ts">
import LabelBox from './LabelBox.vue'
import TextBox from './TextBox.vue'
import ClusterPlot from "./ClusterPlot.vue"
</script>


<template>
    <div id="label-menu">
        <ClusterPlot />
        <div id="text-and-labels">
            <TextBox :text="apiData.t" />
            <LabelBox :alternatives="['LOC', 'HUM', 'DESC', 'ENTY', 'ABBR', 'NUM']" />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent} from 'vue'
import axios from 'axios'
export default defineComponent({
    props: {
        text: String
    },
    data() {
        return {
            apiData: {t: String}
        }
    }, methods: {
        fetchData() {
            axios.get('http://localhost:8000/V1/data/?collection=swe_qaqc_lib_test').then(response => this.apiData.t = response.data[0].text)
        }
    }, mounted() {
        axios.get('http://localhost:8000/V1/data/?collection=swe_qaqc_lib_test').then(response => this.apiData.t = response.data[0].text)
    }
})
</script>

<style scoped>
#label-menu {
    display: flex;
}

#text-and-labels {
    margin: 20px;
    display:block;
    width: 300px;
}
</style>