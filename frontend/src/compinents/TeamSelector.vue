<template>
  <div class="team-selector">

    <div class="team-card">

      <h3>主队</h3>

      <select v-model="homeId">

        <option
          v-for="team in teams"
          :key="team.id"
          :value="team.id"
        >
          {{ team.flag }} {{ team.name }}
        </option>

      </select>

    </div>

    <div class="vs">
      VS
    </div>

    <div class="team-card">

      <h3>客队</h3>

      <select v-model="awayId">

        <option
          v-for="team in teams"
          :key="team.id"
          :value="team.id"
        >
          {{ team.flag }} {{ team.name }}
        </option>

      </select>

    </div>

  </div>
</template>