<template>
  <div>
    <form @submit.prevent="signInButtonSubmit">
      <div class="container">
          <label for="uname" ><b>Username</b></label>
          <input type="text" placeholder="Enter Username" name="uname" v-model="user.username" required>
          <button type="submit">Login</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: {
        username: '',
      }
    }
  },

  methods: {
    signInButtonSubmit() {
      localStorage.setItem('user-signed-in', this.user.username)
      this.$emit('user-sign-in', this.user.username)
      this.$router.push('/') 
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
