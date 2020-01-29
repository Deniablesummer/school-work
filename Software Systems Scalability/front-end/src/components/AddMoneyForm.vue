<template>
  <div>
    <form @submit.prevent="addMoneyButtonClicked">
      <div class="container">
          <label for="uname" ><b>Money Amount</b></label>
          <input type="text" placeholder="Enter Amount" name="money" v-model="user.money" required>
          <button type="submit">Add</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      user: {
        money: '',
      }
    }
  },

  methods: {
    addMoneyButtonClicked() {
      this.$emit('user-add-money', this.user.money)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
