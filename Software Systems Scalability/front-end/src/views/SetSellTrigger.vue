<template>
  <div class="buy-stock">
    <h1>Set Sell Trigger</h1>
    <SetTriggerForm v-on:trigger-set="showSetAmountForm"></SetTriggerForm>
    <SetAmountForm v-if="this.buyTriggerPrice" v-on:user-set-amount="setSellAmount"></SetAmountForm>
  </div>
</template>

<script>
import SetTriggerForm from '@/components/SetTriggerForm.vue'
import SetAmountForm from '@/components/SetAmountForm.vue'

export default {
  components: {
    SetTriggerForm,
    SetAmountForm
  },
  data() {
    return { buyTriggerPrice: '', stockSymbol: ''}
  },
  methods: {
    showSetAmountForm(stockTrigger) {
      this.buyTriggerPrice = stockTrigger.trigger
      this.stockSymbol = stockTrigger.code
    },
    setSellAmount(dollarAmount) {
      let user = localStorage.getItem('user-signed-in')
      //let socketMessage = '[1] SET_BUY_TRIGGER '+user+' '+this.stockSymbol+' '+this.buyTriggerPrice
      let socketMessage = '[1] SET_SELL_AMOUNT '+user+' '+this.stockSymbol+' '+dollarAmount
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        alert(data.data)
        socketMessage = '[1] SET_SELL_TRIGGER '+user+' '+this.stockSymbol+' '+this.buyTriggerPrice
        console.log("sending "+socketMessage)
        this.$socket.send(socketMessage)
        this.$socket.onmessage = (data) => {
            alert(data.data)
        }

      }
    }
  }
}
</script>
