import { shallowMount } from "@vue/test-utils";
import { models } from "django-airavata-api";
import ApplicationOutputFieldEditor from "@/components/applications/ApplicationOutputFieldEditor.vue";

function factory(metaData = {}) {
  const output = new models.OutputDataObjectType({
    name: "Report",
    metaData,
  });
  return shallowMount(ApplicationOutputFieldEditor, {
    propsData: {
      value: output,
    },
    stubs: [
      "b-button",
      "b-card",
      "b-form-group",
      "b-form-input",
      "b-form-radio-group",
      "b-form-select",
      "b-link",
      "json-editor",
    ],
  });
}

describe("ApplicationOutputFieldEditor", () => {
  test("setHtml configures HTML metadata and preserves existing providers", () => {
    const wrapper = factory({
      custom: {
        keep: true,
      },
      "output-view-providers": ["existing-provider"],
    });

    wrapper.vm.setHtml();

    expect(wrapper.vm.data.metaData).toEqual({
      custom: {
        keep: true,
      },
      "file-metadata": {
        "mime-type": "text/html",
      },
      "output-view-providers": ["existing-provider", "html-file"],
    });
  });

  test("setHtml does not duplicate html-file provider", () => {
    const wrapper = factory({
      "output-view-providers": ["html-file"],
    });

    wrapper.vm.setHtml();

    expect(wrapper.vm.data.metaData["output-view-providers"]).toEqual([
      "html-file",
    ]);
  });

  test("setPlainText removes html-file provider and preserves other providers", () => {
    const wrapper = factory({
      custom: {
        keep: true,
      },
      "file-metadata": {
        "mime-type": "text/html",
      },
      "output-view-providers": ["existing-provider", "html-file"],
    });

    wrapper.vm.setPlainText();

    expect(wrapper.vm.data.metaData).toEqual({
      custom: {
        keep: true,
      },
      "file-metadata": {
        "mime-type": "text/plain",
      },
      "output-view-providers": ["existing-provider"],
    });
  });

  test("setPlainText removes output-view-providers when html-file is the only provider", () => {
    const wrapper = factory({});

    wrapper.vm.setHtml();
    wrapper.vm.setPlainText();

    expect(wrapper.vm.data.metaData).toEqual({
      "file-metadata": {
        "mime-type": "text/plain",
      },
    });
  });
});
