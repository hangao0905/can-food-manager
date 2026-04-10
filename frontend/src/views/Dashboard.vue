<template>
  <div class="dashboard">
    <h2 class="page-title">数据概览</h2>

    <el-row :gutter="20" class="stat-row">
      <el-col :span="6">
        <div class="stat-card brand-card">
          <div class="stat-icon">🏭</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.brands?.total || 0 }}</div>
            <div class="stat-label">收录品牌</div>
            <div class="stat-sub">
              <span class="tag domestic">国内 {{ stats.brands?.domestic || 0 }}</span>
              <span class="tag foreign">国外 {{ stats.brands?.foreign || 0 }}</span>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card flavor-card">
          <div class="stat-icon">🍖</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.flavors?.total || 0 }}</div>
            <div class="stat-label">收录口味</div>
            <div class="stat-sub">
              <span class="tag domestic">国内 {{ stats.flavors?.domestic || 0 }}</span>
              <span class="tag foreign">国外 {{ stats.flavors?.foreign || 0 }}</span>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card can-card">
          <div class="stat-icon">🥫</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.cans?.total || 0 }}</div>
            <div class="stat-label">罐头数据</div>
            <div class="stat-sub">已建立营养档案</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card user-card">
          <div class="stat-icon">👤</div>
          <div class="stat-content">
            <div class="stat-value">{{ stats.users?.total || 0 }}</div>
            <div class="stat-label">系统用户</div>
            <div class="stat-sub">已注册使用</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="stat-row">
      <el-col :span="24">
        <div class="stat-card qualify-card">
          <div class="qualify-header">
            <span class="qualify-title">📊 合格率抽样统计（样本 {{ stats.qualification?.sample_count || 0 }} 条）</span>
          </div>
          <div class="qualify-items">
            <div class="qualify-item">
              <span class="qualify-label">粗蛋白合格</span>
              <el-progress :percentage="stats.qualification?.protein_pass_rate || 0" :color="getColor(stats.qualification?.protein_pass_rate)" />
            </div>
            <div class="qualify-item">
              <span class="qualify-label">粗脂肪合格</span>
              <el-progress :percentage="stats.qualification?.fat_pass_rate || 0" :color="getColor(stats.qualification?.fat_pass_rate)" />
            </div>
            <div class="qualify-item">
              <span class="qualify-label">粗灰分合格</span>
              <el-progress :percentage="stats.qualification?.ash_pass_rate || 0" :color="getColor(stats.qualification?.ash_pass_rate)" />
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const stats = ref({})

const getColor = (val) => {
  if (val === undefined) return '#909399'
  if (val >= 80) return '#67c23a'
  if (val >= 60) return '#e6a23c'
  return '#f56c6c'
}

onMounted(async () => {
  try {
    const { data } = await axios.get('/api/stats/')
    stats.value = data
  } catch (e) {
    console.error('加载统计失败', e)
  }
})
</script>

<style scoped>
.dashboard { padding: 0; }
.page-title { font-size: 22px; margin-bottom: 24px; color: #303133; }
.stat-row { margin-bottom: 20px; }
.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-icon { font-size: 40px; }
.stat-value { font-size: 36px; font-weight: bold; color: #303133; line-height: 1; }
.stat-label { font-size: 14px; color: #909399; margin: 4px 0 8px; }
.stat-sub { display: flex; gap: 8px; }
.tag { font-size: 12px; padding: 2px 8px; border-radius: 10px; }
.tag.domestic { background: #f0f9eb; color: #67c23a; }
.tag.foreign { background: #fef0f0; color: #f56c6c; }
.qualify-card { padding: 20px 24px; }
.qualify-header { margin-bottom: 16px; }
.qualify-title { font-size: 15px; color: #303133; font-weight: 600; }
.qualify-items { display: flex; flex-direction: column; gap: 14px; }
.qualify-item { display: flex; align-items: center; gap: 16px; }
.qualify-label { width: 100px; font-size: 14px; color: #606266; flex-shrink: 0; }
</style>
