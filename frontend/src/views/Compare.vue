<template>
  <div class="page-container">
    <!-- 页面标题 -->
    <h2 class="page-title">罐头营养对比</h2>

    <!-- 筛选区域 -->
    <el-card class="filter-card" shadow="never">
      <el-row :gutter="16">
        <el-col :span="6">
          <el-form-item label="品牌">
            <el-select v-model="filterBrand" placeholder="全部品牌" clearable style="width:100%">
              <el-option v-for="b in brands" :key="b.code" :label="b.name" :value="b.code" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="口味">
            <el-select v-model="filterFlavor" placeholder="全部口味" clearable :disabled="!filterBrand" style="width:100%">
              <el-option v-for="f in filteredFlavors" :key="f.code" :label="f.name" :value="f.code" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="选择罐头对比（2-5个）">
            <el-select
              v-model="selectedCodes"
              multiple
              filterable
              placeholder="搜索罐头..."
              style="width:100%"
              :multiple-limit="5"
            >
              <el-option
                v-for="c in filteredCanFoods"
                :key="c.code"
                :label="`${c.brand?.name || ''} - ${c.flavor?.name || ''} - ${(c.description || '').slice(0, 20)}`"
                :value="c.code"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="4" style="padding-top:18px">
          <el-button @click="selectedCodes = []">清空选择</el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 无选择时提示 -->
    <el-empty v-if="selectedItems.length === 0" description="请从上方选择 2~5 个罐头进行对比" />

    <!-- 对比看板 -->
    <div v-else class="compare-grid">
      <div v-for="item in selectedItems" :key="item.code" class="compare-card">

        <!-- 卡片头部 -->
        <div class="card-header">
          <div class="card-title">
            <span class="brand-name">{{ item.brand?.name || '未知品牌' }}</span>
            <span class="flavor-name">{{ item.flavor?.name || '' }}</span>
          </div>
          <div class="card-desc">{{ item.description || '暂无简介' }}</div>
          <div class="card-meta">
            <el-tag size="small" type="info">{{ item.creator || '-' }}</el-tag>
            <el-tag v-if="item.protein_pass === '合格'" size="small" type="success">蛋白合格</el-tag>
            <el-tag v-else-if="item.protein_pass === '不合格'" size="small" type="danger">蛋白不合格</el-tag>
          </div>
          <el-image
            v-if="item.photo"
            :src="item.photo"
            fit="cover"
            class="card-photo"
            :preview-src-list="[item.photo]"
          />
        </div>

        <!-- 营养成分表格 -->
        <div class="section">
          <div class="section-title">湿基成分（%）</div>
          <table class="metric-table">
            <tr><td>蛋白质</td><td>{{ pct(item.protein) }}</td></tr>
            <tr><td>脂肪</td><td>{{ pct(item.fat) }}</td></tr>
            <tr><td>粗灰分</td><td>{{ pct(item.ash) }}</td></tr>
            <tr><td>粗纤维</td><td>{{ pct(item.fiber) }}</td></tr>
            <tr><td>水分</td><td>{{ pct(item.moisture) }}</td></tr>
            <tr><td>NFE（无氮浸出物）</td><td>{{ pct(item.nfe_wet) }}</td></tr>
            <tr><td>钙（湿基）</td><td>{{ pct(item.calcium_wet) }}</td></tr>
            <tr><td>磷（湿基）</td><td>{{ pct(item.phosphorus_wet) }}</td></tr>
          </table>
        </div>

        <el-divider />

        <div class="section">
          <div class="section-title">干基成分（%）</div>
          <table class="metric-table">
            <tr><td>蛋白-干基</td><td :class="highlight(item.protein_dm, 0.5)">{{ pct(item.protein_dm) }}</td></tr>
            <tr><td>脂肪-干基</td><td>{{ pct(item.fat_dm) }}</td></tr>
            <tr><td>灰分-干基</td><td>{{ pct(item.ash_dm) }}</td></tr>
            <tr><td>NFE-干基</td><td>{{ pct(item.nfe_dm) }}</td></tr>
            <tr><td>钙-干基</td><td>{{ pct(item.calcium_dm) }}</td></tr>
            <tr><td>磷-干基</td><td>{{ pct(item.phosphorus_dm) }}</td></tr>
          </table>
        </div>

        <el-divider />

        <div class="section">
          <div class="section-title">热量与代谢能</div>
          <table class="metric-table">
            <tr><td>总热量</td><td class="highlight-val">{{ item.total_energy_kcal ? Math.round(item.total_energy_kcal) + ' kcal/kg' : '-' }}</td></tr>
            <tr><td>标注热量</td><td>{{ item.labeled_kcal != null ? item.labeled_kcal + ' kcal/kg' : '-' }}</td></tr>
            <tr><td>蛋白kcal/kg</td><td>{{ item.protein_kcal ? Math.round(item.protein_kcal) : '-' }}</td></tr>
            <tr><td>脂肪kcal/kg</td><td>{{ item.fat_kcal ? Math.round(item.fat_kcal) : '-' }}</td></tr>
            <tr><td>碳水kcal/kg</td><td>{{ item.carb_kcal ? Math.round(item.carb_kcal) : '-' }}</td></tr>
            <tr><td>蛋白代谢能%</td><td>{{ pct(item.protein_met_energy_pct) }}</td></tr>
            <tr><td>脂肪代谢能%</td><td>{{ pct(item.fat_met_energy_pct) }}</td></tr>
            <tr><td>碳水代谢能%</td><td>{{ pct(item.carb_met_energy_pct) }}</td></tr>
          </table>
        </div>

        <el-divider />

        <div class="section">
          <div class="section-title">关键比例与指标</div>
          <table class="metric-table">
            <tr>
              <td>钙磷比</td>
              <td>
                <span class="highlight-val">{{ item.ca_ph_ratio != null ? item.ca_ph_ratio.toFixed(2) : '-' }}</span>
                <el-tag v-if="item.ca_ph_pass === '合格'" size="small" type="success" style="margin-left:6px">合格</el-tag>
                <el-tag v-else-if="item.ca_ph_pass === '不合格'" size="small" type="danger" style="margin-left:6px">不合格</el-tag>
              </td>
            </tr>
            <tr><td>钙mg/1000kcal</td><td>{{ item.calcium_per_1000kal != null ? Math.round(item.calcium_per_1000kal) : '-' }}</td></tr>
            <tr><td>磷mg/1000kcal</td><td>{{ item.phosphorus_per_1000kal != null ? Math.round(item.phosphorus_per_1000kal) : '-' }}</td></tr>
            <tr><td>蛋白:脂肪</td><td>{{ item.protein_fat_ratio != null ? item.protein_fat_ratio.toFixed(2) : '-' }}</td></tr>
            <tr>
              <td>磷水平</td>
              <td>
                <el-tag v-if="item.phosphorus_level === '高磷'" size="small" type="danger">{{ item.phosphorus_level }}</el-tag>
                <el-tag v-else-if="item.phosphorus_level === '低磷'" size="small" type="success">{{ item.phosphorus_level }}</el-tag>
                <el-tag v-else-if="item.phosphorus_level === '中磷'" size="small" type="warning">{{ item.phosphorus_level }}</el-tag>
                <span v-else>-</span>
              </td>
            </tr>
            <tr>
              <td>蛋白水平</td>
              <td>
                <el-tag v-if="item.protein_level === '优秀'" size="small" type="success">{{ item.protein_level }}</el-tag>
                <el-tag v-else-if="item.protein_level === '一般'" size="small" type="warning">{{ item.protein_level }}</el-tag>
                <el-tag v-else-if="item.protein_level === '不合格'" size="small" type="danger">{{ item.protein_level }}</el-tag>
                <span v-else>-</span>
              </td>
            </tr>
          </table>
        </div>

        <el-divider />

        <div class="section">
          <div class="section-title">合格指标</div>
          <div class="pass-grid">
            <div class="pass-item" :class="passClass(item.protein_pass)">
              <span>蛋白</span>
              <span>{{ item.protein_pass || '-' }}</span>
            </div>
            <div class="pass-item" :class="passClass(item.fat_pass)">
              <span>脂肪</span>
              <span>{{ item.fat_pass || '-' }}</span>
            </div>
            <div class="pass-item" :class="passClass(item.fiber_pass)">
              <span>纤维</span>
              <span>{{ item.fiber_pass || '-' }}</span>
            </div>
            <div class="pass-item" :class="passClass(item.ash_pass)">
              <span>灰分</span>
              <span>{{ item.ash_pass || '-' }}</span>
            </div>
            <div class="pass-item" :class="passClass(item.moisture_pass)">
              <span>水分</span>
              <span>{{ item.moisture_pass || '-' }}</span>
            </div>
            <div class="pass-item" :class="passClass(item.ca_ph_pass)">
              <span>钙磷比</span>
              <span>{{ item.ca_ph_pass || '-' }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { canFoodApi, brandApi, flavorApi } from '../api/index.js'
import { ElMessage } from 'element-plus'

const brands = ref([])
const flavors = ref([])
const canFoods = ref([])
const filterBrand = ref('')
const filterFlavor = ref('')
const selectedCodes = ref([])

const loading = ref(false)

// 挂载时加载品牌和口味
onMounted(async () => {
  loading.value = true
  try {
    const [bRes, cRes] = await Promise.all([
      brandApi.list(),
      canFoodApi.list({ page_size: 500 })
    ])
    brands.value = bRes.data
    canFoods.value = cRes.data.data || []
  } catch {
    // ignore
  } finally {
    loading.value = false
  }
  // 单独加载口味列表
  try {
    const fRes = await flavorApi.list({ page_size: 500 })
    flavors.value = fRes.data.data || []
  } catch {
    // ignore
  }
})

// 口味过滤：只显示属于已选品牌的口味
const filteredFlavors = computed(() => {
  if (!filterBrand.value) return flavors.value
  return flavors.value.filter(f => f.brand_code === filterBrand.value)
})

// 罐头过滤：按品牌+口味筛选
const filteredCanFoods = computed(() => {
  return canFoods.value.filter(c => {
    if (filterBrand.value && c.brand_code !== filterBrand.value) return false
    if (filterFlavor.value && c.flavor_code !== filterFlavor.value) return false
    return true
  })
})

// 选中的罐头完整数据（保持顺序）
const selectedItems = computed(() => {
  return selectedCodes.value
    .map(code => canFoods.value.find(c => c.code === code))
    .filter(Boolean)
})

// 工具函数
function pct(v) {
  if (v == null) return '-'
  return (v * 100).toFixed(2) + '%'
}

function passClass(v) {
  if (v === '合格') return 'pass-ok'
  if (v === '不合格') return 'pass-fail'
  return ''
}

function highlight(v, threshold) {
  if (v == null) return ''
  return v >= threshold ? 'highlight-val' : ''
}
</script>

<style scoped>
.page-container { padding: 20px; }
.page-title { font-size: 20px; font-weight: 600; margin-bottom: 16px; }

.filter-card { margin-bottom: 20px; }

.compare-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
  align-items: start;
}

