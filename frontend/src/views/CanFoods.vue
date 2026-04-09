<template>
  <div class="page-container">
    <!-- 上卡片：查询条件 -->
    <el-card class="search-card">
      <template #header>
        <div class="card-header">
          <span>查询条件</span>
        </div>
      </template>
      
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="所属品牌">
          <el-select 
            v-model="searchForm.brand_code" 
            placeholder="全部" 
            clearable
            style="width: 150px;"
            @change="handleBrandChange"
          >
            <el-option 
              v-for="b in brands" 
              :key="b.code" 
              :label="b.name" 
              :value="b.code" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="所属口味">
          <el-select 
            v-model="searchForm.flavor_code" 
            placeholder="全部" 
            clearable
            filterable
            style="width: 150px;"
          >
            <el-option 
              v-for="f in filteredFlavors" 
              :key="f.code" 
              :label="f.name" 
              :value="f.code" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="磷含量(mg)">
          <el-input-number 
            v-model="searchForm.min_phosphorus" 
            :min="0" 
            :precision="1"
            placeholder="最小值"
            style="width: 100px;"
          />
          <span style="margin: 0 8px;">-</span>
          <el-input-number 
            v-model="searchForm.max_phosphorus" 
            :min="0" 
            :precision="1"
            placeholder="最大值"
            style="width: 100px;"
          />
        </el-form-item>
        <el-form-item label="蛋白质合格">
          <el-select v-model="searchForm.protein_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="脂肪合格">
          <el-select v-model="searchForm.fat_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="纤维合格">
          <el-select v-model="searchForm.fiber_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="灰分合格">
          <el-select v-model="searchForm.ash_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="水分合格">
          <el-select v-model="searchForm.moisture_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="钙磷合格">
          <el-select v-model="searchForm.ca_ph_pass" placeholder="全部" clearable style="width: 100px;">
            <el-option label="合格" value="合格" />
            <el-option label="不合格" value="不合格" />
          </el-select>
        </el-form-item>
      </el-form>
      
      <div class="button-group">
        <el-button type="primary" @click="handleSearch">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
      </div>
    </el-card>

    <!-- 下卡片：查询结果 -->
    <el-card class="result-card">
      <template #header>
        <div class="card-header">
          <span>查询结果 (共 {{ total }} 条)</span>
          <el-button type="success" @click="showDialog('create')">新增罐头</el-button>
        </div>
      </template>
      
      <el-table :data="canFoods" stripe v-loading="loading" scrollbar-always-on>
        <el-table-column prop="code" label="Code" width="70" fixed />
        <el-table-column prop="brand.name" label="品牌" width="100" fixed show-overflow-tooltip />
        <el-table-column prop="flavor.name" label="口味" width="80" fixed show-overflow-tooltip />
        <el-table-column prop="description" label="简介" min-width="200" show-overflow-tooltip />
        <el-table-column prop="protein" label="蛋白%" width="80" align="center">
          <template #default="{ row }">{{ row.protein != null ? row.protein.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat" label="脂肪%" width="80" align="center">
          <template #default="{ row }">{{ row.fat != null ? row.fat.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="fiber" label="纤维%" width="80" align="center">
          <template #default="{ row }">{{ row.fiber != null ? row.fiber.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="ash" label="灰分%" width="80" align="center">
          <template #default="{ row }">{{ row.ash != null ? row.ash.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="moisture" label="水分%" width="80" align="center">
          <template #default="{ row }">{{ row.moisture != null ? row.moisture.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="nfe_wet" label="无抽出物%" width="90" align="center">
          <template #default="{ row }">{{ row.nfe_wet != null ? row.nfe_wet.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="phosphorus_wet" label="磷(mg/100g)" width="95" align="center" />
        <el-table-column prop="calcium_wet" label="钙(mg/100g)" width="95" align="center" />
        <el-table-column prop="ca_ph_ratio" label="钙磷比" width="75" align="center">
          <template #default="{ row }">{{ row.ca_ph_ratio ? row.ca_ph_ratio.toFixed(2) : '-' }}</template>
        </el-table-column>
        <el-table-column prop="protein_dm" label="蛋白DM%" width="85" align="center">
          <template #default="{ row }">{{ row.protein_dm != null ? row.protein_dm.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat_dm" label="脂肪DM%" width="85" align="center">
          <template #default="{ row }">{{ row.fat_dm != null ? row.fat_dm.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="total_energy_kcal" label="能量(kcal)" width="90" align="center" />
        <el-table-column prop="labeled_kcal" label="标称能量" width="80" align="center" />
        <el-table-column prop="protein_met_energy_pct" label="蛋白能量%" width="90" align="center">
          <template #default="{ row }">{{ row.protein_met_energy_pct != null ? row.protein_met_energy_pct.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat_met_energy_pct" label="脂肪能量%" width="90" align="center">
          <template #default="{ row }">{{ row.fat_met_energy_pct != null ? row.fat_met_energy_pct.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="carb_met_energy_pct" label="碳水能量%" width="95" align="center">
          <template #default="{ row }">{{ row.carb_met_energy_pct != null ? row.carb_met_energy_pct.toFixed(3) + '%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="合格判定" width="260">
          <template #default="{ row }">
            <el-tag v-if="row.protein_pass === '合格'" type="success" size="small">蛋白</el-tag>
            <el-tag v-else-if="row.protein_pass === '不合格'" type="danger" size="small">蛋白</el-tag>
            <el-tag v-if="row.fat_pass === '合格'" type="success" size="small">脂肪</el-tag>
            <el-tag v-else-if="row.fat_pass === '不合格'" type="danger" size="small">脂肪</el-tag>
            <el-tag v-if="row.fiber_pass === '合格'" type="success" size="small">纤维</el-tag>
            <el-tag v-else-if="row.fiber_pass === '不合格'" type="danger" size="small">纤维</el-tag>
            <el-tag v-if="row.ash_pass === '合格'" type="success" size="small">灰分</el-tag>
            <el-tag v-else-if="row.ash_pass === '不合格'" type="danger" size="small">灰分</el-tag>
            <el-tag v-if="row.moisture_pass === '合格'" type="success" size="small">水分</el-tag>
            <el-tag v-else-if="row.moisture_pass === '不合格'" type="danger" size="small">水分</el-tag>
            <el-tag v-if="row.ca_ph_pass === '合格'" type="success" size="small">钙磷</el-tag>
            <el-tag v-else-if="row.ca_ph_pass === '不合格'" type="danger" size="small">钙磷</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" width="80" show-overflow-tooltip />
        <el-table-column prop="created_date" label="创建时间" width="150" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px" @closed="resetForm">
      <el-form :model="form" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="品牌" required>
              <el-select v-model="form.brand_code" placeholder="请选择品牌">
                <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="口味">
              <el-select v-model="form.flavor_code" placeholder="请选择口味" clearable>
                <el-option v-for="f in flavors" :key="f.code" :label="`${f.brand?.name || ''} - ${f.name}`" :value="f.code" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="罐头名称">
          <el-input v-model="form.description" placeholder="请输入罐头名称" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" rows="2" placeholder="请输入简介" />
        </el-form-item>
        <el-divider content-position="left">营养成分（湿基）</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="蛋白质(g)">
              <el-input-number v-model="form.protein" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="脂肪(g)">
              <el-input-number v-model="form.fat" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="灰分(g)">
              <el-input-number v-model="form.ash" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="纤维(g)">
              <el-input-number v-model="form.fiber" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="水分(g)">
              <el-input-number v-model="form.moisture" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="无抽出物(g)">
              <el-input-number v-model="form.nfe_wet" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="钙(mg/100g)">
              <el-input-number v-model="form.calcium_wet" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="磷(mg/100g)">
              <el-input-number v-model="form.phosphorus_wet" :min="0" :precision="1" placeholder="0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider content-position="left">标称信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="标称能量(kcal)">
              <el-input-number v-model="form.labeled_kcal" :min="0" :precision="1" placeholder="可选" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-alert
          type="info"
          :closable="false"
          show-icon
          style="margin-top: 10px;"
        >
          <template #title>
            <span>提示：以下字段由系统根据标准自动计算</span>
          </template>
          <template #default>
            钙磷比、干物质基础指标(NFE除外)、能量、能量百分比、合格判定等字段由系统根据 /standards 中的标准自动计算，无需手工填写。
          </template>
        </el-alert>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { canFoodApi, flavorApi, brandApi } from '../api'

