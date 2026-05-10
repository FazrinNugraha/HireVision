"""
Tab AI Consultant - HireVision
================================
Modul ini bertanggung jawab untuk:
1. Menghubungkan user dengan Gemini AI sebagai konsultan karir virtual
2. Menampilkan konteks hasil prediksi gaji dari tab Predict Salary
3. Menyediakan tombol quick-question untuk pertanyaan umum
4. Mengelola riwayat chat dengan streaming response

Struktur fungsi:
- _render_header()                 : Judul tab
- _build_system_prompt(ctx)        : Susun system prompt dinamis dari konteks
- _render_konteks_banner(ctx)      : Banner konteks (jika ada last_prediction)
- _render_no_context_hint()        : Hint jika belum ada prediksi
- _render_quick_questions()        : 6 tombol pertanyaan cepat
- _init_chat_history(ctx)          : Inisialisasi salam pembuka chat
- _stream_ai_response(...)         : Helper streaming response dari Gemini
- _handle_pending_question(...)    : Proses pertanyaan dari tombol cepat
- _render_chat_history()           : Tampilkan riwayat percakapan
- _handle_user_input(...)          : Handle input chat dari user
- render()                         : Entry point (orkestrasi)
"""

import streamlit as st
from utils import get_gemini_client, chat_with_career_bot


# ══════════════════════════════════════════════════════════════
#  KONSTANTA
# ══════════════════════════════════════════════════════════════
QUICK_QUESTIONS = [
    "Tips negosiasi gaji untuk posisi ini",
    "Skillset yang dibutuhkan untuk naik level?",
    "Persiapan interview yang efektif?",
    "Bagaimana prospek karir di posisi ini?",
    "Strategi hunian terbaik untuk gaji ini?",
    "Cara menyusun CV yang baik gimana?",
]

BASE_SYSTEM_PROMPT = (
    "Anda adalah asisten konsultan karir profesional dan perencana keuangan untuk pencari kerja di Jabodetabek. "
    "Tugas Anda menjawab pertanyaan seputar karir, dan SECARA PROAKTIF memberikan 1-2 saran spesifik "
    "mengenai strategi finansial relokasi (tempat tinggal/kos) berdasarkan rasio gaji dan biaya hunian yang ada di konteks."
)


# ══════════════════════════════════════════════════════════════
#  HEADER & BANNER
# ══════════════════════════════════════════════════════════════
def _render_header():
    """Render judul utama + deskripsi tab."""
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


def _get_warna_rasio(rasio_kos: float) -> str:
    """Tentukan warna teks gaji berdasarkan rasio biaya kos."""
    if rasio_kos <= 30:
        return "#2ecc71"   # Hijau — ideal
    if rasio_kos <= 50:
        return "#f1c40f"   # Kuning — warning
    return "#e74c3c"       # Merah — berat


def _render_konteks_banner(ctx: dict):
    """Render banner konteks profil + prediksi gaji dari tab Predict Salary."""
    val_col = _get_warna_rasio(ctx.get("rasio_kos", 100)) if "rasio_kos" in ctx else "#FF6B8A"

    st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(52,152,219,0.08),rgba(41,128,185,0.03));border:1px solid rgba(52,152,219,0.2);border-radius:14px;padding:20px 24px;margin-bottom:24px;">
    <div style="font-size:12px;font-weight:700;color:#5dade2;text-transform:uppercase;letter-spacing:1px;margin-bottom:16px;">📌 Konteks Aktif dari Prediksi Anda</div>
    <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px;">
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">📍 Posisi &amp; Lokasi</div>
            <div style="color:rgba(255,255,255,0.9);font-size:14px;font-weight:600;margin-bottom:2px;">{ctx['judul']}</div>
            <div style="color:rgba(255,255,255,0.5);font-size:12px;">{ctx.get('perusahaan','—')} · di {ctx['lokasi']}</div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">👤 Profil Pekerja</div>
            <div style="color:rgba(255,255,255,0.8);font-size:13px;line-height:1.7;">
                • Pengalaman: {ctx.get('pengalaman','–')}<br>
                • {ctx.get('pendidikan','–')}<br>
                • Sertif: {ctx.get('sertifikasi','–')}
            </div>
        </div>
        <div style="flex:1;min-width:200px;background:rgba(0,0,0,0.2);border:1px solid rgba(255,255,255,0.05);padding:14px;border-radius:10px;">
            <div style="color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px;">💰 Estimasi Gaji</div>
            <div style="color:{val_col};font-weight:700;font-size:1.3rem;margin-bottom:4px;">Rp {ctx['gaji_prediksi']:,}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:11px;">Rentang: Rp {ctx['gaji_min']:,} – Rp {ctx['gaji_max']:,}</div>
        </div>
    </div>
    <div style="border-top:1px solid rgba(52,152,219,0.15);padding-top:12px;font-size:12px;color:rgba(255,255,255,0.38);">
        💡 AI sudah mengetahui profil ini. Silakan langsung tanyakan tips negosiasi atau strategi karir!
    </div>
