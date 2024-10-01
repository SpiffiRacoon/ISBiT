<template>
    <div class="container">
      <h1>Dataset Information</h1>
      <div class="card" v-for="(item, index) in dataList" :key="index">
        <div class="card-content">
          <h2>{{ item.dataset }}</h2>
          <div class="card-details">
            <p><strong>Assignment:</strong> {{ item.assignment }}</p>
            <p><strong>Datatype:</strong> {{ item.datatype }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  
  export default defineComponent({
    name: "DataDisplay",
    data() {
      return {
        dataList: [
          { dataset: "Dataset 1", assignment: "Assignment 1", datatype: "Type A" },
          { dataset: "Dataset 2", assignment: "Assignment 2", datatype: "Type B" },
          { dataset: "Dataset 3", assignment: "Assignment 3", datatype: "Type C" },
          { dataset: "Dataset 4", assignment: "Assignment 4", datatype: "Type D" },
        ],
      };
    },
  });
  </script>
  
  <style scoped>
  /* Container styling */
  .container {
    font-family: Arial, sans-serif;
    padding: 20px;
    max-width: 1100px; /* Increased max-width for a wider layout */
    margin: 0 auto;
    background-color: #f9f9f9;
  }
  
  /* Header styling */
  h1 {
    text-align: center;
    font-size: 28px;
    color: #333;
    margin-bottom: 30px;
  }
  
  /* Card styling */
  .card {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 0; /* 90-degree corners */
    margin: 20px 0;
    padding: 25px 40px; /* Increased padding for a more spacious look */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
    width: 100%; /* Ensures the card takes full width of the container */
  }
  
  .card:hover {
    transform: scale(1.02);
  }
  
  .card-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 60px; /* Increased gap between dataset name and details */
  }
  
  /* Heading inside card */
  .card h2 {
    margin: 0;
    font-size: 22px;
    color: #333;
  }
  
  /* Card details arranged horizontally */
  .card-details {
    display: flex;
    gap: 40px; /* Spacing between assignment and datatype */
  }
  
  .card-details p {
    margin: 0;
    font-size: 16px;
    color: #666;
  }
  
  /* Responsive layout */
  @media (max-width: 768px) {
    .card-content {
      flex-direction: column;
      align-items: flex-start;
    }
  
    .card-details {
      flex-direction: column;
      gap: 10px; /* Reduced gap for small screens */
    }
  
    .card h2 {
      font-size: 18px;
    }
  }
  </style>
  