const canFoods = ref([])
const flavors = ref([])
const brands = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const total = ref(0)

// 分页参数
const pagination = ref({
  page: 1,
  pageSize: 20
})

// 查询表单
const searchForm = ref({
  brand_code: null,
  flavor_code: null,
  min_phosphorus: null,
  max_phosphorus: null,
  protein_pass: null,
  fat_pass: null,
  fiber_pass: null,
  ash_pass: null,
  moisture_pass: null,
  ca_ph_pass: null
})

// 对话框表单
const form = ref({
  brand_code: null, flavor_code: null, description: '',
  protein: null, fat: null, moisture: null,
  phosphorus_wet: null, calcium_wet: null,
  protein_pass: '合格', fat_pass: '合格'
})

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

// 根据品牌过滤口味
const filteredFlavors = computed(() => {
  if (!searchForm.value.brand_code) return flavors.value
  return flavors.value.filter(f => f.brand_code === searchForm.value.brand_code)
})

const defaultForm = () => ({
  brand_code: null, flavor_code: null, description: '',
  protein: null, fat: null, moisture: null,
  phosphorus_wet: null, calcium_wet: null,
  protein_pass: '合格', fat_pass: '合格'
})

// 加载罐头列表
const loadCanFoods = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.pageSize
    }
    if (searchForm.value.brand_code) params.brand_code = searchForm.value.brand_code
    if (searchForm.value.flavor_code) params.flavor_code = searchForm.value.flavor_code
    if (searchForm.value.min_phosphorus) params.min_phosphorus = searchForm.value.min_phosphorus
    if (searchForm.value.max_phosphorus) params.max_phosphorus = searchForm.value.max_phosphorus
    if (searchForm.value.protein_pass) params.protein_pass = searchForm.value.protein_pass
    if (searchForm.value.fat_pass) params.fat_pass = searchForm.value.fat_pass
    if (searchForm.value.fiber_pass) params.fiber_pass = searchForm.value.fiber_pass
    if (searchForm.value.ash_pass) params.ash_pass = searchForm.value.ash_pass
    if (searchForm.value.moisture_pass) params.moisture_pass = searchForm.value.moisture_pass
    if (searchForm.value.ca_ph_pass) params.ca_ph_pass = searchForm.value.ca_ph_pass
    
    const { data } = await canFoodApi.list(params)
    canFoods.value = data
    total.value = data.length
  } catch (error) {
    console.error('加载罐头失败', error)
    ElMessage.error('加载罐头失败')
  } finally {
    loading.value = false
  }
}

