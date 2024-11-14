<template>
  <div class="outer-box">
    <div id="label-text">
        <p>
            {{ text }}
        </p>
        </div>
    <div class="label-box">
      <button
        type="button"
        @click="select(alternative)"
        v-bind:class="{ 'highlight-color': selectedItem == alternative }"
        class="label-alternative-button main-color isbit-button"
        v-for="alternative in alternatives"
      >
        {{ alternative }}
      </button>
    </div>
    <button type="button" id="save-data" class="isbit-button highlight-color" @click="save">
      Spara datapunkt
    </button>
  </div>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent, type PropType } from 'vue'
export default defineComponent({
  props: {
    alternatives: Array as PropType<string[]>,
    text: String
  },
  data() {
    return {
      selectedItem: '',
      info: null
    }
  },
  methods: {
    select(alternative: string) {
      if (this.selectedItem == alternative) {
        this.selectedItem = ''
      } else {
        this.selectedItem = alternative
      }
    },
    save() {
      console.log('selected: ', this.selectedItem)
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
  width: 100%;
}

#label-text {
  display: flex;
  padding: 12px 20px;      /* Add padding */
  margin: 8px 0;           /* Add some margin */
  box-sizing: border-box;  /* Ensure padding and width are accounted for */
  border: 2px solid #ccc;  /* Set the border */
  border-radius: 4px;      /* Rounded corners */
  font-size: 16px;         /* Increase font size */
  transition: border-color 0.3s; /* Smooth transition for border color */
  background-color: white;
}

.label-box {
  display: block;
  flex-direction: column;
  align-items: center;
  border: 2px solid #ccc; /* Set the border */
  border-radius: 4px; /* Rounded corners */
  background-color: white;
}

.outer-box {
  display: block;
}

#save-data {
  float: right;
  border-radius: 10px;
  border-color: rgb(230, 230, 230);
  border-style: solid;
}
</style>
