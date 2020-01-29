<template>
  <div>
    <form @submit.prevent="dumpLogFileSubmit">
      <div class="container">
          <label for="Filename" ><b>Filename</b></label>
          <input type="text" placeholder="Filename.txt" name="money" v-model="filename" required>
          <button type="submit">Download</button>
          <br>
          <textarea rows="100" cols="100" type="text" id="dumplog_result"></textarea>
      </div>
    </form> 
  </div>
</template>
<script>
export default {
  data() {
    return {
      filename: ''
    }
  },

  methods: {
    dumpLogFileSubmit() {
      this.$emit('user-specified-file', this.filename)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
