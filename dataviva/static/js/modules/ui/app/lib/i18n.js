import Vue from "vue";
import VueI18n from "vue-i18n";
import pt from "../lang/pt.json";
import en from "../lang/en.json";

Vue.use(VueI18n);

const locale = "en";

const messages = {
  pt: {
    message: pt.message,
  },
  en: {
    message: en.message,
  },
};

const dateTimeFormats = {
  pt: pt.dateTimeFormat,
  en: en.dateTimeFormat,
};

const numberFormats = {
  pt: pt.numberFormat,
  en: en.numberFormat,
};

const i18n = new VueI18n({
  locale,
  messages,
  dateTimeFormats,
  numberFormats,
});

export default i18n;
