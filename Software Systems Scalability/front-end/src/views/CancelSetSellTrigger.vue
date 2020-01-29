<template>
  <div class="add-money">
    <h1>Cancel Set Sell Trigger</h1>
    <CancelTriggerForm v-on:user-set-cancel="cancelSetSellTrigger"></CancelTriggerForm>

  </div>
</template>

<script>
import CancelTriggerForm from '@/components/CancelTriggerForm.vue'

export default {
  components: {
    CancelTriggerForm
  },
  methods: {
    cancelSetSellTrigger(stockSymbol) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] CANCEL_SET_SELL '+user+' '+stockSymbol
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
