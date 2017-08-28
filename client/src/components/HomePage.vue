<template>
  <div class="input-container">
    <div class="row">
      <div>Home </div>
      <div v-if="this.isLoading">
        <h4>
          Content is loading...
        </h4>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchInitialData } from '../api/monthly';

export default {
  name: 'HomePage',
  data() {
    return {
      username: '',
      password: '',
      isLoading: true
    }
  },
  methods: {
    getDailyAverage() {
    }
  },
  async mounted() {
    this.isLoading = true;
    const data = await fetchInitialData();
    this.isLoading = false;
    console.log(data);
  }
}
</script>

<style lang="scss">




</style>