<template>
  <div class="auth-container">
    <div class="card-title">BASIC</div>
    <div class="logo">
      <i class="fas fa-user-plus"></i>
    </div>
    <h2>Create Account</h2>
    <form @submit.prevent="register">
      <div class="input-group">
        <label for="username"><i class="fas fa-user"></i> Username</label>
        <div class="input-container">
          <input type="text" id="username" v-model="username" placeholder="Choose a username" required>
        </div>
      </div>
      <div class="input-group">
        <label for="password"><i class="fas fa-lock"></i> Password</label>
        <div class="input-container">
          <input type="password" id="password" v-model="password" placeholder="Choose a strong password" required>
        </div>
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <p v-if="error" class="error">{{ error }}</p>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const register = async () => {
  error.value = ''
  try {
    await axios.post('http://localhost:8000/register', {
      username: username.value,
      password: password.value
    })
    router.push('/login')
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
      error.value = err.response.data.detail
    } else {
      error.value = 'An unexpected error occurred.'
    }
  }
}
</script>
