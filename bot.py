import discord
from discord.ext import commands
import os

from config import TOKEN, PREFIX
from ai import generate_image
from meme import make_meme
from kuis import detect_theme, QuizView
from database import get_quiz



intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")

@bot.command()
async def meme(ctx, *, args=None):
    try:
        await ctx.send("🧠 Lagi mikir meme...")

        if not args:
            await ctx.send("❌ Format: !meme prompt | teks atas | teks bawah")
            return

        parts = [p.strip() for p in args.split("|")]
        prompt = parts[0]
        top_text = parts[1] if len(parts) > 1 else ""
        bottom_text = parts[2] if len(parts) > 2 else ""

        image_path = generate_image(prompt)
        meme_path = make_meme(image_path, top_text, bottom_text)

        # ✅ kirim meme
        await ctx.send(file=discord.File(meme_path))

        full_text = " ".join(parts)
        theme = detect_theme(full_text)
        quiz = get_quiz(theme)


        if quiz:
            view = QuizView(quiz)

        await ctx.send(
            f"🎉 Fun quiz tema **{theme}**:\n{quiz['q']}\n\n"
            f"🅰 {quiz['A']}\n"
            f"🅱 {quiz['B']}",
            view=view
        )

    except Exception as e:
        await ctx.send(f"❌ Error: {e}")


@bot.command()
async def start(ctx):
    help_embed = discord.Embed(
        title="🤖 MemeAI Bot",
        description="Bot pembuat meme AI + quiz interaktif untuk menemani hari hari absurd kamu.",
        color=discord.Color.blue()
    )

    help_embed.add_field(
        name="📝 Commands",
        value=(
            "`!start` → Tampilkan menu ini\n"
            "`!info` → Info bot dan fitur\n"
            "`!meme <prompt> | <teks atas> | <teks bawah>` → Generate meme\n"
            "`!meme_random` → Meme random + quiz"
        ),
        inline=False
    )

    help_embed.add_field(
        name="🎯 Contoh Penggunaan",
        value=(
            "`!meme zombie office worker | niat produktif | lembur tanpa hasil`\n\n"
            "Bot akan:\n"
            "• Generate gambar AI\n"
            "• Tambahkan teks meme\n"
            "• Kasih quiz sesuai tema"
        ),
        inline=False
    )

    help_embed.add_field(
        name="🧠 Tips",
        value=(
            "Gunakan kata seperti:\n"
            "`sekolah`, `guru`, `kerja`, `lembur`, `game`, `capek`\n"
            "agar quiz sesuai tema."
        ),
        inline=False
    )

    help_embed.set_footer(text="Prefix bot: !")

    await ctx.send(embed=help_embed)



# ---TUGAS FUNGSI TAMBAHAN--- #

import random

RANDOM_MEMES = [
    {
        "prompt": "tired programmer late night",
        "top": "NIAT TIDUR CEPET",
        "bottom": "TAU TAU SUBUH"
    },
    {
        "prompt": "confused cat meme",
        "top": "GUA",
        "bottom": "PAS LIAT SOAL"
    },
    {
        "prompt": "office worker staring at screen",
        "top": "KATANYA KERJA TIM",
        "bottom": "YANG KERJA GUA"
    },
    {
        "prompt": "sad anime boy",
        "top": "BILANG GAPAPA",
        "bottom": "PADAHAL CAPEK"
    },
    {
        "prompt": "dog sitting fire meme",
        "top": "INI",
        "bottom": "BAIK BAIK SAJA"
    }
]

@bot.command()
async def meme_random(ctx):
    try:
        await ctx.send("🎲 Lagi nyari meme random...")

        data = random.choice(RANDOM_MEMES)

        image_path = generate_image(data["prompt"])
        meme_path = make_meme(
            image_path,
            data["top"],
            data["bottom"]
        )

        await ctx.send(file=discord.File(meme_path))

        full_text = f"{data['prompt']} {data['top']} {data['bottom']}"
        theme = detect_theme(full_text)
        quiz = get_quiz(theme)

        if quiz:
            view = QuizView(quiz)
            await ctx.send(
                f"🎉 Fun quiz tema **{theme}**:\n{quiz['q']}\n\n"
                f"🅰 {quiz['A']}\n"
                f"🅱 {quiz['B']}",
                view=view
            )


    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="🤖 MemeAI Bot",
        description="Bot pembuat meme + quiz yang ngerti penderitaan manusia.",
        color=discord.Color.purple()
    )

    embed.add_field(
        name="🧩 Fitur Utama",
        value=
        "🎨 Generate meme dari prompt\n"
        "🎲 Meme random siap pakai\n"
        "🧠 Quiz interaktif berdasarkan tema\n"
        "💬 Support bahasa Indonesia",
        inline=False
    )

    embed.add_field(
        name="🎭 Personality Bot",
        value=
        "• Tidak toxic\n"
        "• Tidak ngejudge pilihan hidup kamu\n"
        "• Selalu ada saat kamu capek\n"
        "• Tapi tetap tidak bisa memperbaiki hidup kamu",
        inline=False
    )

    embed.add_field(
        name="⚡ Status",
        value=
        f"Online di **{len(bot.guilds)} server**\n"
        f"Latency: **{round(bot.latency * 1000)} ms**",
        inline=False
    )

    embed.add_field(
        name="🎮 Commands",
        value=
        "`!meme prompt | atas | bawah`\n"
        "`!meme_random`\n"
        "`!start`\n"
        "`!info`",
        inline=False
    )

    embed.set_footer(text="Bot ini dibuat untuk mengubah penderitaan menjadi meme.")

    await ctx.send(embed=embed)



bot.run(TOKEN)
