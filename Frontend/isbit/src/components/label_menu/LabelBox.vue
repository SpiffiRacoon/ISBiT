<template>
  <div class="outer-box">
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
    alternatives: Array as PropType<string[]>
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
      this.$emit('mark-point', this.selectedItem)
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
  width: 103%;
  margin-bottom: 10px;
}

.label-box {
  display: block;
  flex-direction: column;
  align-items: center;
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
