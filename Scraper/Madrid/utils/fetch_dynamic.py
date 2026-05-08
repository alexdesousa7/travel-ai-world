from playwright.sync_api import sync_playwright

def fetch_dynamic_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--disable-web-security",
                "--disable-features=IsolateOrigins,site-per-process",
                "--disable-site-isolation-trials",
                "--start-maximized"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
            timezone_id="Europe/Madrid"
        )

        page = context.new_page()

        # ---- STEALTH MANUAL ----
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

            window.navigator.chrome = {
                runtime: {},
            };

            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3],
            });

            Object.defineProperty(navigator, 'languages', {
                get: () => ['es-ES', 'es'],
            });
        """)

        # -------------------------

        page.goto(url, wait_until="domcontentloaded")

        # Aceptar cookies si aparece
        try:
            page.click("button#onetrust-accept-btn-handler", timeout=3000)
        except:
            pass

        # Simular actividad humana
        page.mouse.move(200, 300)
        page.wait_for_timeout(500)
        page.mouse.move(400, 500)
        page.wait_for_timeout(500)

        # Scroll para disparar carga dinámica
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

        html = page.content()
        browser.close()
        return html
