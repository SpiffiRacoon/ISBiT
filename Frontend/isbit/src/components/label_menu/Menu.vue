<script setup lang="ts">
import LabelBox from './LabelBox.vue'
import TextBox from './TextBox.vue'
</script>


<template>
    <div id="label-menu">
        <TextBox :text="'Text från datapunkt...'" />
        <LabelBox :alternatives="['a', 'b', 'c']" />
        <button type="button" @click="fetchData">API BUTTON</button>
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
            apiData: {}
        }
    }, methods: {
        fetchData() {
            axios.get('https://localhost:8000/V1/ping').then(response => console.log(response))
        }
    }
})
</script>

<style scoped>
#label-menu {
    width: 300px;
    padding: 10%;
    background-color: #f1f1f1;
    border-radius: 10px;
}
</style>