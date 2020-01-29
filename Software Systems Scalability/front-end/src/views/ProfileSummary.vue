<template>
  <div class="profile-summary">
    <h1>Profile Summary Page</h1>
    <span>{{userData}}</span>
  </div>
</template>

<script>
//DISPLAY_SUMMARY
  export default {
    data() {
      return { userData: ''}
    },
    methods: {
      getProfileSummary() {
        let user = localStorage.getItem('user-signed-in')
        this.$socket.send('[1] ADD '+user+' 0')
        let socketMessage = '[1] DISPLAY_SUMMARY '+user
        console.log("sending "+socketMessage)
        this.$socket.send(socketMessage)
        this.$socket.onmessage = (data) => {
          console.log("receieved ", data)
          if(data.data.includes("Reserved Money")){
            this.userData = data.data
          }
        }
      }
    },
    beforeMount(){
      this.getProfileSummary()
    }
  }

</script>
