<template>
  <div>

    <h3>阵型微调</h3>

    <svg
      width="400"
      height="250"
      style="border:1px solid #ccc"
    >

      <circle
        v-for="player in players"
        :key="player.id"
        :cx="player.x"
        :cy="player.y"
        r="10"
        fill="blue"
        @mousedown="startDrag(player)"
      />

    </svg>

  </div>
</template>

<script setup>
import { ref } from "vue"

const emit = defineEmits([
  "update-position"
])

const players = ref([
  { id:1,x:50,y:120 },
  { id:2,x:120,y:60 },
  { id:3,x:120,y:180 },
  { id:4,x:200,y:120 }
])

let current = null

function startDrag(player){

  current = player

  window.onmousemove = move

  window.onmouseup = stop
}

function move(e){

  if(!current) return

  current.x += e.movementX
  current.y += e.movementY

  emit(
    "update-position",
    players.value
  )
}

function stop(){

  current = null

  window.onmousemove = null
  window.onmouseup = null
}
</script>