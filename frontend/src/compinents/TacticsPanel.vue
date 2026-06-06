<template>

  <div>

    <h3>主队战术</h3>

    <div
      v-for="tag in homeTeam.tactical_tags"
      :key="tag"
    >
      <label>

        <input
          type="checkbox"
          :value="tag"
          v-model="homeTactics"
        />

        {{ tag }}

      </label>
    </div>

  </div>

</template>