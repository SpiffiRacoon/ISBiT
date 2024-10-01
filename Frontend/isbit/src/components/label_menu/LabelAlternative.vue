<template>
    <div class="label_alternative">
            <button type="button" :class="{'selected': selectedItem == 'b1'}" @click="select('b1')">B1</button>
            <button type="button" :class="{'selected': selectedItem == 'b2'}" @click="select('b2')">B2</button>
    </div>
</template>

<script lang="ts">
    export default {
        data() {
            return {selectedItem: ''};
        }, 
        methods: {
            select(id: string) {
                this.selectedItem = id;
            }
        }
    }
</script>

<style scoped>
p {
    color:aliceblue
}

.label_alternative {

}

.selected {
    background-color: blue;
}

.box {
    background-color: chartreuse;
}
</style>