<template>
  <div class="home">
  <p v-if="!isSignedIn()">Click sign in to get started! This is a user interface for Group CJSM's Seng468 project. The group members are Callum Thomas, James Ryan, Shawn Daliwhal, and Max Gunton. Im salad man haha, I can be whatever, you know what I mean?.</p>  
  <p v-if="isSignedIn()"> Welcome {{getUserName()}} </p>
  </div>
</template>

<script>
export default {
  name: 'Home',
   methods:{
     isSignedIn: function() {
       return localStorage.getItem('user-signed-in')
     },
     getUserName: function() {
       return localStorage.getItem('user-signed-in')
     }
  },
  beforeMount() {
    
  }
}
</script>


