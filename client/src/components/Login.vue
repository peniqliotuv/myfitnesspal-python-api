<template>
  <div class="input-container">
    <div class="row">
      <div class="input-field col s12">
        <input v-model="username" id="username" type="text" class="validate">
        <label for="username">Username</label>
      </div>
    </div>
    <div class="row">
      <div class="input-field col s12">
        <input v-model="password" id="password" type="password" class="validate">
        <label for="password">Password</label>
      </div>
    </div>
    <div class="button-container">
      <button class="waves-effect waves-light btn" @click="handleLogin()">Login</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data() {
    return {
      username: '',
      password: '',
      isLoggedIn: false,
    }
  },
  methods: {
    async handleLogin() {
      console.log(this.username, this.password);
      const url = 'http://localhost:5000/api/login';
      const { username, password } = this;
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password }),
        credentials: 'same-origin'
      });
      const res = await response.json();
      if (response.status === 200 && res.success === true) {
        this.isLoggedIn = true;
      } else {
        this.isLoggedIn = false;
      }
      console.log(this.isLoggedIn);
    }
  }
}
</script>

<style lang="scss">

template {
  color: #2c3e50;
}

.input-container {
  margin: 0 25%;
}

.button-container {

}



</style>