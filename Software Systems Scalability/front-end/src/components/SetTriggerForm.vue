<template>
  <div>
    <form @submit.prevent="SetTriggerSubmitted">
      <div class="container">
          <label for="stockcode" ><b>Stock Code</b></label>
          <input type="text" placeholder="Enter Stock Code" name="stockcode" v-model="stock.code" required maxlength="3">
          <input type="text" placeholder="Enter Trigger Amount" name="trigger" v-model="stock.trigger" required>
          <button type="submit">Set Trigger</button>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      stock: {
        trigger: '',
        code: ''
      }
    }
  },

  methods: {
    SetTriggerSubmitted() {
        this.$emit('trigger-set', this.stock)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
