<script setup lang="ts">
import LabelBox from './LabelBox.vue'
import TextBox from './TextBox.vue'
</script>


<template>
    <div id="label-menu">
        <TextBox :text="'Text från datapunkt...'" />
        <LabelBox :alternatives="['a', 'b', 'c']" />
    </div>
</template>

<style scoped>
#label-menu {
    width: 300px;
    padding: 10%;
    background-color: #f1f1f1;
    border-radius: 10px;
}
</style>