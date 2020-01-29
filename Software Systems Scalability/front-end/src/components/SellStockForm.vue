<template>
  <div>
    <form @submit.prevent="SellStockButtonClicked">
      <div class="container">
          <label for="stockSymbol" ><b>Stock Symbol</b></label>
          <input type="text" placeholder="Stock Symbol" name="stockSymbol" v-model="stock.stockSymbol" required>
          <label for="dollarAmount" ><b>Dollar Amount</b></label>
          <input type="text" placeholder="Dollar Amount" name="dollarAmount" v-model="stock.dollarAmount" required>
          <button type="submit">Sell</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      stock: {dollarAmount: "", stockSymbol: ""}
    }
  },

  methods: {
    SellStockButtonClicked() {
      this.$emit('user-sell-stock', this.stock)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
