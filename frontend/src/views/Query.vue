<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>组合查询</span>
      </template>

      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="品牌">
          <el-select v-model="queryForm.brand_code" placeholder="全部" clearable style="width:180px" @change="onBrandChange">
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="口味">
          <el-select v-model="queryForm.flavor_code" placeholder="全部" clearable style="width:180px">
            <el-option v-for="f in filteredFlavors" :key="f.code" :label="f.name" :value="f.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="罐头简介">
          <el-input v-model="queryForm.keyword" placeholder="模糊搜索" clearable style="width:160px" />
        </el-form-item>
        <el-form-item label="蛋白合格">
          <el-select v-model="queryForm.protein_pass" placeholder="全部" clearable style="width:120px">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <br />
        <el-form-item label="热量范围">
          <el-input-number v-model="queryForm.min_calories" placeholder="最小" :min="0" style="width: 100px" />
          <span class="ml-5 mr-5">-</span>
          <el-input-number v-model="queryForm.max_calories" placeholder="最大" :min="0" style="width: 100px" />
        </el-form-item>
        <el-form-item label="蛋白质范围">
          <el-input-number v-model="queryForm.min_protein" placeholder="最小" :min="0" style="width: 100px" />
          <span class="ml-5 mr-5">-</span>
          <el-input-number v-model="queryForm.max_protein" placeholder="最大" :min="0" style="width: 100px" />
        </el-form-item>
        <el-form-item label="脂肪范围">
          <el-input-number v-model="queryForm.min_fat" placeholder="最小" :min="0" style="width: 100px" />
          <span class="ml-5 mr-5">-</span>
          <el-input-number v-model="queryForm.max_fat" placeholder="最大" :min="0" style="width: 100px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="pagedResults" stripe v-loading="loading" show-summary>
        <el-table-column prop="code" label="ID" width="80" />
        <el-table-column prop="description" label="罐头简介" min-width="150" show-overflow-tooltip />
        <el-table-column prop="brand.name" label="品牌" width="100" />
        <el-table-column prop="flavor.name" label="口味" width="100" />
        <el-table-column prop="net_weight" label="净重(g)" width="100">
          <template #default="{ row }">{{ row.net_weight || '-' }}</template>
        </el-table-column>
        <el-table-column prop="total_energy_kcal" label="热量(kcal/kg)" width="100" sortable>
          <template #default="{ row }">{{ row.total_energy_kcal ? Math.round(row.total_energy_kcal) : '-' }}</template>
        </el-table-column>
        <el-table-column label="蛋白%" width="80" sortable align="center">
          <template #default="{ row }">{{ row.protein != null ? (row.protein*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="脂肪%" width="80" sortable align="center">
          <template #default="{ row }">{{ row.fat != null ? (row.fat*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="protein_pass" label="蛋白合格" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.protein_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.protein_pass || '-' }}</el-tag>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="filteredResults.length"
          layout="total, sizes, prev, pager, next"
          :page-sizes="[10, 20, 50, 100]"
          background
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { canFoodApi, brandApi, flavorApi } from '../api'

const brands = ref([])
const flavors = ref([])
const allCanFoods = ref([])
const loading = ref(false)
const queryForm = ref({
  brand_code: null, flavor_code: null, keyword: '', protein_pass: null,
  min_calories: null, max_calories: null,
  min_protein: null, max_protein: null,
  min_fat: null, max_fat: null,
})
const pagination = ref({ page: 1, pageSize: 20 })

const filteredFlavors = computed(() => {
  if (!queryForm.value.brand_code) return flavors.value
  return flavors.value.filter(f => f.brand_code === queryForm.value.brand_code)
})

const filteredResults = computed(() => {
  return allCanFoods.value.filter(c => {
    if (queryForm.value.brand_code && c.brand_code !== queryForm.value.brand_code) return false
    if (queryForm.value.flavor_code && c.flavor_code !== queryForm.value.flavor_code) return false
    if (queryForm.value.keyword && !c.description?.includes(queryForm.value.keyword)) return false
    if (queryForm.value.protein_pass && c.protein_pass !== queryForm.value.protein_pass) return false
    if (queryForm.value.min_calories != null && (c.total_energy_kcal == null || c.total_energy_kcal < queryForm.value.min_calories)) return false
    if (queryForm.value.max_calories != null && (c.total_energy_kcal == null || c.total_energy_kcal > queryForm.value.max_calories)) return false
    if (queryForm.value.min_protein != null && (c.protein == null || c.protein < queryForm.value.min_protein)) return false
    if (queryForm.value.max_protein != null && (c.protein == null || c.protein > queryForm.value.max_protein)) return false
    if (queryForm.value.min_fat != null && (c.fat == null || c.fat < queryForm.value.min_fat)) return false
    if (queryForm.value.max_fat != null && (c.fat == null || c.fat > queryForm.value.max_fat)) return false
    return true
  })
})

const pagedResults = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.pageSize
  return filteredResults.value.slice(start, start + pagination.value.pageSize)
})

const loadBrands = async () => {
  try { const { data } = await brandApi.list(); brands.value = data } catch (e) { ElMessage.error('加载品牌失败') }
}

const loadFlavors = async () => {
  try { const { data } = await flavorApi.list({ page_size: 500 }); flavors.value = data } catch (e) { ElMessage.error('加载口味失败') }
}

const loadAll = async () => {
  loading.value = true
  try {
    const { data } = await canFoodApi.list({ page: 1, page_size: 500 })
    allCanFoods.value = data
  } catch (error) {
    ElMessage.error('加载罐头数据失败')
  } finally {
    loading.value = false
  }
}

const handleQuery = () => { pagination.value.page = 1 }

const resetQuery = () => {
  queryForm.value = { brand_code: null, flavor_code: null, keyword: '', protein_pass: null, min_calories: null, max_calories: null, min_protein: null, max_protein: null, min_fat: null, max_fat: null }
  pagination.value.page = 1
}

const onBrandChange = () => { queryForm.value.flavor_code = null }

onMounted(() => { loadBrands(); loadFlavors(); loadAll() })
</script>

<style scoped>
.page-container { height: 100%; }
.query-form { margin-bottom: 20px; }
.ml-5 { margin-left: 5px; }
.mr-5 { margin-right: 5px; }
.pagination-container { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
