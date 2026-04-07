<template>
  <el-container class="app-container">
    <el-aside width="200px" v-if="isLoggedIn">
      <div class="logo-area">
        <span class="logo-text">罐头系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="app-menu"
      >
        <el-menu-item index="/brands">
          <el-icon><Shop /></el-icon>
          <span>品牌管理</span>
        </el-menu-item>
        <el-menu-item index="/flavors">
          <el-icon><Dish /></el-icon>
          <span>口味管理</span>
        </el-menu-item>
        <el-menu-item index="/can-foods">
          <el-icon><Box /></el-icon>
          <span>罐头管理</span>
        </el-menu-item>
        <el-menu-item index="/query">
          <el-icon><Search /></el-icon>
          <span>组合查询</span>
        </el-menu-item>
        <el-menu-item index="/standards">
          <el-icon><Setting /></el-icon>
          <span>计算标准</span>
        </el-menu-item>
        <el-menu-item index="/users" v-if="isAdmin">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
      <div class="user-info">
        <span class="username">{{ username }}</span>
        <el-button type="danger" size="small" @click="logout">登出</el-button>
      </div>
    </el-aside>
    <el-main class="app-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Shop, Dish, Box, Search, Setting, User } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const token = localStorage.getItem('token')
const user = JSON.parse(localStorage.getItem('user') || '{}')
const isLoggedIn = ref(!!token)
const isAdmin = ref(user.role === 'admin')
const username = ref(user.username || '')

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif; }
</style>

<style scoped>
.app-container { height: 100vh; }
.app-header { background: #409eff; color: white; display: flex; align-items: center; font-size: 18px; }
.app-aside { background: #f5f7fa; border-right: 1px solid #e4e7ed; display: flex; flex-direction: column; overflow: hidden; }
.logo-area { padding: 16px; font-size: 16px; font-weight: bold; color: #409eff; border-bottom: 1px solid #e4e7ed; text-align: center; }
.app-menu { border: none; background: transparent; flex: 1; }
.app-main { background: #f5f7fa; padding: 20px; overflow-y: auto; }
.user-info { padding: 12px 16px; border-top: 1px solid #e4e7ed; display: flex; align-items: center; justify-content: space-between; }
.username { font-size: 13px; color: #606266; }
</style>
