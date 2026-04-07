<template>
  <div class="page-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>罐头管理</span>
          <el-button type="primary" @click="showDialog('create')">新增罐头</el-button>
        </div>
      </template>
      
      <el-table :data="canFoods" stripe v-loading="loading">
        <el-table-column prop="code" label="ID" width="100" />
        <el-table-column prop="brand.name" label="品牌" width="120" />
        <el-table-column prop="flavor.name" label="口味" width="100" />
        <el-table-column prop="description" label="简介" show-overflow-tooltip min-width="200" />
        <el-table-column prop="protein" label="蛋白%" width="70">
          <template #default="{ row }">{{ row.protein ? (row.protein*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat" label="脂肪%" width="70">
          <template #default="{ row }">{{ row.fat ? (row.fat*100).toFixed(1)+'%' : '-' }}</template>
        </el-table-column>
        <el-table-column prop="creator" label="创建人" width="100" />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

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
                <el-option v-for="f in filteredFlavors" :key="f.code" :label="f.name" :value="f.code" />
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
          <el-col :span="8"><el-form-item label="钙磷比"><el-input-number v-model="form.ca_ph_ratio" :min="0" :precision="4" /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">营养成分（干物质）</el-divider>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="钙干物质"><el-input-number v-model="form.calcium_dm" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="磷干物质"><el-input-number v-model="form.phosphorus_dm" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="钙mg/1000kal"><el-input-number v-model="form.calcium_per_1000kal" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="磷mg/1000kal"><el-input-number v-model="form.phosphorus_per_1000kal" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="磷含量指标"><el-input v-model="form.phosphorus_level" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="NFE计算-干基"><el-input-number v-model="form.nfe_dm" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="蛋白质-干基"><el-input-number v-model="form.protein_dm" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="脂肪-干基"><el-input-number v-model="form.fat_dm" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗灰分-干基"><el-input-number v-model="form.ash_dm" :min="0" :precision="4" /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">代谢能</el-divider>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="碳水代谢能占比%"><el-input-number v-model="form.carb_met_energy_pct" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="蛋白代谢能占比%"><el-input-number v-model="form.protein_met_energy_pct" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="脂肪代谢能占比%"><el-input-number v-model="form.fat_met_energy_pct" :min="0" :precision="4" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="1kg总热量kcal"><el-input-number v-model="form.total_energy_kcal" :min="0" :precision="2" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="碳水kcal"><el-input-number v-model="form.carb_kcal" :min="0" :precision="2" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="蛋白质kcal"><el-input-number v-model="form.protein_kcal" :min="0" :precision="2" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="脂肪kcal"><el-input-number v-model="form.fat_kcal" :min="0" :precision="2" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="标注kcal"><el-input-number v-model="form.labeled_kcal" :min="0" :precision="2" /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">合格指标</el-divider>
        <el-row :gutter="12">
          <el-col :span="8"><el-form-item label="粗蛋白合格"><el-input v-model="form.protein_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗脂肪合格"><el-input v-model="form.fat_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗纤维合格"><el-input v-model="form.fiber_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="粗灰分合格"><el-input v-model="form.ash_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="含水量合格"><el-input v-model="form.moisture_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="钙磷合格"><el-input v-model="form.ca_ph_pass" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="蛋白质：脂肪"><el-input-number v-model="form.protein_fat_ratio" :min="0" :precision="4" /></el-form-item></el-col>
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
const form = ref(getDefaultForm())

function getDefaultForm() {
  return {
    brand_code: '', flavor_code: '', description: '', creator: '',
    protein: null, fat: null, ash: null, fiber: null, moisture: null,
    calcium_wet: null, phosphorus_wet: null, nfe_wet: null, ca_ph_ratio: null,
    calcium_dm: null, phosphorus_dm: null, calcium_per_1000kal: null, phosphorus_per_1000kal: null,
    phosphorus_level: '', nfe_dm: null, protein_dm: null, fat_dm: null, ash_dm: null,
    carb_met_energy_pct: null, protein_met_energy_pct: null, fat_met_energy_pct: null,
    total_energy_kcal: null, carb_kcal: null, protein_kcal: null, fat_kcal: null, labeled_kcal: null,
    protein_pass: '', fat_pass: '', fiber_pass: '', ash_pass: '', moisture_pass: '', ca_ph_pass: '',
    protein_fat_ratio: null, protein_level: '',
  }
}

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

const filteredFlavors = computed(() => {
  if (!form.value.brand_code) return flavors.value
  return flavors.value.filter(f => f.brand_code === form.value.brand_code)
})

const onBrandChange = () => { form.value.flavor_code = '' }

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
  try { const { data } = await brandApi.list(); brands.value = data } catch (e) { console.error(e) }
}

const loadFlavors = async () => {
  try { const { data } = await flavorApi.list(); flavors.value = data } catch (e) { console.error(e) }
}

const showDialog = (type, row = null) => {
  dialogType.value = type
  if (type === 'edit' && row) {
    const f = { code: row.code }
    const fields = ['brand_code','flavor_code','description','creator','protein','fat','ash','fiber','moisture',
      'calcium_wet','phosphorus_wet','nfe_wet','ca_ph_ratio','calcium_dm','phosphorus_dm',
      'calcium_per_1000kal','phosphorus_per_1000kal','phosphorus_level','nfe_dm','protein_dm','fat_dm','ash_dm',
      'carb_met_energy_pct','protein_met_energy_pct','fat_met_energy_pct','total_energy_kcal',
      'carb_kcal','protein_kcal','fat_kcal','labeled_kcal',
      'protein_pass','fat_pass','fiber_pass','ash_pass','moisture_pass','ca_ph_pass',
      'protein_fat_ratio','protein_level']
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
.page-container { height: 100%; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
