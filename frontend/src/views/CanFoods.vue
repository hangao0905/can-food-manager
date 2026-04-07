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
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="罐头名称" min-width="150" />
        <el-table-column prop="flavor.brand.name" label="品牌" width="100" />
        <el-table-column prop="flavor.name" label="口味" width="100" />
        <el-table-column prop="calories" label="热量" width="80">
          <template #default="{ row }">{{ row.calories || '-' }}</template>
        </el-table-column>
        <el-table-column prop="protein" label="蛋白质" width="80">
          <template #default="{ row }">{{ row.protein || '-' }}</template>
        </el-table-column>
        <el-table-column prop="fat" label="脂肪" width="80">
          <template #default="{ row }">{{ row.fat || '-' }}</template>
        </el-table-column>
        <el-table-column prop="is_quality_passed" label="合格" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_quality_passed ? 'success' : 'danger'">
              {{ row.is_quality_passed ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="700px" @closed="resetForm">
      <el-form :model="form" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="罐头名称">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="口味">
              <el-select v-model="form.flavor_id" placeholder="请选择口味">
                <el-option v-for="f in flavors" :key="f.id" :label="`${f.brand?.name || ''} - ${f.name}`" :value="f.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="条形码">
              <el-input v-model="form.barcode" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="净重(g)">
              <el-input-number v-model="form.net_weight" :min="0" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider content-position="left">营养成分 (每100g)</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="热量(kcal)">
              <el-input-number v-model="form.calories" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="蛋白质(g)">
              <el-input-number v-model="form.protein" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="脂肪(g)">
              <el-input-number v-model="form.fat" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="碳水(g)">
              <el-input-number v-model="form.carbohydrate" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="水分(g)">
              <el-input-number v-model="form.moisture" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="磷(mg)">
              <el-input-number v-model="form.phosphorus" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="钙(mg)">
              <el-input-number v-model="form.calcium" :min="0" :precision="1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="沥干重(g)">
              <el-input-number v-model="form.drained_weight" :min="0" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="合格">
              <el-switch v-model="form.is_quality_passed" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="合格说明">
          <el-input v-model="form.quality_notes" />
        </el-form-item>
        <el-form-item label="简介">
          <el-input v-model="form.description" type="textarea" rows="3" />
        </el-form-item>
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
import { canFoodApi, flavorApi } from '../api'

const canFoods = ref([])
const flavors = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref('create')
const form = ref({
  name: '', flavor_id: '', barcode: '', net_weight: null, drained_weight: null,
  calories: null, protein: null, fat: null, carbohydrate: null, moisture: null,
  phosphorus: null, calcium: null, is_quality_passed: true, quality_notes: '', description: ''
})

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

const defaultForm = () => ({
  name: '', flavor_id: '', barcode: '', net_weight: null, drained_weight: null,
  calories: null, protein: null, fat: null, carbohydrate: null, moisture: null,
  phosphorus: null, calcium: null, is_quality_passed: true, quality_notes: '', description: ''
})

const loadCanFoods = async () => {
  loading.value = true
  try {
    const { data } = await canFoodApi.list({ page_size: 100 })
    canFoods.value = data
  } catch (error) {
    ElMessage.error('加载罐头失败')
  } finally {
    loading.value = false
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
      await canFoodApi.update(data.id, data)
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
    await canFoodApi.delete(row.id)
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
})
</script>

<style scoped>
.page-container {
  height: 100%;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
