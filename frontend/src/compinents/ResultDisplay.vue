<template>

  <div>

    <div
      ref="captureArea"
      v-if="result"
    >

      <div
        id="scoreChart"
        style="height:300px"
      ></div>

      <h3>控球率</h3>

      <p>
        主队 {{ result.possession.home }}%
        -
        客队 {{ result.possession.away }}%
      </p>

      <h3>战术分析</h3>
      <p>{{ result.tactical_analysis }}</p>

      <h3>核心球员预测</h3>
      <pre>{{ result.key_players }}</pre>

      <h3>战术建议</h3>
      <p>{{ result.tactical_advice }}</p>

      <h3>智能体博弈记录</h3>

      <pre>
{{ JSON.stringify(result.history,null,2) }}
      </pre>

    </div>

    <button
      v-if="result"
      @click="share"
    >
      分享截图
    </button>

  </div>

</template>

<script setup>
import * as echarts from "echarts"
import html2canvas from "html2canvas"

import {
  ref,
  watch,
  nextTick
} from "vue"

const props = defineProps([
  "result"
])

const captureArea = ref()

watch(
  () => props.result,
  async (val) => {

    if(!val) return

    await nextTick()

    const chart = echarts.init(
      document.getElementById("scoreChart")
    )

    chart.setOption({
      xAxis:{
        type:"category",
        data: val.score_probabilities.map(
          i => i.score
        )
      },
      yAxis:{
        type:"value"
      },
      series:[
        {
          type:"bar",
          data: val.score_probabilities.map(
            i => i.prob
          )
        }
      ]
    })
  }
)

async function share(){

  const canvas = await html2canvas(
    captureArea.value
  )

  const link = document.createElement("a")

  link.download = "tactician-result.png"

  link.href = canvas.toDataURL()

  link.click()
}
</script>