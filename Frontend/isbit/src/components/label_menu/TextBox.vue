<template>
    <div id="label-text">
        <p>
            {{ text }}
        </p>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
export default defineComponent({
    props: {
        text: String
    },
})
</script>

<style scoped>
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
</style>