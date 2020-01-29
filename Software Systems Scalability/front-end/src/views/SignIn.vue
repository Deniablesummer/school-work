<template>
  <div class="sign-in">
    <h1>Sign in page</h1>
    <signInForm v-on:user-sign-in="userSignedIn"></SignInForm>
  </div>
</template>

<script>
import SignInForm from '@/components/SignInForm.vue'

export default {
  components: {
    SignInForm
  },
  data() {
    return {
      username: ''
    };
  },
  methods: {
    userSignedIn(username) {
      if(localStorage.getItem('user-signed-in')){
        console.log(localStorage.getItem('user-signed-in'))
      }
    }
  }
}
</script>
