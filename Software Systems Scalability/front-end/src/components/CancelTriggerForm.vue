<template>
  <div>
    <form @submit.prevent="cancelTriggerSubmit">
      <div class="container">
          <label for="stockSymbol" ><b>Stock Symbol</b></label>
          <input type="text" placeholder="Enter Stock Symbol" name="stockSymbol" v-model="stockSymbol" required>
          <button type="submit">Cancel</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      stockSymbol: ''
    }
  },

  methods: {
    cancelTriggerSubmit() {
      this.$emit('user-set-cancel', this.stockSymbol)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
