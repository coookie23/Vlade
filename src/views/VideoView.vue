<template>
  <ProcessingWorkspace :suite="toolSuites.video" />
</template>

<script>
import ProcessingWorkspace from '../components/ProcessingWorkspace.vue'
import { toolSuites } from '../data/toolSuites.js'

export default {
  name: 'VideoView',
  components: { ProcessingWorkspace },
  data() {
    return { toolSuites }
  },
}
</script>
