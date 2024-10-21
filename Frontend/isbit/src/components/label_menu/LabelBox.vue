<template>
    <div class="label-box">
        <button type="button" @click="select(alternative)" v-bind:class="{'highlight-color': selectedItem == alternative}" class="label-alternative-button main-color isbit-button" 
        v-for="alternative in alternatives">
            {{ alternative }}
        </button>
        <button type="button" id="save-data" class="isbit-button" @click="save">
            Spara datapunkt
        </button>
        <p>
            {{ selectedItem }}
            {{ alternatives }}
        </p>
    </div>
</template>


<script lang="ts">
import { defineComponent, type PropType } from 'vue'
export default defineComponent({
    props: {
        alternatives: Array as PropType<string[]>
    },
    data() {
        return {
            selectedItem: "",
        }
    }, methods: {
        select(alternative: string) {
            if (this.selectedItem == alternative) {
                this.selectedItem = ""
            } else {
                this.selectedItem = alternative;
            }
        }, 
        save() {
            console.log("selected: ", this.selectedItem)
        }
    }
})
</script>

<style scoped>
.label-alternative-button {
    border-color: rgb(230, 230, 230);
    border-radius: 10px;
    border-style: solid;
    border-width: thin;
    display: block;
    width: 90%;
}

.label-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
}

</style>