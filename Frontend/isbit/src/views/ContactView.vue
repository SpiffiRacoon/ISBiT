<template>
    <div>
      <h1>Fetched Posts</h1>
      <ul>
        <li v-for="post in posts" :key="post.id">
          <h2>{{ post.title }}</h2>
          <p>{{ post.body }}</p>
        </li>
      </ul>
      <div v-if="error">{{ error }}</div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import axios from 'axios';
  
  interface Post {
    id: number;
    title: string;
    body: string;
  }
  
  export default defineComponent({
    name: 'PostsComponent',
    setup() {
      const posts = ref<Post[]>([]);
      const error = ref<string | null>(null);
  
      const fetchPosts = async () => {
        try {
          const response = await axios.get<Post[]>('http://localhost:8000/V1/dataset');
          console.log(response.data);
          posts.value = response.data;
        } catch (err) {
          error.value = 'Failed to fetch posts';
          console.error(err);
        }
      };
  
      onMounted(fetchPosts);
  
      return { posts, error };
    },
  });
  </script>
  
  <style scoped>
  h1 {
    color: #333;
  }
  </style>
  