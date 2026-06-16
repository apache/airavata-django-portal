import { shallowMount } from "@vue/test-utils";
import HtmlIframeOutputDisplay from "@/components/experiment/output-displays/HtmlIframeOutputDisplay.vue";

describe("HtmlIframeOutputDisplay", () => {
  test("renders sandboxed iframe for HTML output URL", () => {
    const wrapper = shallowMount(HtmlIframeOutputDisplay, {
      propsData: {
        viewData: {
          url: "http://testserver/sdk/download/?data-product-uri=abc&mime-type=text%2Fhtml",
        },
      },
    });

    const iframe = wrapper.find("iframe");
    expect(iframe.exists()).toBe(true);
    expect(iframe.attributes("src")).toBe(
      "http://testserver/sdk/download/?data-product-uri=abc&mime-type=text%2Fhtml"
    );
    expect(iframe.attributes("sandbox")).toBe("");
  });

  test("renders unavailable message when no URL is provided", () => {
    const wrapper = shallowMount(HtmlIframeOutputDisplay, {
      propsData: {
        viewData: {},
      },
    });

    expect(wrapper.find("iframe").exists()).toBe(false);
    expect(wrapper.text()).toContain("HTML output is not available.");
  });
});
