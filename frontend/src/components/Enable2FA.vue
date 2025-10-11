<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="card-header">
        <h1>Enable 2FA</h1>
        <p>Scan the QR code with your authenticator app.</p>
      </div>
      <div v-if="qrCode" class="qr-code-container">
        <img :src="qrCode" alt="QR Code" class="qr-code">
        <div class="secret-key-container">
          <p class="secret-key">{{ otpSecret }}</p>
          <button @click="copySecret" class="copy-btn">
            <i class="fas fa-copy"></i>
          </button>
        </div>
      </div>
      <form @submit.prevent="confirm2fa">
        <div class="input-group">
          <input type="text" id="otp" v-model="otp" placeholder="Enter 2FA Code" required>
        </div>
        <button type="submit" class="btn btn-primary">Confirm & Enable</button>
      </form>
    </div>
    <Toast :message="toastMessage" :show="showToast" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Toast from './Toast.vue'

const qrCode = ref('')
const otpSecret = ref('')
const otp = ref('')
const showToast = ref(false)
const toastMessage = ref('')
const router = useRouter()

const copySecret = () => {
  navigator.clipboard.writeText(otpSecret.value)
  toastMessage.value = 'Secret key copied to clipboard!'
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

onMounted(async () => {
  try {
    const response = await axios.post('http://localhost:8000/2fa/enable', {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    qrCode.value = response.data.qr_code
    otpSecret.value = response.data.otp_secret
  } catch (err) {
    console.error(err)
  }
})

const confirm2fa = async () => {
  try {
    await axios.post('http://localhost:8000/2fa/confirm', 
      { code: otp.value },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    )
    router.push('/')
  } catch (err) {
    console.error(err)
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.auth-card {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  color: #FFFFFF;
}

.card-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 10px;
}

.card-header p {
  font-size: 16px;
  color: #F5F5F5;
  margin-bottom: 40px;
}

.qr-code-container {
  margin-bottom: 40px;
}

.qr-code {
  width: 160px;
  height: 160px;
  margin: 0 auto 24px;
  background: #fff;
  padding: 10px;
  border-radius: 10px;
}

.secret-key-container {
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  padding: 12px;
}

.secret-key {
  font-family: 'JetBrains Mono', monospace;
  font-size: 16px;
  letter-spacing: 1px;
  margin: 0;
  color: #FFFFFF;
}

.copy-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #F5F5F5;
  margin-left: 16px;
  transition: color 0.3s ease;
}

.copy-btn:hover {
  color: #E91E63;
}

.input-group input {
  width: 100%;
  padding: 15px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  color: #FFFFFF;
  font-size: 16px;
  text-align: center;
  letter-spacing: 4px;
  margin-bottom: 20px;
}

.input-group input::placeholder {
  color: #F5F5F5;
}

.btn-primary {
  width: 100%;
  padding: 15px;
  background-color: #E91E63;
  border: none;
  border-radius: 10px;
  color: #FFFFFF;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 30, 99, 0.6);
}
</style>