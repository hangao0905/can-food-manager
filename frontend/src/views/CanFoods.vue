<template>
  <div class="page-container">
    <!-- 上部：查询条件 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm">
        <el-form-item label="品牌">
          <el-select v-model="filterForm.brand_code" placeholder="全部" clearable style="width: 180px" @change="onBrandFilterChange">
            <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="口味">
          <el-select v-model="filterForm.flavor_code" placeholder="全部" clearable style="width: 180px">
            <el-option v-for="f in filterFlavors" :key="f.code" :label="f.name" :value="f.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="罐头名称">
          <el-input v-model="filterForm.keyword" placeholder="模糊搜索罐头简介" clearable style="width: 160px" />
        </el-form-item>
        <el-form-item label="蛋白合格">
          <el-select v-model="filterForm.protein_pass" placeholder="全部" clearable style="width: 120px">
            <el-option value="合格" label="合格" />
            <el-option value="不合格" label="不合格" />
          </el-select>
        </el-form-item>
        <el-form-item label="创建人">
          <el-input v-model="filterForm.creator" placeholder="模糊搜索" clearable style="width: 120px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="showDialog('create')">新增罐头</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 下部：数据明细 -->
    <el-card class="table-card">
      <el-table :data="pagedData" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="70" />
        <el-table-column prop="brand.name" label="品牌" width="90" />
        <el-table-column prop="flavor.name" label="口味" width="90" />
        <el-table-column prop="description" label="简介" width="120" show-overflow-tooltip />
        <el-table-column prop="total_energy_kcal" label="热量" width="80" sortable>
          <template #default="{ row }">{{ row.total_energy_kcal ? Math.round(row.total_energy_kcal)+'kcal/kg' : '-' }}</template>
        </el-table-column>
        <el-table-column label="蛋白%" width="70" sortable align="center">
          <template #default="{ row }">{{ row.protein != null ? (row.protein*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="脂肪%" width="70" sortable align="center">
          <template #default="{ row }">{{ row.fat != null ? (row.fat*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="灰分%" width="70" sortable align="center">
          <template #default="{ row }">{{ row.ash != null ? (row.ash*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="纤维%" width="70" sortable align="center">
          <template #default="{ row }">{{ row.fiber != null ? (row.fiber*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="水分%" width="70" sortable align="center">
          <template #default="{ row }">{{ row.moisture != null ? (row.moisture*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="钙%" width="75" sortable align="center">
          <template #default="{ row }">{{ row.calcium_wet != null ? (row.calcium_wet*100).toFixed(3)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column label="磷%" width="75" sortable align="center">
          <template #default="{ row }">{{ row.phosphorus_wet != null ? (row.phosphorus_wet*100).toFixed(3)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="protein_pass" label="蛋白合格" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.protein_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.protein_pass || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="fat_pass" label="脂肪合格" width="80" align="center">
          <template #default="{ row }">
            <el-tag :type="row.fat_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.fat_pass || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ca_ph_pass" label="钙磷比合格" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.ca_ph_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.ca_ph_pass || '-' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" width="80" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredData.length"
          layout="total, sizes, prev, pager, next"
          background
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="900px" @closed="resetForm">
      <el-form :model="form" label-width="110px">
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="品牌">
              <el-select v-model="form.brand_code" placeholder="请选择品牌" @change="onBrandChange">
                <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="口味">
              <el-select v-model="form.flavor_code" placeholder="请先选品牌">
                <el-option v-for="f in dialogFlavors" :key="f.code" :label="f.name" :value="f.code" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="创建人">
              <el-input v-model="form.creator" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="罐头简介">
          <el-input v-model="form.description" type="textarea" rows="2" />
        </el-form-item>

        <el-divider content-position="left">营养成分（湿基）</el-divider>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="蛋白质含量"><el-input-number v-model="form.protein" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="脂肪含量"><el-input-number v-model="form.fat" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗灰分含量"><el-input-number v-model="form.ash" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗纤维含量"><el-input-number v-model="form.fiber" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="水分含量"><el-input-number v-model="form.moisture" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗NFE(碳水)"><el-input-number v-model="form.nfe_wet" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="钙含量-湿基"><el-input-number v-model="form.calcium_wet" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="磷含量-湿基"><el-input-number v-model="form.phosphorus_wet" :min="0" :precision="4" /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">合格指标</el-divider>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="粗蛋白合格"><el-input v-model="form.protein_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗脂肪合格"><el-input v-model="form.fat_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗纤维合格"><el-input v-model="form.fiber_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗灰分合格"><el-input v-model="form.ash_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="含水量合格"><el-input v-model="form.moisture_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="钙磷合格"><el-input v-model="form.ca_ph_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="蛋白质含量合格"><el-input v-model="form.protein_level" /></el-form-item></el-col>
        </el-row>
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
import { canFoodApi, brandApi, flavorApi } from '../api'

