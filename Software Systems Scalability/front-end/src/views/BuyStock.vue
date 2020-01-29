<template>
  <div class="buy-stock">
    <h1>Buy Stock Page</h1>
    <QuoteStockForm v-on:quoted-stock="showBuyForm" v-on:stock-symbol="setStockSymbol"></QuoteStockForm>
    <p v-if="this.stockPrice">{{stockPrice}}</p>
    <StockBuyForm v-if="this.stockPrice" v-on:user-buy-quote="buyStock"></StockBuyForm>
  </div>
</template>

<script>
import QuoteStockForm from '@/components/QuoteStockForm.vue'
import StockBuyForm from '@/components/StockBuyForm.vue'

export default {
  components: {
    QuoteStockForm,
    StockBuyForm
  },
  data() {
    return { stockPrice: '', stockSymbol: ''}
  },
  methods: {
    showBuyForm(stockPrice) {
      this.stockPrice = stockPrice
    },
    buyStock(dollarAmount) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] BUY '+user+' '+this.stockSymbol+' '+dollarAmount
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data.data)
        if(data.data.includes("Error")){
          alert(data.data)
        } else {
          alert("Commit buy to complete transaction")
        }
      }
    },
    setStockSymbol(symbol){
      console.log(symbol)
      this.stockSymbol = symbol
      console.log("setStockSymbol "+this.stockSymbol)
    }
  }
}
</script>
