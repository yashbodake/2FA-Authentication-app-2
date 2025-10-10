<template>
  <div class="auth-container">
    <div class="card-title">2FA SETUP</div>
    <div class="logo">
      <i class="fas fa-shield-alt"></i>
    </div>
    <h2>Enable 2FA</h2>
    <div v-if="qrCode" class="qr-code-container center-content">
      <p>Scan this QR code with your authenticator app:</p>
      <img :src="qrCode" alt="QR Code">
      <p>Or manually enter this secret key:</p>
      <p><strong>{{ otpSecret }}</strong></p>
      <p>Then enter the code from your app below:</p>
      <form @submit.prevent="confirm2fa">
        <div class="input-group">
          <label for="otp"><i class="fas fa-key"></i> 2FA Code</label>
          <div class="input-container">
            <input type="text" id="otp" v-model="otp" placeholder="Enter your 2FA code" required>
          </div>
        </div>
        <button type="submit">Confirm</button>
      </form>
    </div>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const qrCode = ref('')
const otpSecret = ref('')
const otp = ref('')
const error = ref('')
const router = useRouter()

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
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'An unexpected error occurred.'
    }
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
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'An unexpected error occurred.'
    }
  }
}
</script>