const canFoods = ref([])
const brands = ref([])
const flavors = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const dialogFlavors = ref([])
const filterForm = ref({ brand_code: '', flavor_code: '', keyword: '', protein_pass: '', creator: '' })
const pagination = ref({ page: 1, pageSize: 20 })
const form = ref(getDefaultForm())

function getDefaultForm() {
  return {
    brand_code: '', flavor_code: '', description: '', creator: '',
    protein: null, fat: null, ash: null, fiber: null, moisture: null,
    calcium_wet: null, phosphorus_wet: null, nfe_wet: null,
    protein_pass: '', fat_pass: '', fiber_pass: '', ash_pass: '',
    moisture_pass: '', ca_ph_pass: '', protein_level: '',
  }
}

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

const filterFlavors = computed(() => {
  if (!filterForm.value.brand_code) return flavors.value
  return flavors.value.filter(f => f.brand_code === filterForm.value.brand_code)
})

const onBrandFilterChange = () => {
  filterForm.value.flavor_code = ''
}

const onBrandChange = () => {
  form.value.flavor_code = ''
  dialogFlavors.value = flavors.value.filter(f => f.brand_code === form.value.brand_code)
}

const filteredData = computed(() => {
  return canFoods.value.filter(c => {
    if (filterForm.value.brand_code && c.brand_code !== filterForm.value.brand_code) return false
    if (filterForm.value.flavor_code && c.flavor_code !== filterForm.value.flavor_code) return false
    if (filterForm.value.protein_pass && c.protein_pass !== filterForm.value.protein_pass) return false
    if (filterForm.value.keyword && !c.description?.includes(filterForm.value.keyword)) return false
    if (filterForm.value.creator && !c.creator?.includes(filterForm.value.creator)) return false
    return true
  })
})

const pagedData = computed(() => {
  const start = (pagination.value.page - 1) * pagination.value.pageSize
  return filteredData.value.slice(start, start + pagination.value.pageSize)
})

const loadCanFoods = async () => {
  loading.value = true
  try {
    const { data } = await canFoodApi.list()
    canFoods.value = data
  } catch (error) {
    ElMessage.error('加载罐头失败')
  } finally {
    loading.value = false
  }
}

const loadBrands = async () => {
  try { const { data } = await brandApi.list(); brands.value = data } catch (e) {}
}

const loadFlavors = async () => {
  try { const { data } = await flavorApi.list(); flavors.value = data } catch (e) {}
}

const handleSearch = () => { pagination.value.page = 1 }
const handleReset = () => { filterForm.value = { brand_code: '', flavor_code: '', keyword: '', protein_pass: '', creator: '' }; pagination.value.page = 1 }

const showDialog = (type, row = null) => {
  dialogType.value = type
  dialogFlavors.value = type === 'edit' && row ? flavors.value.filter(f => f.brand_code === row.brand_code) : []
  if (type === 'edit' && row) {
    const f = { code: row.code }
    const fields = ['brand_code','flavor_code','description','creator','protein','fat','ash','fiber','moisture',
      'calcium_wet','phosphorus_wet','nfe_wet','protein_pass','fat_pass','fiber_pass','ash_pass',
      'moisture_pass','ca_ph_pass','protein_level']
    fields.forEach(k => f[k] = row[k] ?? null)
    form.value = f
  } else {
    form.value = getDefaultForm()
  }
  dialogVisible.value = true
}

const resetForm = () => { form.value = getDefaultForm() }

const handleSubmit = async () => {
  try {
    if (dialogType.value === 'create') {
      await canFoodApi.create(form.value)
      ElMessage.success('创建成功')
    } else {
      await canFoodApi.update(form.value.code, form.value)
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
    if (error !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => { loadCanFoods(); loadBrands(); loadFlavors() })
</script>

<style scoped>
.page-container { display: flex; flex-direction: column; gap: 16px; height: 100%; }
.filter-card { }
.table-card { flex: 1; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
