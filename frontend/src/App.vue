<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <h1>🥫 罐头信息管理系统</h1>
    </el-header>
    <el-container>
      <el-aside width="200px" class="app-aside">
        <el-menu :default-active="$route.path" router>
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
        </el-menu>
      </el-aside>
      <el-main class="app-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { Shop, Dish, Box, Search, Setting } from '@element-plus/icons-vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
.app-container {
  height: 100vh;
}
.app-header {
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
}
.app-header h1 {
  font-size: 20px;
}
.app-aside {
  background: #f5f5f5;
  padding-top: 10px;
}
.app-main {
  background: #ffffff;
  padding: 20px;
}
</style>
