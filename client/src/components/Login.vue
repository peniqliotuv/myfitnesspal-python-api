<template>
  <div>
    <transition name="fade">
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
    </transition>
    <div v-if="this.isAuthenticating && !this.isLoggedIn">
      Authenticating...
    </div>
    <div v-if="this.authenticationError">
      Authentication Error.
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
      authenticationError: false,
      isAuthenticating: false,
    }
  },
  methods: {
    async handleLogin() {
      this.isAuthenticating = true;
      this.authenticationError = false;
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
        this.authenticationError = false;
        this.redirect(this.username);
      } else {
        this.authenticationError = true;
      }
      this.isAuthenticating = false;
    },
    redirect(username) {
      this.$router.push({ 
        path: 'home/username', 
        params: { username },
      });
    }
  }
}
</script>

<style lang="scss" scoped>

template {
  color: #2c3e50;
}

.input-container {
  margin: 0 25%;
}

.button-container {

}

.overlay {
  position: absolute;
}



</style>