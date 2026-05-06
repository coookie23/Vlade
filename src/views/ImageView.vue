<template>
  <ProcessingWorkspace :suite="toolSuites.image" />
</template>

<script>
import ProcessingWorkspace from '../components/ProcessingWorkspace.vue'
import { toolSuites } from '../data/toolSuites.js'

export default {
  name: 'ImageView',
  components: { ProcessingWorkspace },
  data() {
    return { toolSuites }
  },
}
</script>
