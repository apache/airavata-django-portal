<template>
  <div>
    <b-form-group>
      <b-form-checkbox-group
        v-model="selected"
        :options="options"
        name="flavour-2a"
        stacked
      ></b-form-checkbox-group>
    </b-form-group>

  </div>
</template>

<script>

export default {
  name: "parser-selector",
  data() {
    return {
      selected: [], // Must be an array reference!
      options: [
        { text: 'Gamess RNA Parser', value: 'orange' },
        { text: 'Gamess Lig Parser', value: 'apple' },
        { text: 'Gamess Cmplx Parser', value: 'pineapple' }
      ]
    }
  }
}

</script>