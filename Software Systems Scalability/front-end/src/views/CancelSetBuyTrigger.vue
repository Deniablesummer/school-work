<template>
  <div class="add-money">
    <h1>Cancel Set Buy Trigger</h1>
    <CancelTriggerForm v-on:user-set-cancel="cancelSetBuyTrigger"></CancelTriggerForm>

  </div>
</template>

<script>
import CancelTriggerForm from '@/components/CancelTriggerForm.vue'

export default {
  components: {
    CancelTriggerForm
  },
  methods: {
    cancelSetBuyTrigger(stockSymbol) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] CANCEL_SET_BUY '+user+' '+stockSymbol
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
