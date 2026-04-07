<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <span>组合查询</span>
      </template>
      
      <el-form :inline="true" :model="queryForm" class="query-form">
        <el-form-item label="品牌">
          <el-select v-model="queryForm.brand_id" placeholder="全部" clearable @change="onBrandChange">
            <el-option v-for="b in brands" :key="b.id" :label="b.name" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="口味">
          <el-select v-model="queryForm.flavor_id" placeholder="全部" clearable>
            <el-option v-for="f in filteredFlavors" :key="f.id" :label="f.name" :value="f.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称">
          <el-input v-model="queryForm.name" placeholder="模糊搜索" clearable />
        </el-form-item>
        <el-form-item label="合格">
          <el-select v-model="queryForm.is_quality_passed" placeholder="全部" clearable>
            <el-option label="合格" :value="true" />
            <el-option label="不合格" :value="false" />
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

      <el-table :data="results" stripe v-loading="loading" show-summary>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="罐头名称" min-width="150" />
        <el-table-column prop="flavor.brand.name" label="品牌" width="100" />
        <el-table-column prop="flavor.name" label="口味" width="100" />
        <el-table-column prop="net_weight" label="净重(g)" width="100">
          <template #default="{ row }">{{ row.net_weight || '-' }}</template>
        </el-table-column>
        <el-table-column prop="calories" label="热量" width="80" sortable>
          <template #default="{ row }">{{ row.calories || '-' }}</template>
        </el-table-column>
        <el-table-column prop="protein" label="蛋白质" width="80" sortable>
          <template #default="{ row }">{{ row.protein || '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat" label="脂肪" width="80" sortable>
          <template #default="{ row }">{{ row.fat || '-' }}</template>
        </el-table-column>
        <el-table-column prop="carbohydrate" label="碳水" width="80">
          <template #default="{ row }">{{ row.carbohydrate || '-' }}</template>
        </el-table-column>
        <el-table-column prop="phosphorus" label="磷(mg)" width="80">
          <template #default="{ row }">{{ row.phosphorus || '-' }}</template>
        </el-table-column>
        <el-table-column prop="calcium" label="钙(mg)" width="80">
          <template #default="{ row }">{{ row.calcium || '-' }}</template>
        </el-table-column>
        <el-table-column prop="is_quality_passed" label="合格" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_quality_passed ? 'success' : 'danger'" size="small">
              {{ row.is_quality_passed ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          :page-size="pagination.page_size"
          :total="pagination.total"
          layout="total, prev, pager, next"
          @current-change="loadResults"
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
const results = ref([])
const loading = ref(false)
const queryForm = ref({
  brand_id: null, flavor_id: null, name: '', is_quality_passed: null,
  min_calories: null, max_calories: null,
  min_protein: null, max_protein: null,
  min_fat: null, max_fat: null,
  page: 1, page_size: 20
})
const pagination = ref({ page: 1, page_size: 20, total: 0 })

const filteredFlavors = computed(() => {
  if (!queryForm.value.brand_id) return flavors.value
  return flavors.value.filter(f => f.brand_id === queryForm.value.brand_id)
})

const loadBrands = async () => {
  try {
    const { data } = await brandApi.list()
    brands.value = data
  } catch (error) {
    console.error('加载品牌失败', error)
  }
}

const loadFlavors = async () => {
  try {
    const { data } = await flavorApi.list({ page_size: 100 })
    flavors.value = data
  } catch (error) {
    console.error('加载口味失败', error)
  }
}

const loadResults = async () => {
  loading.value = true
  try {
    const params = { ...queryForm.value }
    Object.keys(params).forEach(key => {
      if (params[key] === null || params[key] === '') delete params[key]
    })
    const { data } = await canFoodApi.list(params)
    results.value = data
  } catch (error) {
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

const handleQuery = () => {
  queryForm.value.page = 1
  loadResults()
}

const resetQuery = () => {
  queryForm.value = {
    brand_id: null, flavor_id: null, name: '', is_quality_passed: null,
    min_calories: null, max_calories: null,
    min_protein: null, max_protein: null,
    min_fat: null, max_fat: null,
    page: 1, page_size: 20
  }
  loadResults()
}

const onBrandChange = () => {
  queryForm.value.flavor_id = null
}

onMounted(() => {
  loadBrands()
  loadFlavors()
  loadResults()
})
</script>

<style scoped>
.page-container {
  height: 100%;
}
.query-form {
  margin-bottom: 20px;
}
.ml-5 {
  margin-left: 5px;
}
.mr-5 {
  margin-right: 5px;
}
.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