</div>
""", unsafe_allow_html=True)


def _render_no_context_hint():
    """Render hint jika user belum jalankan prediksi gaji."""
    st.markdown("""
<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:14px 18px;margin-bottom:20px;">
    <span style="color:rgba(255,255,255,0.4);font-size:14px;">
        💡 <strong>Tips:</strong> Jalankan <strong>Predict Salary</strong> di Tab 1 terlebih dahulu agar AI bisa memberi saran yang lebih personal.
    </span>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  SYSTEM PROMPT BUILDER
# ══════════════════════════════════════════════════════════════
def _build_system_prompt(ctx: dict | None) -> str:
    """Susun system prompt dinamis berdasarkan konteks prediksi gaji."""
    if ctx is None:
        konteks_str = "Belum ada data prediksi gaji dari pengguna ini."
    else:
        konteks_str = (
            f"Pengguna baru saja menggunakan fitur prediksi gaji dan mendapatkan hasil berikut: "
            f"Posisi/Jabatan: '{ctx['judul']}', Perusahaan: '{ctx.get('perusahaan','—')}', "
            f"Pengalaman: {ctx.get('pengalaman','')}, Pendidikan: {ctx.get('pendidikan','')}, "
            f"Sertifikasi Profesional: {ctx.get('sertifikasi','')}, "
            f"estimasi gaji pasar (setelah penyesuaian): Rp {ctx['gaji_prediksi']:,} per bulan "
            f"(rentang negosiasi wajar Rp {ctx['gaji_min']:,} hingga Rp {ctx['gaji_max']:,}). "
            f"Gunakan informasi ini sebagai konteks utama untuk semua jawaban Anda. "
        )
        if "estimasi_kos" in ctx:
            konteks_str += (
                f"Selain itu, berdasarkan data prediksi hunian Mamikos, rata-rata harga kos di {ctx['lokasi']} "
                f"adalah Rp {ctx['estimasi_kos']:,} per bulan, yang menghabiskan sekitar {ctx['rasio_kos']:.1f}% "
                f"dari prediksi gaji pengguna."
            )

    return f"{BASE_SYSTEM_PROMPT}\n\nKONTEKS PENGGUNA SAAT INI: {konteks_str}"


# ══════════════════════════════════════════════════════════════
#  QUICK QUESTIONS
# ══════════════════════════════════════════════════════════════
def _render_quick_questions():
    """Render grid 2x3 tombol pertanyaan cepat. Set 'pending_question' di session state jika diklik."""
    st.markdown("""
<div style="font-size:13px;font-weight:600;color:rgba(255,255,255,0.5);margin:16px 0 10px 0;letter-spacing:0.5px;">
    ⚡ PERTANYAAN CEPAT
</div>
""", unsafe_allow_html=True)

    # Layout 2 baris x 3 kolom
    for row_start in (0, 3):
        cols = st.columns(3)
        for i, q in enumerate(QUICK_QUESTIONS[row_start:row_start + 3]):
            key = f"q{row_start + i}"
            with cols[i]:
                if st.button(q, key=key, use_container_width=True):
                    st.session_state["pending_question"] = q
                    st.rerun()

    st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  CHAT LOGIC
