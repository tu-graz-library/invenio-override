/*
 * SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
 * SPDX-License-Identifier: MIT
 */

import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";
import TRANSLATE_DE from "./messages/de/translations.json";
import TRANSLATE_EN from "./messages/en/translations.json";

const i18next = i18n.createInstance();
i18next
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: "en",
    returnEmptyString: false,
    debug: process.env.NODE_ENV === "development",
    resources: {
      en: { translation: TRANSLATE_EN },
      de: { translation: TRANSLATE_DE },
    },
    keySeparator: false,
    nsSeparator: false,
    detection: {
      order: ["htmlTag"],
      caches: [],
    },
    react: {
      transKeepBasicHtmlNodesFor: [],
    },
  });

export { i18next };
