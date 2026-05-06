<template>
  <ProcessingWorkspace :suite="toolSuites.audio" />
</template>

<script>
import ProcessingWorkspace from '../components/ProcessingWorkspace.vue'
import { toolSuites } from '../data/toolSuites.js'

export default {
  name: 'AudioView',
  components: { ProcessingWorkspace },
  data() {
    return { toolSuites }
  },
}
</script>
