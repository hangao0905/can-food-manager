<template>
  <div class="login-page">
    <div class="login-card">
      <h1>罐头管理系统</h1>
      <el-form :model="form" @submit.prevent="handleLogin">
        <el-form-item>
          <el-input v-model="form.username" placeholder="用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="form.password" type="password" placeholder="密码" prefix-icon="Lock" show-password @keyup.enter="handleLogin" />
        </el-form-item>
        <el-button type="primary" class="login-btn" :loading="loading" native-type="submit" @click="handleLogin">
          登录
        </el-button>
        <div v-if="error" class="error-msg">{{ error }}</div>
      </el-form>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref('')
const form = ref({ username: '', password: '' })

// 清除全局 token
localStorage.removeItem('token')
localStorage.removeItem('user')

const handleLogin = async () => {
  if (!form.value.username || !form.value.password) {
    error.value = '请输入用户名和密码'
    return
  }
  loading.value = true
  error.value = ''
  try {
    const { data } = await axios.post('/auth/login', {
      username: form.value.username,
      password: form.value.password
    })
    localStorage.setItem('token', data.access_token)
    localStorage.setItem('user', JSON.stringify(data.user))
    ElMessage.success('登录成功')
    router.push('/brands')
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  width: 360px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.login-card h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 22px;
  color: #333;
}
.login-btn {
  width: 100%;
  height: 40px;
  font-size: 16px;
}
.error-msg {
  color: #f56c6c;
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
}
</style>
