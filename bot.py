headers={"Authorization": f"Bearer {KEY}"},
                json={"model": MODEL, "messages": [
                    {"role": "user", "content": update.message.text}
                ]},
            )
            response.raise_for_status()
            answer = response.json()["choices"][0]["message"].get("content")
        if not answer:
            answer = "ما وصلني رد، جرّب مرة تانية"
        for i in range(0, len(answer), 4000):
            await update.message.reply_text(answer[i:i + 4000])
    except Exception:
        await update.message.reply_text("ما قدرت أجيب الرد، جرّب مرة تانية")

async def main():
    bot = Application.builder().token(TOKEN).build()
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

async def health(request):
        return web. Response(text="OK")

async def webhook(request):
        given = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not hmac.compare_digest(given, SECRET):
            raise web.HTTPForbidden()
        try:
            data = await request.json()
            update = Update.de_json(data, bot.bot)
        except Exception:
            raise web.HTTPBadRequest()
        await bot.update_queue.put(update)
        return web. Response(text="OK")

server = web. Application(client_max_size=1024 * 1024)
    server.router.add_get("/", health)
    server.router.add_post("/telegram", webhook)
    runner = web. AppRunner(server)
    await bot.initialize()
    await bot.start()
    try:
        await runner.setup()
        await web.TCPSite(runner, "0.0.0.0", int(os.environ.get("PORT", "10000"))).start()
        await bot.bot.set_webhook(url=BASE_URL + "/telegram", secret_token=SECRET)
        await asyncio. Event().wait()
    finally:
        await runner.cleanup()
        await bot.stop()
        await bot.shutdown()

if name == "main":
    asyncio.run(main())
