<template>
  <div class="add-money">
    <h1>Dumplog</h1>
    <DumplogForm v-on:user-specified-file="getDumpLog"></DumplogForm>

  </div>
</template>

<script>
import DumplogForm from '@/components/DumplogForm.vue'

export default {
  components: {
    DumplogForm
  },
  methods: {
    getDumpLog(filename) {
      let user = localStorage.getItem('user-signed-in')
      let socketMessage = '[1] DUMPLOG '+user+' '+filename
      console.log("sending "+socketMessage)
      this.$socket.send(socketMessage)
      this.$socket.onmessage = (data) => {
        console.log("receieved ", data)
        document.getElementById("dumplog_result").value += data.data;
      }
    }
  }
}
</script>
