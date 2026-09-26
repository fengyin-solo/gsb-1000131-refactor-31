<template>
  <ModulePage :config="config" />
</template>

<script setup lang="ts">
import ModulePage from '@/components/ModulePage.vue'
import { MODULE_VIEWS } from '@/config/modules'

const config = MODULE_VIEWS.qc
</script>
