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
      <div class="table-scroll">
        <el-table :data="pagedData" stripe v-loading="loading">
          <!-- 固定列 -->
          <el-table-column prop="code" label="ID" width="70" fixed />
          <el-table-column prop="brand.name" label="品牌" width="100" fixed />
          <el-table-column prop="flavor.name" label="口味" width="100" fixed />
          <el-table-column prop="description" label="简介" width="120" show-overflow-tooltip fixed />
          <!-- 营养成分（湿基）-->
          <el-table-column label="总热量" width="90" sortable>
            <template #default="{ row }">{{ row.total_energy_kcal ? Math.round(row.total_energy_kcal)+'kcal/kg' : '-' }}</template>
          </el-table-column>
          <el-table-column label="蛋白%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.protein != null ? (row.protein*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="脂肪%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.fat != null ? (row.fat*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="粗灰分%·湿" width="85" sortable align="center">
            <template #default="{ row }">{{ row.ash != null ? (row.ash*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="粗纤维%·湿" width="85" sortable align="center">
            <template #default="{ row }">{{ row.fiber != null ? (row.fiber*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="水分%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.moisture != null ? (row.moisture*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="钙%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.calcium_wet != null ? (row.calcium_wet*100).toFixed(3)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="磷%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.phosphorus_wet != null ? (row.phosphorus_wet*100).toFixed(3)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="NFE%·湿" width="80" sortable align="center">
            <template #default="{ row }">{{ row.nfe_wet != null ? (row.nfe_wet*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <!-- 干物质 -->
          <el-table-column label="蛋白%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.protein_dm != null ? (row.protein_dm*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="脂肪%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.fat_dm != null ? (row.fat_dm*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="灰分%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.ash_dm != null ? (row.ash_dm*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="NFE%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.nfe_dm != null ? (row.nfe_dm*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="钙%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.calcium_dm != null ? (row.calcium_dm*100).toFixed(3)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="磷%·干" width="80" sortable align="center">
            <template #default="{ row }">{{ row.phosphorus_dm != null ? (row.phosphorus_dm*100).toFixed(3)+'%' : '-' }}</template>
          </el-table-column>
          <!-- 钙磷比 -->
          <el-table-column label="钙磷比" width="80" sortable align="center">
            <template #default="{ row }">{{ row.ca_ph_ratio != null ? row.ca_ph_ratio.toFixed(2) : '-' }}</template>
          </el-table-column>
          <el-table-column prop="ca_ph_pass" label="钙磷合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.ca_ph_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.ca_ph_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <!-- 每1000kcal -->
          <el-table-column label="钙mg/1000kal" width="110" sortable align="center">
            <template #default="{ row }">{{ row.calcium_per_1000kal != null ? row.calcium_per_1000kal.toFixed(0) : '-' }}</template>
          </el-table-column>
          <el-table-column label="磷mg/1000kal" width="110" sortable align="center">
            <template #default="{ row }">{{ row.phosphorus_per_1000kal != null ? row.phosphorus_per_1000kal.toFixed(0) : '-' }}</template>
          </el-table-column>
          <el-table-column prop="phosphorus_level" label="磷水平" width="80" align="center">
            <template #default="{ row }">{{ row.phosphorus_level || '-' }}</template>
          </el-table-column>
          <!-- 代谢能 -->
          <el-table-column label="蛋白代谢能%" width="105" sortable align="center">
            <template #default="{ row }">{{ row.protein_met_energy_pct != null ? (row.protein_met_energy_pct*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="脂肪代谢能%" width="105" sortable align="center">
            <template #default="{ row }">{{ row.fat_met_energy_pct != null ? (row.fat_met_energy_pct*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="碳水代谢能%" width="105" sortable align="center">
            <template #default="{ row }">{{ row.carb_met_energy_pct != null ? (row.carb_met_energy_pct*100).toFixed(1)+'%' : '-' }}</template>
          </el-table-column>
          <el-table-column label="蛋白kcal" width="85" sortable align="center">
            <template #default="{ row }">{{ row.protein_kcal != null ? Math.round(row.protein_kcal) : '-' }}</template>
          </el-table-column>
          <el-table-column label="脂肪kcal" width="85" sortable align="center">
            <template #default="{ row }">{{ row.fat_kcal != null ? Math.round(row.fat_kcal) : '-' }}</template>
          </el-table-column>
          <el-table-column label="碳水kcal" width="85" sortable align="center">
            <template #default="{ row }">{{ row.carb_kcal != null ? Math.round(row.carb_kcal) : '-' }}</template>
          </el-table-column>
          <!-- 蛋白:脂肪比 -->
          <el-table-column label="蛋白:脂肪" width="85" sortable align="center">
            <template #default="{ row }">{{ row.protein_fat_ratio != null ? row.protein_fat_ratio.toFixed(2) : '-' }}</template>
          </el-table-column>
          <el-table-column prop="protein_level" label="蛋白水平" width="80" align="center">
            <template #default="{ row }">{{ row.protein_level || '-' }}</template>
          </el-table-column>
          <!-- 合格指标 -->
          <el-table-column prop="protein_pass" label="蛋白合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.protein_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.protein_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="fat_pass" label="脂肪合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.fat_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.fat_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="fiber_pass" label="纤维合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.fiber_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.fiber_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="ash_pass" label="灰分合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.ash_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.ash_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="moisture_pass" label="水分合格" width="85" align="center">
            <template #default="{ row }">
              <el-tag :type="row.moisture_pass === '合格' ? 'success' : 'danger'" size="small">{{ row.moisture_pass || '-' }}</el-tag>
            </template>
          </el-table-column>
          <!-- 创建信息 -->
          <el-table-column prop="creator" label="创建人" width="80" />
          <el-table-column prop="created_date" label="创建日期" width="160" />
          <!-- 操作（固定右侧）-->
          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="showDialog('edit', row)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
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
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="1100px" @closed="resetForm">
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

        <el-divider content-position="left">营养成分（湿基）- 可编辑</el-divider>
        <el-row :gutter="12">
          <el-col :span="6"><el-form-item label="蛋白质"><el-input-number v-model="form.protein" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="脂肪"><el-input-number v-model="form.fat" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="粗灰分"><el-input-number v-model="form.ash" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="粗纤维"><el-input-number v-model="form.fiber" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="水分"><el-input-number v-model="form.moisture" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="钙-湿基"><el-input-number v-model="form.calcium_wet" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="磷-湿基"><el-input-number v-model="form.phosphorus_wet" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="NFE-湿基"><el-input-number v-model="form.nfe_wet" :min="0" :precision="4" style="width:100%" /></el-form-item></el-col>
          <el-col :span="6"><el-form-item label="标注kcal"><el-input-number v-model="form.labeled_kcal" :min="0" :precision="2" style="width:100%" /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">罐头图片</el-divider>
        <el-form-item label="">
          <div style="display:flex;align-items:center;gap:12px">
            <el-image v-if="form.photo" :src="form.photo" fit="cover" style="width:80px;height:80px;border-radius:8px;border:1px solid #dcdfe6" :preview-src-list="[form.photo]" />
            <div v-else style="width:80px;height:80px;border:1px dashed #dcdfe6;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#909399;font-size:12px;cursor:pointer" @click="photoInput.click()">点击上传</div>
            <div v-if="form.photo"><el-button size="small" type="danger" @click="form.photo=''">移除</el-button></div>
          </div>
          <input ref="photoInput" type="file" accept="image/*" style="display:none" @change="e=>handlePhotoUpload(e,'photo')" />
        </el-form-item>

        <el-divider content-position="left">自动计算值</el-divider>
        <el-row :gutter="12">
          <el-col :span="6"><el-form-item >          <template #label>
            钙磷比
            <el-tooltip content="钙(湿基) / 磷(湿基)" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.ca_ph_ratio != null ? form.ca_ph_ratio.toFixed(4) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白-干基
            <el-tooltip content="蛋白(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_dm != null ? (form.protein_dm*100).toFixed(2)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            脂肪-干基
            <el-tooltip content="脂肪(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.fat_dm != null ? (form.fat_dm*100).toFixed(2)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            灰分-干基
            <el-tooltip content="灰分(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.ash_dm != null ? (form.ash_dm*100).toFixed(2)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            NFE-干基
            <el-tooltip content="NFE(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.nfe_dm != null ? (form.nfe_dm*100).toFixed(2)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            钙-干基
            <el-tooltip content="钙(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.calcium_dm != null ? (form.calcium_dm*100).toFixed(3)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            磷-干基
            <el-tooltip content="磷(湿基) / 干物质" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.phosphorus_dm != null ? (form.phosphorus_dm*100).toFixed(3)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            钙mg/1000kal
            <el-tooltip content="钙(湿基)×1000×10 / 总热量" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.calcium_per_1000kal != null ? form.calcium_per_1000kal.toFixed(1) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            磷mg/1000kal
            <el-tooltip content="磷(湿基)×1000×10 / 总热量" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.phosphorus_per_1000kal != null ? form.phosphorus_per_1000kal.toFixed(1) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            磷水平
            <el-tooltip content="磷mg/1000kal &gt;2400 高磷, &lt;1800 低磷" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.phosphorus_level || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            1kg总热量
            <el-tooltip content="蛋白kcal+脂肪kcal+碳水kcal" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.total_energy_kcal != null ? Math.round(form.total_energy_kcal)+'kcal/kg' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            标注kcal
            <el-tooltip content="人工输入的标注热量值" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.labeled_kcal != null ? form.labeled_kcal : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白kcal
            <el-tooltip content="蛋白×3.5×100×10" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_kcal != null ? Math.round(form.protein_kcal) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            脂肪kcal
            <el-tooltip content="脂肪×8.5×100×10" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.fat_kcal != null ? Math.round(form.fat_kcal) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            碳水kcal
            <el-tooltip content="NFE×3.5×100×10" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.carb_kcal != null ? Math.round(form.carb_kcal) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白代谢能%
            <el-tooltip content="蛋白kcal / 总热量" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_met_energy_pct != null ? (form.protein_met_energy_pct*100).toFixed(1)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            脂肪代谢能%
            <el-tooltip content="脂肪kcal / 总热量" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.fat_met_energy_pct != null ? (form.fat_met_energy_pct*100).toFixed(1)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            碳水代谢能%
            <el-tooltip content="碳水kcal / 总热量" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.carb_met_energy_pct != null ? (form.carb_met_energy_pct*100).toFixed(1)+'%' : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白:脂肪
            <el-tooltip content="蛋白(湿基) / 脂肪(湿基)" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_fat_ratio != null ? form.protein_fat_ratio.toFixed(2) : '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白水平
            <el-tooltip content="比值&gt;3.0优秀, &gt;1.5一般, ≤1.5不合格" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_level || '-'" disabled /></el-form-item></el-col>
        </el-row>

        <el-divider content-position="left">合格指标</el-divider>
        <el-row :gutter="12">
          <el-col :span="6"><el-form-item >          <template #label>
            蛋白合格
            <el-tooltip content="依据标准规则自动判定" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.protein_pass || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            脂肪合格
            <el-tooltip content="依据标准规则自动判定" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.fat_pass || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            纤维合格
            <el-tooltip content="依据标准规则自动判定" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.fiber_pass || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            灰分合格
            <el-tooltip content="依据标准规则自动判定" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.ash_pass || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            水分合格
            <el-tooltip content="依据标准规则自动判定" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.moisture_pass || '-'" disabled /></el-form-item></el-col>
          <el-col :span="6"><el-form-item >          <template #label>
            钙磷合格
            <el-tooltip content="钙磷比在 1.1~1.4 之间为合格" placement="top">
              <el-icon style="margin-left:4px;cursor:pointer;color:#909399"><QuestionFilled /></el-icon>
            </el-tooltip>
          </template>
            <el-input :model-value="form.ca_ph_pass || '-'" disabled /></el-form-item></el-col>
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
import { QuestionFilled } from '@element-plus/icons-vue'
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
    photo: '',
    labeled_kcal: null,
  }
}

const dialogTitle = computed(() => dialogType.value === 'create' ? '新增罐头' : '编辑罐头')

const filterFlavors = computed(() => {
  if (!filterForm.value.brand_code) return flavors.value
  return flavors.value.filter(f => f.brand_code === filterForm.value.brand_code)
})

const onBrandFilterChange = () => { filterForm.value.flavor_code = '' }

const onBrandChange = () => {
  form.value.flavor_code = ''
  dialogFlavors.value = flavors.value.filter(f => f.brand_code === form.value.brand_code)
}

const photoInput = ref(null)
const handlePhotoUpload = (e) => {
  const file = e.target.files[0]
  if (!file) return
  if (file.size > 5 * 1024 * 1024) { ElMessage.warning('图片不超过5MB'); return }
  const reader = new FileReader()
  reader.onload = (ev) => { form.value.photo = ev.target.result }
  reader.readAsDataURL(file)
}

const filteredData = computed(() => {
  return canFoods.value.filter(c => {
    if (filterForm.value.brand_code && c.brand_code !== filterForm.value.brand_code) return false
    if (filterForm.value.flavor_code && c.flavor_code !== filterForm.value.flavor_code) return false
    if (filterForm.value.keyword && !c.description?.includes(filterForm.value.keyword)) return false
    if (filterForm.value.protein_pass && c.protein_pass !== filterForm.value.protein_pass) return false
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
    if (!error.config?._handled) ElMessage.error('加载罐头失败')
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
    form.value = {
      code: row.code,
      brand_code: row.brand_code ?? '',
      flavor_code: row.flavor_code ?? '',
      description: row.description ?? '',
      creator: row.creator ?? '',
      protein: row.protein ?? null,
      fat: row.fat ?? null,
      ash: row.ash ?? null,
      fiber: row.fiber ?? null,
      moisture: row.moisture ?? null,
      calcium_wet: row.calcium_wet ?? null,
      phosphorus_wet: row.phosphorus_wet ?? null,
      nfe_wet: row.nfe_wet ?? null,
      photo: row.photo ?? '',
      labeled_kcal: row.labeled_kcal ?? null,
    }
  } else {
    form.value = getDefaultForm()
  }
  dialogVisible.value = true
}

const resetForm = () => { form.value = getDefaultForm() }

const handleSubmit = async () => {
  try {
    // 只发送可编辑字段，避免覆盖后端计算值
    const payload = {
      brand_code: form.value.brand_code || null,
      flavor_code: form.value.flavor_code || null,
      description: form.value.description || null,
      creator: form.value.creator || null,
      protein: form.value.protein,
      fat: form.value.fat,
      ash: form.value.ash,
      fiber: form.value.fiber,
      moisture: form.value.moisture,
      calcium_wet: form.value.calcium_wet,
      phosphorus_wet: form.value.phosphorus_wet,
      nfe_wet: form.value.nfe_wet,
      labeled_kcal: form.value.labeled_kcal,
      photo: form.value.photo || null,
    }
    if (dialogType.value === 'create') {
      await canFoodApi.create(payload)
      ElMessage.success('创建成功')
    } else {
      await canFoodApi.update(form.value.code, payload)
      ElMessage.success('更新成功')
    }
    dialogVisible.value = false
    loadCanFoods()
  } catch (error) {
    if (!error.config?._handled) ElMessage.error(error.response?.data?.detail || '操作失败')
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
.table-card { flex: 1; }
.table-scroll { overflow-x: auto; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