# ══════════════════════════════════════════════════════════════
def _init_chat_history(ctx: dict | None):
    """Inisialisasi pesan pembuka dari assistant (hanya sekali per sesi)."""
    if "messages" in st.session_state:
        return

    if ctx:
        salam = (
            f"Halo! Saya Konsultan Karir Virtual Anda. "
            f"Saya sudah melihat hasil prediksi Anda untuk posisi **{ctx['judul']}** di **{ctx['lokasi']}** "
            f"dengan estimasi gaji **Rp {ctx['gaji_prediksi']:,}**. Ada pertanyaan seputar ini atau topik karir lainnya?"
        )
    else:
        salam = "Halo! Saya Konsultan Karir Virtual Anda. Ada yang bisa saya bantu terkait karir Anda di Jabodetabek hari ini?"

    st.session_state["messages"] = [{"role": "assistant", "content": salam}]


def _collect_stream_response(stream) -> str:
    """Kumpulkan semua chunk dari stream Gemini menjadi 1 string."""
    full_response = ""
    if stream is None:
        return full_response

    for chunk in stream:
        try:
            delta = chunk.text
            if delta:
                full_response += delta
        except Exception:
            # Chunk kadang mengandung metadata tanpa .text, skip aja
            pass
    return full_response


def _stream_to_placeholder(stream, placeholder) -> str:
    """Streaming response ke st.empty() placeholder dengan cursor efek."""
    full_response = ""
    if stream is None:
        return full_response

    for chunk in stream:
        try:
            delta = chunk.text
            if delta:
                full_response += delta
                placeholder.markdown(full_response + "▌")
        except Exception:
            pass
    placeholder.markdown(full_response)
    return full_response


def _handle_pending_question(client, system_prompt: str):
    """Proses pertanyaan dari quick-button yang diset via session_state['pending_question']."""
    if "pending_question" not in st.session_state:
        return

    pending_q = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": pending_q})

    # Susun history tanpa pesan terakhir (yang baru saja ditambahkan)
    history_murni = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages[:-1]
    ]
    stream = chat_with_career_bot(client, pending_q, history_murni, system_prompt)
    full_response = _collect_stream_response(stream)

    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.rerun()


def _render_chat_history():
    """Tampilkan riwayat chat lengkap."""
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


def _handle_user_input(client, system_prompt: str):
    """Handle input chat baru dari user (via st.chat_input)."""
    user_input = st.chat_input("Tanya seputar karir, gaji, skill, atau persiapan interview...")
    if not user_input:
        return

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        history_murni = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]
        stream = chat_with_career_bot(client, user_input, history_murni, system_prompt)
        full_response = _stream_to_placeholder(stream, placeholder)

    if full_response:
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════
def render():
    """Entry point tab — orkestrasi semua komponen."""
    _render_header()

    client = get_gemini_client()
    if client is None:
        st.warning(
            "⚠️ Anda Belum Memasukkan `GEMINI_API_KEY` di `.streamlit/secrets.toml`. Chatbot di-nonaktifkan sementara."
        )
        return

    # Ambil konteks prediksi (jika ada)
    ctx = st.session_state.get("last_prediction")

    # ── Banner konteks / hint ──
    if ctx:
        _render_konteks_banner(ctx)
    else:
        _render_no_context_hint()

    # ── Build system prompt + init chat ──
    system_prompt = _build_system_prompt(ctx)

    # ── Quick questions (hanya jika ada konteks) ──
    if ctx:
        _render_quick_questions()

    _init_chat_history(ctx)
    _handle_pending_question(client, system_prompt)
    _render_chat_history()
    _handle_user_input(client, system_prompt)
