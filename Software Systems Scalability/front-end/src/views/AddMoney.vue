<template>
  <div class="add-money">
    <h1>Add Money Page</h1>
    <AddMoneyForm v-on:user-add-money="addMoneyToUser"></AddMoneyForm>

  </div>
</template>

<script>
import AddMoneyForm from '@/components/AddMoneyForm.vue'

export default {
  components: {
    AddMoneyForm
  },
  methods: {
    addMoneyToUser(money) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] ADD '+user+' '+money
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        alert(data.data)
      }
    }
  }
}
</script>
