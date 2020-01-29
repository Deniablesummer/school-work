<template>
  <div class="buy-stock">
    <h1>Buy Stock Page</h1>
    <SellStockForm v-on:user-sell-stock="sellStock"></SellStockForm>
  </div>
</template>

<script>
import SellStockForm from '@/components/SellStockForm.vue'

export default {
  components: {
    SellStockForm
  },
  methods: {
    sellStock(stockObject) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] SELL '+user+' '+stockObject.stockSymbol+' '+stockObject.dollarAmount
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data.data)
        if(data.data.includes("Error")){
          alert(data.data+"..CUSTOM: check stock quote price from commit buy page and try again with valid input, or maybe it expired")
        } else {
          alert("Commit sell to complete transaction")
        }
      }
    }
  }
}
</script>
