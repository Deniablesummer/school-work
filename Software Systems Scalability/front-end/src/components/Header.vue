<template>
  <div class="hello">
    <div id="nav">
      <router-link to="/" class="header-text">Home |</router-link>
      <router-link to="/sign-in" v-if="!isSignedIn()"  class="header-text">Sign In </router-link>
      <router-link to="/Add-Money" v-if="isSignedIn()"  class="header-text">Add Money |</router-link><br>
      <router-link to="/Buy-Stock" v-if="isSignedIn()"  class="header-text">Buy Stock |</router-link>
      <span v-if="isSignedIn()" v-on:click="commitBuy" class="header-text">Commit Buy |</span>
      <span v-if="isSignedIn()" v-on:click="cancelBuy" class="header-text">Cancel Buy |</span>
      <router-link to="/Set-Buy-Trigger" v-if="isSignedIn()"  class="header-text">Set Buy Trigger |</router-link>
      <router-link to="/Cancel-Set-Buy-Trigger" v-if="isSignedIn()"  class="header-text">Cancel Set Buy Trigger |</router-link><br>
      <router-link to="/Sell-Stock" v-if="isSignedIn()"  class="header-text">Sell Stock |</router-link>
      <span v-if="isSignedIn()" v-on:click="commitSell" class="header-text">Commit Sell |</span>
      <span v-if="isSignedIn()" v-on:click="cancelSell" class="header-text">Cancel Sell |</span>
      <router-link to="/Set-Sell-Trigger" v-if="isSignedIn()"  class="header-text">Set Sell Trigger |</router-link>
      <router-link to="/Cancel-Set-Sell-Trigger" v-if="isSignedIn()"  class="header-text">Cancel Set Sell Trigger |</router-link><br>
      <router-link to="/Dumplog" v-if="isSignedIn()"  class="header-text">Dumplog </router-link><br>
      <router-link to="/Profile-Summary" v-if="isSignedIn()"  class="header-text">Profile Summary |</router-link>
      <span v-if="isSignedIn()" class="header-text" v-on:click="signOutUser">Sign Out </span>
    </div>
    <router-view/>
  </div>
</template>
<script>
export default {
  name: 'Header',
  // To use props, they must be declared
  props: {
    username: String,
  },
   methods:{
     isSignedIn: function() {
       return localStorage.getItem('user-signed-in')
     },
    commitBuy: function() {
      let socketMessage = '[1] COMMIT_BUY '+localStorage.getItem
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        alert(data.data)
      }
     },
    cancelBuy: function() {
      let socketMessage = '[1] CANCEL_BUY '+localStorage.getItem
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        alert(data.data)
      }
     },
    commitSell: function() {
      let socketMessage = '[1] COMMIT_SELL '+localStorage.getItem
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        alert(data.data)
      }
     },
    cancelSell: function() {
      let socketMessage = '[1] CANCEL_SELL '+localStorage.getItem
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        alert(data.data)
      }
     },
     signOutUser: function () {
      localStorage.removeItem('user-signed-in')
      this.$router.push('home')
     }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.header-text{
  text-decoration: underline;
  cursor: pointer;
  margin-right: 10px;
}
</style>
