<template>
  <div>
    <iframe
      v-if="url"
      :src="url"
      class="html-output-frame"
      sandbox
      title="HTML output"
    />
    <div v-else class="text-muted">HTML output is not available.</div>
  </div>
</template>

<script>
export default {
  name: "html-iframe-output-display",
  props: {
    viewData: {
      type: Object,
      required: true,
    },
  },
  computed: {
    url() {
      return this.viewData && this.viewData.url ? this.viewData.url : null;
    },
  },
};
</script>

<style scoped>
.html-output-frame {
  display: block;
  width: 100%;
  min-height: 640px;
  border: 1px solid var(--gray);
  border-radius: 3px;
}
</style>
