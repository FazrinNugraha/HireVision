import streamlit as st
from utils import get_groq_client, chat_with_career_bot

def render():
    st.header("Konsultan Karir Virtual 🤖")
    st.write("Tanyakan masalah wawancara Anda, bedah CV Anda, atau tips nego gaji ke ahlinya!")

    client = get_groq_client()

    if client is None:
        st.warning("⚠️ Anda Belum Memasukkan `GROQ_API_KEY` di `.streamlit/secrets.toml`. Chatbot di-nonaktifkan sementara.")
    else:
        # ── BANNER KONTEKS: Tampilkan jika user sudah melakukan prediksi ──
        prediksi_ctx = st.session_state.get("last_prediction")
        if prediksi_ctx:
            st.info(
                f"📌 **Konteks Aktif dari Prediksi Anda:**  \n"
                f"Kategori: **{prediksi_ctx['kategori']}** | Lokasi: **{prediksi_ctx['lokasi']}**  \n"
                f"Profil: {prediksi_ctx.get('level','–')} | {prediksi_ctx.get('kontrak','–')} | {prediksi_ctx.get('skala','–')}  \n"
                f"Estimasi Gaji: **Rp {prediksi_ctx['gaji_prediksi']:,}** "
                f"(Rentang: Rp {prediksi_ctx['gaji_min']:,} – Rp {prediksi_ctx['gaji_max']:,}) | "
                f"Multiplier: `×{prediksi_ctx.get('multiplier', '–')}`  \n"
                f"_AI sudah mengetahui profil ini. Silakan langsung tanya!_"
            )
        else:
            st.caption("💡 **Tips:** Jalankan Prediksi Gaji di Tab 1 terlebih dahulu agar AI bisa memberi saran yang lebih personal.")

        # ── BUILD SYSTEM PROMPT DINAMIS BERDASARKAN KONTEKS ──
        if prediksi_ctx:
            konteks_str = (
                f"Pengguna baru saja menggunakan fitur prediksi gaji dan mendapatkan hasil berikut: "
                f"Kategori pekerjaan: '{prediksi_ctx['kategori']}', lokasi: '{prediksi_ctx['lokasi']}', "
                f"estimasi gaji pasar: Rp {prediksi_ctx['gaji_prediksi']:,} per bulan "
                f"(rentang negosiasi wajar Rp {prediksi_ctx['gaji_min']:,} hingga Rp {prediksi_ctx['gaji_max']:,}). "
                f"Gunakan informasi ini sebagai konteks utama untuk semua jawaban Anda."
            )
        else:
            konteks_str = "Belum ada data prediksi gaji dari pengguna ini."

        system_prompt_dinamis = (
            "Anda adalah asisten konsultan karir profesional dan ramah yang khusus "
            "membantu pencari kerja di wilayah Jabodetabek (Indonesia). Tugas Anda menjawab pertanyaan "
            "seputar negosiasi gaji, tren industri, persiapan wawancara, dan skill set. "
            "Jawab dengan bahasa Indonesia yang santai tapi profesional. "
            "Jawaban harus ringkas, tepat sasaran (maksimal 3 paragraf), dan berikan 1-3 bullet points jika perlu. "
            f"\n\nKONTEKS PENGGUNA SAAT INI: {konteks_str}"
        )

        # ── INISIALISASI HISTORY CHAT ──
        if "messages" not in st.session_state:
            salam_awal = (
                f"Halo! Saya Konsultan Karir Virtual Anda. "
                + (f"Saya sudah melihat hasil prediksi Anda untuk posisi **{prediksi_ctx['kategori']}** di **{prediksi_ctx['lokasi']}** "
                   f"dengan estimasi gaji **Rp {prediksi_ctx['gaji_prediksi']:,}**. Ada pertanyaan seputar ini atau topik karir lainnya?"
                   if prediksi_ctx else
                   "Ada yang bisa saya bantu terkait karir Anda di Jabodetabek hari ini?")
            )
            st.session_state["messages"] = [{"role": "assistant", "content": salam_awal}]

        # ── TAMPILKAN HISTORY CHAT ──
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # ── INPUT USER ──
        user_input = st.chat_input("Tanya seputar karir, gaji, skill, atau persiapan interview...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            with st.chat_message("assistant"):
                placeholder_resp = st.empty()
                full_response = ""

                history_murni = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]

                # Kirim system prompt dinamis ke utils
                stream = chat_with_career_bot(client, user_input, history_murni, system_prompt_dinamis)

                if stream:
                    for chunk in stream:
                        delta = chunk.choices[0].delta.content
                        if delta:
                            full_response += delta
                            placeholder_resp.markdown(full_response + "▌")
                    placeholder_resp.markdown(full_response)

            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
