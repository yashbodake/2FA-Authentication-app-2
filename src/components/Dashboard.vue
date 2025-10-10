<template>
  <div class="dashboard-container">
    <div class="card-title">DASHBOARD</div>
    <div class="logo">
      <i class="fas fa-tachometer-alt"></i>
    </div>
    <h2>Dashboard</h2>
    <p>Welcome <span class="special-username">{{ username }}</span> to your dashboard!</p>
    <p v-if="twoFactorEnabled" class="2fa-activated-message">2FA Activated</p>
    <div class="dashboard-buttons">
      <button @click="logout">Logout</button>
      <button v-if="!twoFactorEnabled" @click="enable2fa">Enable 2FA</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const twoFactorEnabled = ref(false)
const router = useRouter()

onMounted(async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
        router.push('/login');
        return;
    }

    const meResponse = await axios.get('http://localhost:8000/me', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    username.value = meResponse.data.username;
    twoFactorEnabled.value = meResponse.data.otp_enabled;

  } catch (error) {
    router.push('/login')
  }
})

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const enable2fa = () => {
  router.push('/enable-2fa')
}
</script>