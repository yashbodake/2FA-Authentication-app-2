<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="card-header">
        <h1>Create Account</h1>
        <p>Join the community!</p>
      </div>
      <form @submit.prevent="register">
        <div class="input-group">
          <input type="text" id="username" v-model="username" placeholder="Username" required>
        </div>
        <div class="input-group">
          <input type="password" id="password" v-model="password" placeholder="Password" required>
        </div>
        <button type="submit" class="btn btn-primary" :disabled="loading">
          <Spinner v-if="loading" />
          <span v-else>Create Account</span>
        </button>
      </form>
      <div class="form-footer">
        <p>Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Spinner from './Spinner.vue'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const loading = ref(false)

const register = async () => {
  loading.value = true
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
  } finally {
    loading.value = false
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

.input-group input {
  width: 100%;
  padding: 15px;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  color: #FFFFFF;
  font-size: 16px;
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

.btn-primary:disabled {
  background-color: #C2185B;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 40px;
}

.form-footer a {
  color: #F5F5F5;
  text-decoration: none;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>