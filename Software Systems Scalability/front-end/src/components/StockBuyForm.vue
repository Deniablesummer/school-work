<template>
  <div>
    <form @submit.prevent="BuyStockButtonClicked">
      <div class="container">
          <label for="dollarAmount" ><b>Dollar Amount</b></label>
          <input type="text" placeholder="Dollar Amount" name="dollarAmount" v-model="dollarAmount" required>
          <button type="submit">Buy</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      dollarAmount: ""
    }
  },

  methods: {
    BuyStockButtonClicked() {
      this.$emit('user-buy-quote', this.dollarAmount)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
