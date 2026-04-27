import streamlit as st
from utils import get_gemini_client, chat_with_career_bot

def render():
    st.markdown("""
    <div style="margin-bottom:6px;">
        <h2 style="font-size:1.55rem;font-weight:800;color:#fff;margin:0 0 6px 0;">
            Konsultan Karir Virtual 🤖
        </h2>
        <p style="color:rgba(255,255,255,0.45);font-size:0.9rem;margin:0;">
            Tanyakan masalah wawancara, bedah CV, atau tips nego gaji ke ahlinya!
        </p>
    </div>
    <hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:18px 0 24px 0;">
    """, unsafe_allow_html=True)

    client = get_gemini_client()

    if client is None:
        st.warning("⚠️ Anda Belum Memasukkan `GEMINI_API_KEY` di `.streamlit/secrets.toml`. Chatbot di-nonaktifkan sementara.")
    else:
        prediksi_ctx = st.session_state.get("last_prediction")

        # ── BANNER KONTEKS ──
        if prediksi_ctx:
            # Tentukan warna teks gaji berdasarkan rasio kos
            val_col = "#FF6B8A"
            if 'rasio_kos' in prediksi_ctx:
                if prediksi_ctx['rasio_kos'] <= 30:
                    val_col = "#2ecc71" # Hijau
                elif prediksi_ctx['rasio_kos'] <= 50:
                    val_col = "#f1c40f" # Kuning
                else:
                    val_col = "#e74c3c" # Merah

            st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(52,152,219,0.08),rgba(41,128,185,0.03));border:1px solid rgba(52,152,219,0.2);border-radius:14px;padding:20px 24px;margin-bottom:24px;">
    <div style="font-size:12px;font-weight:700;color:#5dade2;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">📌 Konteks Aktif dari Prediksi Anda</div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px;">
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">📍 Posisi &amp; Lokasi</div>
            <div style="color:rgba(255,255,255,0.9);font-size:14px;font-weight:600;margin-bottom:2px;">{prediksi_ctx['kategori']}</div>
            <div style="color:rgba(255,255,255,0.5);font-size:12px;">di {prediksi_ctx['lokasi']}</div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">👤 Profil Pekerja</div>
            <div style="color:rgba(255,255,255,0.8);font-size:13px;line-height:1.7;">
                • {prediksi_ctx.get('level','–')}<br>
                • {prediksi_ctx.get('kontrak','–')}<br>
                • {prediksi_ctx.get('skala','–')}
            </div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">💰 Estimasi Gaji</div>
            <div style="color:{val_col};font-weight:700;font-size:1.3rem;margin-bottom:4px;">Rp {prediksi_ctx['gaji_prediksi']:,}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:11px;">Rentang: Rp {prediksi_ctx['gaji_min']:,} – Rp {prediksi_ctx['gaji_max']:,}</div>
        </div>
    </div>
    <div style="border-top:1px solid rgba(52,152,219,0.15);padding-top:12px;font-size:12px;color:rgba(255,255,255,0.38);">
        💡 AI sudah mengetahui profil ini. Silakan langsung tanyakan tips negosiasi atau strategi karir!
    </div>
</div>
""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 18px;margin-bottom:20px;">
                <span style="color:rgba(255,255,255,0.4);font-size:14px;">
                    💡 <strong>Tips:</strong> Jalankan <strong>Predict Salary</strong> di Tab 1 terlebih dahulu agar AI bisa memberi saran yang lebih personal.
                </span>
            </div>
            """, unsafe_allow_html=True)

        # ── BUILD SYSTEM PROMPT ──
        if prediksi_ctx:
            konteks_str = (
                f"Pengguna baru saja menggunakan fitur prediksi gaji dan mendapatkan hasil berikut: "
                f"Kategori pekerjaan: '{prediksi_ctx['kategori']}', lokasi: '{prediksi_ctx['lokasi']}', "
                f"estimasi gaji pasar: Rp {prediksi_ctx['gaji_prediksi']:,} per bulan "
                f"(rentang negosiasi wajar Rp {prediksi_ctx['gaji_min']:,} hingga Rp {prediksi_ctx['gaji_max']:,}). "
                f"Gunakan informasi ini sebagai konteks utama untuk semua jawaban Anda. "
            )
            if 'estimasi_kos' in prediksi_ctx:
                konteks_str += (
                    f"Selain itu, berdasarkan data prediksi hunian Mamikos, rata-rata harga kos di {prediksi_ctx['lokasi']} "
                    f"adalah Rp {prediksi_ctx['estimasi_kos']:,} per bulan, yang menghabiskan sekitar {prediksi_ctx['rasio_kos']:.1f}% "
                    f"dari prediksi gaji pengguna."
                )
        else:
            konteks_str = "Belum ada data prediksi gaji dari pengguna ini."

        system_prompt_dinamis = (
            "Anda adalah asisten konsultan karir profesional dan perencana keuangan untuk pencari kerja di Jabodetabek. Tugas Anda menjawab pertanyaan "
            "seputar karir, dan SECARA PROAKTIF memberikan 1-2 saran spesifik mengenai strategi finansial relokasi (tempat tinggal/kos) berdasarkan rasio gaji dan biaya hunian yang ada di konteks."
            f"\n\nKONTEKS PENGGUNA SAAT INI: {konteks_str}"
        )

        # ── INISIALISASI CHAT ──
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
                stream = chat_with_career_bot(client, user_input, history_murni, system_prompt_dinamis)

                if stream:
                    for chunk in stream:
                        try:
                            delta = chunk.text
                            if delta:
                                full_response += delta
                                placeholder_resp.markdown(full_response + "▌")
                        except Exception:
                            pass
                    placeholder_resp.markdown(full_response)

            if full_response:
                st.session_state.messages.append({"role": "assistant", "content": full_response})
