import streamlit as st
from utils.i18n import TRANSLATIONS


def init_lang() -> None:
    if "lang" not in st.session_state:
        locale = getattr(st.context, "locale", "en")
        st.session_state.lang = "zh-TW" if str(locale).startswith("zh") else "en"


def set_lang_selector() -> None:
    lang_options = {
        "English": "en",
        "繁體中文": "zh-TW",
    }

    reverse_options = {v: k for k, v in lang_options.items()}
    current_lang = st.session_state.get("lang", "en")
    current_label = reverse_options.get(current_lang, "English")

    selected_label = st.sidebar.selectbox(
        "Language / 語言",
        options=list(lang_options.keys()),
        index=list(lang_options.keys()).index(current_label),
    )

    st.session_state.lang = lang_options[selected_label]


def t(key: str) -> str:
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, {}).get(
        key,
        TRANSLATIONS["en"].get(key, key),
    )