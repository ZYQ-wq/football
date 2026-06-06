<template>
  <div class="container">

    <h1>Tactician Pro ⚽</h1>

    <div class="layout">

      <div class="left-panel">

        <TeamSelector
          :teams="teams"
          v-model:homeTeam="form.home_team"
          v-model:awayTeam="form.away_team"
        />

        <TacticsPanel
          :formations="formations"
          v-model:formation="form.formation"
          v-model:tactics="form.tactics"
        />

        <FormationCanvas
          @update-position="updatePosition"
        />

        <div class="player-select">
          <h3>核心球员</h3>

          <input
            v-model="form.key_players.home"
            placeholder="主队核心球员"
          />

          <input
            v-model="form.key_players.away"
            placeholder="客队核心球员"
          />
        </div>

        <button
          class="simulate-btn"
          @click="simulate"
          :disabled="loading"
        >
          {{ loading ? "智能体正在博弈中..." : "开始推演" }}
        </button>

      </div>

      <div class="right-panel">

        <ResultDisplay
          ref="resultRef"
          :result="result"
        />

      </div>

    </div>

    <footer>
      本推演为 AI 模型基于历史数据模拟生成，仅供战术娱乐与学习参考，不代表实际比赛结果。
    </footer>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"

import TeamSelector from "./components/TeamSelector.vue"
import TacticsPanel from "./components/TacticsPanel.vue"
import FormationCanvas from "./components/FormationCanvas.vue"
import ResultDisplay from "./components/ResultDisplay.vue"

const teams = ref([])
const formations = ref([])

const loading = ref(false)
const result = ref(null)

const form = ref({
  home_team: "",
  away_team: "",
  formation: "4-3-3",
  tactics: [],
  key_players: {
    home: "",
    away: ""
  },
  formation_offsets: []
})

onMounted(async () => {

  const teamRes = await axios.get(
    "http://localhost:8000/api/teams"
  )

  const formationRes = await axios.get(
    "http://localhost:8000/api/formations"
  )

  teams.value = teamRes.data
  formations.value = formationRes.data
})

function updatePosition(offsets) {
  form.value.formation_offsets = offsets
}

async function simulate() {

  loading.value = true

  try {

    const res = await axios.post(
      "http://localhost:8000/api/simulate",
      form.value
    )

    result.value = res.data

  } catch (e) {

    alert("推演失败，请检查后端或API额度")

  } finally {

    loading.value = false
  }
}
</script>

<style scoped>
.container{
  padding:20px;
}

.layout{
  display:flex;
  gap:20px;
}

.left-panel{
  width:420px;
}

.right-panel{
  flex:1;
}

.simulate-btn{
  margin-top:20px;
  padding:10px 20px;
}

footer{
  margin-top:20px;
  color:#666;
}
</style>