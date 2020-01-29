<template>
  <div>
    <form @submit.prevent="QuoteStockButtonClicked">
      <div class="container">
          <label for="stockcode" ><b>Stock Code</b></label>
          <input type="text" placeholder="Enter Stock Code" name="stockcode" v-model="stock.code" required maxlength="3">
          <button type="submit">Quote</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      stock: {
        code: '',
      }
    }
  },

  methods: {
    QuoteStockButtonClicked() {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] QUOTE '+user+' '+this.stock.code
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data.data)
        this.$emit('quoted-stock', data.data)
        this.$emit('stock-symbol', this.stock.code)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
