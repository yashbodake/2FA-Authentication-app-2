<template>
  <div class="toast" :class="{ 'show': show }">
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  message: String,
  show: Boolean
})

const showToast = ref(props.show)

watch(() => props.show, (newValue) => {
  showToast.value = newValue
})
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #10B981;
  color: #fff;
  padding: 16px 24px;
  border-radius: 8px;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.toast.show {
  opacity: 1;
  visibility: visible;
}
</style>