.compare-card {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.card-header {
  background: linear-gradient(135deg, #4a90d9 0%, #67c23a 100%);
  color: #fff;
  padding: 16px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
}

.brand-name { margin-right: 8px; }

.flavor-name {
  font-size: 13px;
  opacity: 0.85;
}

.card-desc {
  font-size: 12px;
  opacity: 0.85;
  line-height: 1.5;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 10px;
}

.card-photo {
  width: 100%;
  height: 120px;
  border-radius: 6px;
  object-fit: cover;
  margin-top: 6px;
}

.section { padding: 0 16px 8px; }

.section-title {
  font-size: 13px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 8px;
  border-left: 3px solid #409eff;
  padding-left: 8px;
}

.metric-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.metric-table tr:nth-child(even) { background: #f5f7fa; }
.metric-table td:first-child { color: #606266; width: 50%; padding: 4px 6px; }
.metric-table td:last-child { color: #303133; font-weight: 500; padding: 4px 6px; text-align: right; }

.highlight-val { color: #409eff; font-weight: 700; }

.pass-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.pass-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 4px;
  border-radius: 6px;
  font-size: 12px;
  background: #f5f7fa;
}

.pass-item span:first-child { color: #909399; margin-bottom: 2px; }
.pass-item span:last-child { font-weight: 600; }

.pass-ok { background: #f0f9eb; }
.pass-ok span:first-child { color: #67c23a; }
.pass-ok span:last-child { color: #67c23a; }

.pass-fail { background: #fef0f0; }
.pass-fail span:first-child { color: #f56c6c; }
.pass-fail span:last-child { color: #f56c6c; }
</style>
