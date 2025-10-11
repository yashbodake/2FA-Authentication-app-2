<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Welcome, {{ username }}</h1>
    </div>
    <div class="dashboard-grid">
      <div class="panel two-fa-panel">
        <div class="panel-header">
          <h2>Two-Factor Authentication</h2>
          <span class="status-badge" :class="{ enabled: twoFactorEnabled }">{{ twoFactorEnabled ? 'Enabled' : 'Disabled' }}</span>
        </div>
        <p class="secondary-text">{{ twoFactorEnabled ? '2FA is active on your account.' : 'Protect your account by enabling Two-Factor Authentication.' }}</p>
        <button v-if="!twoFactorEnabled" @click="enable2fa" class="btn btn-primary">
          Enable Protection
        </button>
      </div>
      <div class="panel actions-panel">
        <div class="panel-header">
          <h2>Account Actions</h2>
        </div>
        <p class="secondary-text">Manage your account and session.</p>
        <button @click="logout" class="btn btn-secondary">
          Logout
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('yash')
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

<style scoped>
.dashboard-container {
  padding: 48px;
  max-width: 1200px;
  margin: auto;
}

.dashboard-header h1 {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 48px;
  color: #FFFFFF;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 32px;
}

.panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 32px;
  color: #FFFFFF;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.panel-header h2 {
  font-size: 20px;
  font-weight: 700;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 16px;
  font-weight: 700;
  font-size: 14px;
}

.status-badge.enabled {
  background-color: #E91E63;
  color: #FFFFFF;
}

.status-badge.disabled {
  background-color: #F5F5F5;
  color: #0D0D0D;
}

.secondary-text {
  color: #F5F5F5;
  font-size: 14px;
  margin-bottom: 24px;
}

.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  width: 100%;
}

.btn-primary {
  background-color: #E91E63;
  color: #FFFFFF;
  box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 30, 99, 0.6);
}

.btn-secondary {
  background-color: transparent;
  border: 1px solid #F5F5F5;
  color: #F5F5F5;
}

.btn-secondary:hover {
  background-color: #F5F5F5;
  color: #0D0D0D;
}
</style>
