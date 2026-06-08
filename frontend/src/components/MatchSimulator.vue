<template>
  <div class="page">

    <!-- 顶部导航 -->
    <header class="header">
      <div class="logo">
        ⚽ Tactician Pro
      </div>

      <div class="subtitle">
        AI Football Tactical Simulator
      </div>
    </header>

    <div class="main-layout">

      <!-- 左侧配置区 -->
      <aside class="sidebar">

        <h2>比赛配置</h2>

        <div class="form-group">
          <label>主队</label>
          <select v-model="form.home_team_id">
            <option
              v-for="team in teams"
              :key="team.id"
              :value="team.id"
            >
              {{ team.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>客队</label>
          <select v-model="form.away_team_id">
            <option
              v-for="team in teams"
              :key="team.id"
              :value="team.id"
            >
              {{ team.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>阵型</label>
          <select v-model="form.formation">
            <option
              v-for="item in formations"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>战术指令</label>
          <select v-model="form.tactics">
            <option
              v-for="item in tactics"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>主队核心球员</label>
          <input
            v-model="form.focus_home"
            placeholder="例如 Mbappe"
          />
        </div>

        <div class="form-group">
          <label>客队核心球员</label>
          <input
            v-model="form.focus_away"
            placeholder="例如 Kane"
          />
        </div>

        <button
          class="simulate-btn"
          @click="simulate"
          :disabled="loading"
        >
          {{ loading ? "AI推演中..." : "开始推演" }}
        </button>

      </aside>

      <!-- 右侧结果区 -->
      <section class="content">

        <div class="result-card">

          <h2>比赛推演结果</h2>

          <div v-if="loading" class="loading">
            🤖 智能体正在博弈中...
          </div>

          <div v-else-if="result">

            <!-- 比分预测 -->
            <div class="score-card">

              <div class="team">
                {{ getTeamName(form.home_team_id) }}
              </div>

              <div class="score">
                {{ result.predicted_score || "2 : 1" }}
              </div>

              <div class="team">
                {{ getTeamName(form.away_team_id) }}
              </div>

            </div>

            <!-- 控球率 -->
            <div class="stats-row">

              <div class="stat-box">
                <div class="stat-title">
                  主队控球率
                </div>

                <div class="stat-value">
                  {{ result.possession_home || 54 }}%
                </div>
              </div>

              <div class="stat-box">
                <div class="stat-title">
                  客队控球率
                </div>

                <div class="stat-value">
                  {{ result.possession_away || 46 }}%
                </div>
              </div>

            </div>

            <!-- 图表区域 -->
            <div class="chart-placeholder">

              📊 比分概率分布（ECharts区域）

            </div>

            <!-- 战术分析 -->
            <div class="analysis-card">

              <h3>AI战术分析</h3>

              <p>
                {{ result.analysis }}
              </p>

            </div>

            <!-- 智能体博弈 -->
            <div
              class="analysis-card"
              v-if="result.debate_log"
            >

              <h3>智能体博弈记录</h3>

              <pre>
{{ JSON.stringify(result.debate_log, null, 2) }}
              </pre>

            </div>

          </div>

          <div
            v-else
            class="empty"
          >
            点击左侧按钮开始推演比赛
          </div>

        </div>

      </section>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { api } from "../api"

const teams = ref([])
const formations = ref([])
const tactics = ref([])

const loading = ref(false)

const result = ref(null)

const form = ref({
  home_team_id: "",
  away_team_id: "",
  formation: "",
  tactics: "",
  focus_home: "",
  focus_away: ""
})

const getTeamName = (id) => {
  const team = teams.value.find(
    t => t.id === id
  )

  return team?.name || id
}

const loadData = async () => {
  teams.value = await api.getTeams()
  formations.value = await api.getFormations()
  tactics.value = await api.getTactics()

  if (teams.value.length) {
    form.value.home_team_id = teams.value[0].id
    form.value.away_team_id = teams.value[1].id
  }

  if (formations.value.length) {
    form.value.formation = formations.value[0]
  }

  if (tactics.value.length) {
    form.value.tactics = tactics.value[0]
  }
}

const simulate = async () => {
  loading.value = true

  try {
    result.value = await api.simulate(form.value)
  } catch (err) {
    alert("推演失败")
    console.error(err)
  }

  loading.value = false
}

onMounted(loadData)
</script>

<style scoped>

.page{
  min-height:100vh;
  background:#f3f4f6;
}

.header{
  height:80px;
  background:#0f172a;
  color:white;

  display:flex;
  justify-content:space-between;
  align-items:center;

  padding:0 30px;
}

.logo{
  font-size:30px;
  font-weight:bold;
}

.subtitle{
  opacity:.8;
}

.main-layout{
  display:flex;
  gap:20px;
  padding:20px;
}

.sidebar{
  width:340px;

  background:white;
  border-radius:12px;

  padding:20px;

  box-shadow:
    0 4px 12px rgba(0,0,0,.08);
}

.sidebar h2{
  margin-bottom:20px;
}

.form-group{
  margin-bottom:16px;
}

.form-group label{
  display:block;
  margin-bottom:6px;
  font-weight:600;
}

.form-group input,
.form-group select{
  width:100%;
  padding:10px;

  border:1px solid #ddd;
  border-radius:8px;
}

.simulate-btn{
  width:100%;
  padding:12px;

  background:#16a34a;
  color:white;

  border:none;
  border-radius:8px;

  cursor:pointer;
  font-size:16px;
  font-weight:bold;
}

.content{
  flex:1;
}

.result-card{
  background:white;

  border-radius:12px;
  padding:20px;

  min-height:700px;

  box-shadow:
    0 4px 12px rgba(0,0,0,.08);
}

.score-card{
  display:flex;
  justify-content:space-around;
  align-items:center;

  background:#f8fafc;

  padding:25px;
  border-radius:10px;

  margin-top:20px;
}

.team{
  font-size:22px;
  font-weight:bold;
}

.score{
  font-size:42px;
  font-weight:bold;
  color:#16a34a;
}

.stats-row{
  display:flex;
  gap:20px;
  margin-top:20px;
}

.stat-box{
  flex:1;
  text-align:center;

  background:#f8fafc;

  border-radius:10px;
  padding:20px;
}

.stat-title{
  margin-bottom:10px;
}

.stat-value{
  font-size:30px;
  font-weight:bold;
}

.chart-placeholder{
  margin-top:20px;

  height:280px;

  border:2px dashed #ccc;

  display:flex;
  align-items:center;
  justify-content:center;

  border-radius:10px;
}

.analysis-card{
  margin-top:20px;

  background:#f8fafc;

  border-radius:10px;
  padding:20px;
}

.loading{
  margin-top:30px;
  text-align:center;
  font-size:20px;
}

.empty{
  margin-top:100px;
  text-align:center;
  color:#888;
}
</style>