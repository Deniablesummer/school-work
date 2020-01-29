<template>
  <div>
    <form @submit.prevent="SetAmountSubmitted">
      <div class="container">
         <input type="text" placeholder="Enter Amount" name="amount" v-model="amount" required>
        <button type="submit">Set Amount</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      amount: ''
    }
  },

  methods: {
    SetAmountSubmitted() {
        this.$emit('user-set-amount', this.amount)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