// 加载口味列表
const loadFlavors = async () => {
  try {
    const { data } = await flavorApi.list({ limit: 1000 })
    flavors.value = data.data || []
  } catch (error) {
    console.error('加载口味失败', error)
  }
}

// 加载品牌列表
const loadBrands = async () => {
  try {
    const { data } = await brandApi.list()
    brands.value = data || []
  } catch (error) {
    console.error('加载品牌失败', error)
  }
}

// 品牌选择变化
const handleBrandChange = () => {
  searchForm.value.flavor_code = null
}

// 查询
const handleSearch = () => {
  pagination.value.page = 1
  loadCanFoods()
}

// 重置
const handleReset = () => {
  searchForm.value = {
    brand_code: null,
    flavor_code: null,
    min_phosphorus: null,
    max_phosphorus: null,
    protein_pass: null,
    fat_pass: null,
    fiber_pass: null,
    ash_pass: null,
    moisture_pass: null,
    ca_ph_pass: null
  }
  pagination.value.page = 1
  pagination.value.pageSize = 20
  loadCanFoods()
}

// 分页大小改变
const handleSizeChange = () => {
  pagination.value.page = 1
  loadCanFoods()
}

// 页码改变
const handlePageChange = () => {
  loadCanFoods()
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    form.value = { ...row }
  } else {
    form.value = defaultForm()
  }
  dialogVisible.value = true
}

const resetForm = () => {
  form.value = defaultForm()
}

const handleSubmit = async () => {
  try {
    const data = { ...form.value }
    if (dialogType.value === 'create') {
      await canFoodApi.create(data)
      ElMessage.success('创建成功')
    } else {
      await canFoodApi.update(data.code, data)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadCanFoods()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该罐头?', '提示', { type: 'warning' })
    await canFoodApi.delete(row.code)
    ElMessage.success('删除成功')
    loadCanFoods()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadCanFoods()
  loadFlavors()
  loadBrands()
})
</script>

<style scoped>
.page-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.search-card {
  flex-shrink: 0;
}

.result-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-container {
  margin-top: 16px;
  display: flex;
  justify-content: flex-end;
}

.button-group {
  display: flex;
  gap: 12px;
  margin-top: 16px;
  padding-left: 8px;
}

:deep(.el-form--inline .el-form-item) {
  margin-right: 16px;
  margin-bottom: 12px;
}
</style>
