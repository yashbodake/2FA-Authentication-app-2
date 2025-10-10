<template>
  <div class="auth-container">
    <div class="card-title">LOGIN</div>
    <div class="logo">
      <i class="fas fa-sign-in-alt"></i>
    </div>
    <h2>Login</h2>
    <form @submit.prevent="login" class="center-content">
      <div v-if="!twoFactorRequired">
        <div class="input-group">
          <label for="username"><i class="fas fa-user"></i> Username</label>
          <div class="input-container">
            <input type="text" id="username" v-model="username" placeholder="Enter your username" required>
          </div>
        </div>
        <div class="input-group">
          <label for="password"><i class="fas fa-lock"></i> Password</label>
          <div class="input-container">
            <input type="password" id="password" v-model="password" placeholder="Enter your password" required>
          </div>
        </div>
        <button type="submit">Login</button>
      </div>
      <div v-else>
        <p>Open your authenticator app to get the 2FA code.</p>
        <div class="input-group">
          <label for="otp"><i class="fas fa-key"></i> 2FA Code</label>
          <div class="input-container">
            <input type="text" id="otp" v-model="otp" placeholder="Enter your 2FA code" required>
          </div>
        </div>
        <button @click="verify2fa">Verify</button>
      </div>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>Don't have an account? <router-link to="/register">Register</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const otp = ref('')
const error = ref('')
const twoFactorRequired = ref(false)
const router = useRouter()

const login = async () => {
  error.value = ''
  try {
    const response = await axios.post('http://localhost:8000/login', {
      username: username.value,
      password: password.value
    })

    const token = response.data.access_token;
    const decodedToken = JSON.parse(atob(token.split('.')[1]));
    
    if (decodedToken.scopes.includes('2fa:verify')) {
      localStorage.setItem('token', token)
      twoFactorRequired.value = true
    } else {
      localStorage.setItem('token', token)
      router.push('/')
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'An unexpected error occurred.'
    }
  }
}

const verify2fa = async () => {
  error.value = ''
  try {
    const response = await axios.post('http://localhost:8000/2fa/verify', 
      { code: otp.value },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    )
    localStorage.setItem('token', response.data.access_token)
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