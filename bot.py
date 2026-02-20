import discord
from discord.ext import commands
from config import TOKEN
from ai import generate_image
from meme import make_meme
from kuis import detect_theme, QuizView
from database import get_quiz
import random

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

RANDOM_MEMES = [
    {"prompt":"tired programmer late night","top":"NIAT TIDUR CEPET","bottom":"TAU TAU SUBUH"},
    {"prompt":"confused cat meme","top":"GUA","bottom":"PAS LIAT SOAL"},
    {"prompt":"office worker staring at screen","top":"KATANYA KERJA TIM","bottom":"YANG KERJA GUA"},
    {"prompt":"sad anime boy","top":"BILANG GAPAPA","bottom":"PADAHAL CAPEK"},
    {"prompt":"dog sitting fire meme","top":"INI","bottom":"BAIK BAIK SAJA"}
]

@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")

@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="🚀 Botty Siap Tempur!",
        description=(
            "Halo! Aku bot meme + quiz random.\n\n"
            "Perintah yang bisa kamu pake:\n"
            "• `!meme prompt | teks atas | teks bawah`\n"
            "• `!meme_random`\n"
            "• `!info`\n\n"
            "Contoh:\n"
            "`!meme programmer stress | NIAT NGODING | MALAH DEBUG 3 JAM`"
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    embed = discord.Embed(
        title="ℹ️ Info Bot",
        description=(
            "Bot ini bisa:\n"
            "| Generate gambar AI\n"
            "| Bikin meme otomatis\n"
            "| Kasih quiz sesuai tema meme\n\n"
            "Dibuat pake discord.py + AI image generator.\n"
            "Prefix: `!`"
        ),
        color=discord.Color.green()
    )
    embed.set_footer(text=f"Diminta oleh {ctx.author}")
    await ctx.send(embed=embed)

@bot.command()
async def meme(ctx, *, args=None):
    try:
        await ctx.send("🧠 Lagi mikir meme...")
        if not args:
            await ctx.send("❌ Format: !meme prompt | teks atas | teks bawah")
            return
        parts = [p.strip() for p in args.split("|")]
        prompt = parts[0]
        top_text = parts[1] if len(parts)>1 else ""
        bottom_text = parts[2] if len(parts)>2 else ""
        image_path = generate_image(prompt)
        meme_path = make_meme(image_path, top_text, bottom_text)
        await ctx.send(file=discord.File(meme_path))
        theme = detect_theme(" ".join(parts))
        quiz = get_quiz(theme)
        if quiz:
            view = QuizView(quiz)
            await ctx.send(f"🎉 Fun quiz tema **{theme}**:\n{quiz['q']}\n\n🅰 {quiz['A']}\n🅱 {quiz['B']}", view=view)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

@bot.command()
async def meme_random(ctx):
    try:
        await ctx.send("🎲 Lagi nyari meme random...")
        data = random.choice(RANDOM_MEMES)
        image_path = generate_image(data["prompt"])
        meme_path = make_meme(image_path, data["top"], data["bottom"])
        await ctx.send(file=discord.File(meme_path))
        theme = detect_theme(f"{data['prompt']} {data['top']} {data['bottom']}")
        quiz = get_quiz(theme)
        if quiz:
            view = QuizView(quiz)
            await ctx.send(f"🎉 Fun quiz tema **{theme}**:\n{quiz['q']}\n\n🅰 {quiz['A']}\n🅱 {quiz['B']}", view=view)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(TOKEN)
