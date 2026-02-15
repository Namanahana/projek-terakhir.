import random
import discord

QUIZ_AB = {
    "school": [
        {
            "q": "PR numpuk biasanya kamu…",
            "A": "Cicil dari jauh hari",
            "B": "Panik H-1",
            "resultA": "🧠 Kamu tipe strategis. Guru bangga.",
            "resultB": "🔥 Kamu hidup di bawah tekanan — dan survive."
        },
        {
            "q": "Belajar ujian kamu…",
            "A": "Rutin tiap hari",
            "B": "SKS semalam",
            "resultA": "📚 Disiplin level dewa.",
            "resultB": "⚡ Master kebut semalam."
        },
        {
            "q": "Guru tanya mendadak kamu…",
            "A": "Jawab percaya diri",
            "B": "Pura-pura baca buku",
            "resultA": "😎 Aura anak pintar.",
            "resultB": "🫥 Ninja menghilang."
        },
        {
            "q": "Kerja kelompok kamu…",
            "A": "Leader tim",
            "B": "Anggota pasif",
            "resultA": "👑 Jiwa pemimpin.",
            "resultB": "🛌 Mode hemat energi."
        }
    ],
    "life": [
        {
            "q": "Kalau capek kamu…",
            "A": "Tidur",
            "B": "Scroll HP 3 jam",
            "resultA": "😌 Kamu tahu cara recharge diri.",
            "resultB": "📱 Kamu korban algoritma."
        },
        {
            "q": "Jam 2 pagi kamu…",
            "A": "Tidur nyenyak",
            "B": "Overthinking",
            "resultA": "😴 Damai dunia.",
            "resultB": "🧠 Pikiran tidak shutdown."
        },
        {
            "q": "Chat belum dibalas kamu…",
            "A": "Santai aja",
            "B": "Langsung mikir aneh",
            "resultA": "🧘 Emotional stable.",
            "resultB": "🎢 Roller coaster emosi."
        },
        {
            "q": "Hari libur kamu…",
            "A": "Istirahat total",
            "B": "Scroll tanpa henti",
            "resultA": "🌿 Recharge sukses.",
            "resultB": "📱 Budak layar."
        }
    ],
    "gaming": [
    {
        "q": "Kalah rank kamu…",
        "A": "Stop main",
        "B": "Rematch terus",
        "resultA": "🧘 Mental stabil.",
        "resultB": "⚔️ Pejuang sejati."
    },
    {
        "q": "Ping naik kamu…",
        "A": "Sabar",
        "B": "Nyalahin wifi",
        "resultA": "😌 Zen gamer.",
        "resultB": "📡 Korban jaringan."
    },
    {
        "q": "Temen noob kamu…",
        "A": "Ajarin pelan",
        "B": "Ngamuk di voice",
        "resultA": "🤝 Supportive player.",
        "resultB": "🔥 Toxic tapi jujur."
    }
    ],
    "work": [
    {
        "q": "Deadline besok kamu…",
        "A": "Sudah selesai",
        "B": "Baru buka file",
        "resultA": "📅 Organisasi rapi.",
        "resultB": "💀 Hidup di edge."
    },
    {
        "q": "Meeting panjang kamu…",
        "A": "Fokus dengerin",
        "B": "Mikir makan siang",
        "resultA": "🎯 Profesional.",
        "resultB": "🍜 Prioritas jelas."
    },
    {
        "q": "Kerja lembur kamu…",
        "A": "Terima nasib",
        "B": "Mengeluh tiap menit",
        "resultA": "🧱 Tahan banting.",
        "resultB": "🎭 Drama worker."
    }
    ]


}


def detect_theme(prompt: str):
    p = prompt.lower()

    school_keywords = [
    "pr", "ujian", "sekolah", "guru", "kelas", "belajar",
    "school", "teacher", "exam", "student"
]
    gaming_keywords = [
    "game", "rank", "ml", "valorant", "pubg", "gamer",
    "gaming", "player"
]
    work_keywords = [
    "kerja", "kantor", "deadline", "meeting", "lembur",
    "work", "office", "worker", "job", "boss"
]
    life_keywords = [
    "stress", "capek", "tidur", "overthinking", "hidup",
    "tired", "sad", "sleep", "life"
]

    def match(words):
        return any(w in p for w in words)

    if match(school_keywords):
        return "school"
    if match(gaming_keywords):
        return "gaming"
    if match(work_keywords):
        return "work"
    if match(life_keywords):
        return "life"

    return "life"  # default fallback

class QuizView(discord.ui.View):
    def __init__(self, quiz):
        super().__init__(timeout=20)
        self.quiz = quiz

    @discord.ui.button(label="A", style=discord.ButtonStyle.primary)
    async def option_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"💡 Kamu tipe orang yang:\n{self.quiz['resultA']}"
        )
        self.stop()


    @discord.ui.button(label="B", style=discord.ButtonStyle.danger)
    async def option_b(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"💡 Kamu tipe orang yang:\n{self.quiz['resultB']}"
        )
        self.stop()

