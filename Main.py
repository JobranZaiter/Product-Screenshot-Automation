import asyncio
import random
import os
import logging
import uuid
from playwright.async_api import async_playwright

local_screenshot_dir = "screenshots"
if not os.path.exists(local_screenshot_dir):
    os.makedirs(local_screenshot_dir)

logging.basicConfig(level=logging.INFO)

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

urls = [
    "https://www.saksoff5th.com/product/gucci-%E2%80%8B60mm-round-sunglasses-0400018811922.html",
    "https://poshmark.com/listing/NEW-Gucci-Blue-and-Silver-Square-Womens-Sunglasses-6290c466e0b7c752f973731d",
    "https://www.amazon.sa/%D9%86%D8%B8%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D9%86%D8%B3%D8%A7%D8%A1-%D8%BA%D9%88%D8%AA%D8%B4%D9%8A-%D9%88%D8%A7%D8%AD%D8%AF%D8%A9-60mm%D8%8C/dp/B09QXRXKWH?th=1&psc=1",
    "https://www.speert.com/gucci-gg0972s-003-women-designer-sunglasses-gold-brown-tortoise-havana-pink-60mm/",
    "https://www.nordstrom.com/s/prada-54mm-gradient-rectangle-sunglasses/5936259",
    "https://www.ebay.com/itm/256497007169",
    "https://saudiglasses.com/en/product/gucci-sunglasses-gg1005s-001/",
    "https://almadinaopt.com/en/gucci-0972-60-004-sg/p2074982143",
    "https://www.edel-optics.com/HER-0145-S-DDB-3X-by-Carolina-Herrera.html",
    "https://www.eyeons.com/vogue-vo4207s",
    "https://www.edel-optics.com/Sunglasses-for-trapezium-Faces-79.html",
    "https://www.yoox.com/ch/46756891KU/item",
    "https://www.warehousefashion.com/product/gucci-butterfly-silver-brown-gradient-gg1005s_p-0072fb61-fe9b-4c83-9371-b92645846d17",
    "https://s.click.aliexpress.com/deep_link.htm?aff_short_key=UneMJZVf&dl_target_url=https%3A%2F%2Fpt.aliexpress.com%2Fitem%2F1005005889889642.html%3F_randl_currency%3DEUR%26_randl_shipto%3DPT%26src%3Dgoogle",
    "https://www.diffeyewear.com/products/iris-gold-inca-gradient-sunglasses",
    "https://uniglasses.com/product/gg0882sa-005-60-gold/",
    "https://www.ebay.ca/itm/384898435539",
    "https://glasseseasybuy.com/products/sun-soar",
    "https://www.go-optic.com/metal-coach",
    "https://www.designereyes.com/products/gucci-gg0972s-de-sunglasses",
    "https://pretavoir.us/products/max-mara-mm0061-design5-16w",
    "https://www.otticasm.com/en/sunglasses-victoria-beckham-vb232s-601.html",
    "https://www.otticait.com/en/guess-gu7785-32w",
    "https://www.dhgate.com/product/2022-women-men-high-quality-fashion-sunglasses/927253728.html",
    "https://sunglassstyle.com.au/shop/brand/polaroid/pldcn-0030fs-gold-red-shaded-polarised-pol-alt-fit/",
    "https://www.pinterest.com.mx/pin/brand-new-gucci-gg0972s-004-silverlight-blue-women-sunglasses--344877283977501025/",
    "https://www.amazon.eg/-/en/Despada-DS1948-C3-DESPADA-1948-SUNGLASSES/dp/B09KQX8DX2",
    "https://www.eopticians.co.uk/gant-ga-8083-32f-sunglasses-60",
    "https://idee-eyewear.com/collections/sunglasses/products/idee-2869",
    "https://www.ebay.com/itm/185024489696",
    "https://maverickandwolf.com/products/miu-miu-smu52w",
    "https://www.opticabassol.com/se/solglasogon/guess-fran_6_till_8_arbetsdagar?p=4&price=amshopby_slider_from-amshopby_slider_to",
    "https://www.occhialando.eu/sunglasses/ralph-lauren-ra-4138-911662-bordeaux-sunglasses-woman-square",
    "https://blinkblink.pl/en/products/gucci-sunglasses-gg0972s-001-67767.html",
    "https://www.theopticalshop.ca/products/coach-hc7132",
    "https://www.facebook.com/optometrijos.centras/videos/atrask-savo-gucci-optometrijos-centre/431907075140305/?locale=ms_MY",
    "https://www.designerglasses.co.uk/product/guess-gu7785-sunglasses/",
    "https://lookeronline.com/products/vogue-eyewear-0vo4198s-280-36-top-red-gold-pink-gradient-dark-grey",
    "https://br.revolve.com/miu-miu-square-in-gold-pink-gradient/dp/MIUR-WA46/?d=Womens&page=1&lc=14&itrownum=28&itcurrpage=1&itview=05",
    "https://www.facebook.com/menaraoptometrymidvalley/",
    "https://www.idealo.it/cat/9112F1970449/occhiali-da-sole.html",
    "https://otticaachilli.com/prodotto/gucci-gg0972s-004/",
    "https://www.boyner.com.tr/hermossa-gunes-gozlugu-1809796",
    "https://www.ebay.com/itm/385576364082",
    "https://www.ebay.com/itm/404953157913?chn=ps&mkevt=1&mkcid=28",
    "https://www.ebay.com/itm/285551274292"
];


async def handle_console_message(msg):
    logging.info(f"Console message: {msg.text}")


async def random_delay(min_seconds=3, max_seconds=10):
    await asyncio.sleep(random.uniform(min_seconds, max_seconds))


async def simulate_human_behavior(page):
    await page.evaluate('''() => {
        const scrollHeight = document.body.scrollHeight;
        const totalSteps = 10;
        let currentStep = 0;

        function smoothScroll() {
            if (currentStep >= totalSteps) return;
            const scrollTo = (currentStep / totalSteps) * scrollHeight;
            window.scrollTo(0, scrollTo);
            currentStep++;
            setTimeout(smoothScroll, 100 + Math.random() * 200);
        }

        smoothScroll();
    }''')
    await random_delay(3, 10)


async def run_script(page):
    await page.evaluate(r'''() => {
        const blockPatterns = [
            ".html",
            ".css",
            ".js"
        ];

        function shouldBlock(url) {
            return blockPatterns.some(e=> url.includes(e));
        }

        function interceptFetch() {
            const oldFetch = window.fetch;
            window.fetch = function(url, options) {
                if (shouldBlock(url)) {
                    console.log(`Blocking fetch request to: ${url}`);
                    return Promise.reject(new Error(`Blocked request to: ${url}`));
                }
                return oldFetch.apply(this, arguments);
            };
        }

        function interceptXHR() {
            const oldOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url) {
                if (shouldBlock(url)) {
                    console.log(`Blocking XMLHttpRequest to: ${url}`);
                    this.abort();
                    return;
                }
                return oldOpen.apply(this, arguments);
            };
        }

        function interceptDocument() {
            try {
                const iframeDescriptor = Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'src');
                if (iframeDescriptor && iframeDescriptor.set) {
                    const oldIFrameSrc = iframeDescriptor.set;
                    Object.defineProperty(HTMLIFrameElement.prototype, 'src', {
                        set: function(url) {
                            if (shouldBlock(url)) {
                                console.log(`Blocking iframe request to: ${url}`);
                                return;
                            }
                            oldIFrameSrc.call(this, url);
                        }
                    });
                }

                const frameDescriptor = Object.getOwnPropertyDescriptor(HTMLFrameElement.prototype, 'src');
                if (frameDescriptor && frameDescriptor.set) {
                    const oldFrameSrc = frameDescriptor.set;
                    Object.defineProperty(HTMLFrameElement.prototype, 'src', {
                        set: function(url) {
                            if (shouldBlock(url)) {
                                console.log(`Blocking frame request to: ${url}`);
                                return;
                            }
                            oldFrameSrc.call(this, url);
                        }
                    });
                }
            } catch (error) {
                console.error("Error intercepting document requests:", error);
            }
        }

        function cleanDOM() {
            const blacklistPatterns = [
                "popup",
                "pop-up",
                "pop",
                "advertisement",
                "sponsored",
                "dialogue",
                "dialog",
                "cookie",
                "important",
                "needsclick",
            ];

            const whitelistTags = ['nav', 'footer', 'main', 'header', 'img', 'body'];

            function isElementFullScreenWidth(el) {
                const rect = el.getBoundingClientRect();
                return Math.abs(rect.width - window.innerWidth) < 1;
            }

            function isElementAtTop(el, threshold = 50) {
                const rect = el.getBoundingClientRect();
                return rect.top <= threshold;
            }

            function isElementAtBottom(el, threshold = 50) {
                const rect = el.getBoundingClientRect();
                return rect.bottom <= threshold;
            }

            function isElementInMiddleH(el, threshold = 100) {
                const rect = el.getBoundingClientRect();
                const elementCenter = (rect.left + rect.right) / 2;
                const viewportWidth = window.innerWidth;
                const viewportCenter = viewportWidth / 2;

                return Math.abs(elementCenter - viewportCenter) <= threshold;
            }

            function isElementInMiddleV(el, threshold = 100) {
                const rect = el.getBoundingClientRect();
                const elementCenter = (rect.top + rect.bottom) / 2;
                const viewportHeight = window.innerHeight;
                const viewportCenter = viewportHeight / 2;

                return Math.abs(elementCenter - viewportCenter) <= threshold;
            }

            function shouldHideElement(el) {
                const tagName = el.tagName.toLowerCase();
                const className = (el.getAttribute('class') || '').toLowerCase();
                const id = (el.getAttribute('id') || '').toLowerCase();
                const role = (el.getAttribute('role') || '').toLowerCase();
                const style = window.getComputedStyle(el);
                const zIndex = parseInt(style.zIndex, 10);
                const isPositioned = style.position === 'fixed' || style.position === 'absolute';
                const isFullScreenWidth = isElementFullScreenWidth(el);
                const isInMiddleH = isElementInMiddleH(el);
                const isInMiddleV = isElementInMiddleV(el);
                const isWhitelistedTag = whitelistTags.includes(tagName);
                const isTop = isElementAtTop(el);
                const isBottom = isElementAtBottom(el);

                let score = 0;
                if (isWhitelistedTag) {
                    return false;
                }

                const isBlacklisted = blacklistPatterns.some(pattern =>
                    id.includes(pattern) || className.includes(pattern) || role.includes(pattern)
                );
                if (isBlacklisted) {
                    console.log(`Element with id="${id}" or class="${className}" or role="${role}" is blacklisted.`);
                    return true;
                }
                if (!isNaN(zIndex) && zIndex > 1000) {
                    score += 5;
                }
                if (isPositioned) {
                    score += 2;
                }
                if (isFullScreenWidth && (isTop || isBottom)) {
                    score += 2;
                }
                if (isInMiddleH && !isFullScreenWidth) {
                    score += 2;
                }
                if (isInMiddleV && !isFullScreenWidth) {
                    score += 2;
                }
                const hideThreshold = 7;
                return score >= hideThreshold;
            }

            function hideUnwantedElements() {
                const processedElements = new Set();

                function processElement(el) {
                    if (processedElements.has(el)) return;

                    if (shouldHideElement(el)) {
                        el.remove();
                        console.log(`Removed element ${el}`);
                        processedElements.add(el);
                    } else {
                        el.childNodes.forEach(child => {
                            if (child.nodeType === 1) {
                                processElement(child);
                            }
                        });
                    }
                }
                processElement(document.body);
            }

            hideUnwantedElements();
        }

        function removeAutofocus() {
            document.querySelectorAll('[autofocus]').forEach(el => {
                el.removeAttribute('autofocus');
            });
        }

    function removeAllBlurEffects() {
    document.querySelectorAll('*').forEach(el => {
        const filter = el.style.filter;
        if (filter) {
            el.style.filter = filter.replace(/blur\(.*?\)/g, '').trim();
            if (el.style.filter === '') el.style.removeProperty('filter');
        }

        const backdropFilter = el.style.backdropFilter;
        if (backdropFilter) {
            el.style.backdropFilter = backdropFilter.replace(/blur\(.*?\)/g, '').trim();
            if (el.style.backdropFilter === '') el.style.removeProperty('backdrop-filter');
        }
    });

    const styleSheets = Array.from(document.styleSheets);
    styleSheets.forEach(sheet => {
        try {
            const rules = Array.from(sheet.cssRules || []);
            rules.forEach(rule => {
                if (rule.style && (rule.style.filter.includes('blur') || rule.style.backdropFilter.includes('blur'))) {
                    rule.style.filter = rule.style.filter.replace(/blur\(.*?\)/g, '').trim();
                    if (rule.style.filter === '') rule.style.removeProperty('filter');

                    rule.style.backdropFilter = rule.style.backdropFilter.replace(/blur\(.*?\)/g, '').trim();
                    if (rule.style.backdropFilter === '') rule.style.removeProperty('backdrop-filter');
                }
            });
        } catch (e) {
            console.warn('Cannot access stylesheet rules:', e);
        }
    });

    console.log('All blur effects removed.');
}



    console.log('Visual effects removed for all elements except images.');

        interceptFetch();
        interceptXHR();
        interceptDocument();
        removeAutofocus();
        setInterval(() => {
            cleanDOM();
            removeAllBlurEffects();
        }, 3000);
    }''')


async def load_page_with_retry(page, url, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            response = await page.goto(url, wait_until='load', timeout=60000)
            if response.ok:
                await run_script(page)
                await page.wait_for_timeout(1000)
                await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

                product_elements = await page.query_selector_all('img')
                if product_elements:
                    logging.info(f"Page loaded successfully on attempt {attempt + 1}")
                    return True
                else:
                    logging.warning(f"Page loaded, but no product elements found on attempt {attempt + 1}")
            else:
                logging.error(f"Failed to load page on attempt {attempt + 1}. Status: {response.status}")
        except Exception as e:
            logging.error(f"Error loading page on attempt {attempt + 1}: {e}")

        await random_delay(10, 20)

    logging.error(f"Failed to load {url} after {max_attempts} attempts")
    return False


async def process_url(url, page):
    logging.info(f"Opening {url}...")

    success = await load_page_with_retry(page, url)
    if not success:
        logging.error(f"Failed to load {url} after multiple attempts")
        return

    page_title = await page.title()
    logging.info(f"Page title: {page_title}")

    await page.evaluate('window.scrollTo(0, 0)')
    await page.wait_for_timeout(9000)
    unique_id = uuid.uuid4()
    screenshot_filename = f"screenshot_{unique_id}.png"
    screenshot_path = os.path.join(local_screenshot_dir, screenshot_filename)
    await page.screenshot(path=screenshot_path, full_page=True)
    logging.info(f"Full page screenshot taken: {screenshot_path}")

    await random_delay(10, 20)


async def main():
    browser = None
    try:
        async with async_playwright() as p:
            brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            user_data_dir = r"C:\Users\User\AppData\Local\BraveSoftware\Brave-Browser\User Data"
            extensions_path = os.path.join(user_data_dir, "Default 1", "Extensions")

            extension_paths = []
            for ext_id in os.listdir(extensions_path):
                ext_path = os.path.join(extensions_path, ext_id)
                if os.path.isdir(ext_path):
                    versions = os.listdir(ext_path)
                    if versions:
                        latest_version = max(versions)
                        full_ext_path = os.path.join(ext_path, latest_version)
                        extension_paths.append(full_ext_path)

            extensions_arg = ','.join(extension_paths)

            browser = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                executable_path=brave_path,
                headless=False,
                args=[
                    '--start-maximized',
                    '--profile-directory= Default 1',
                    f'--load-extension={extensions_arg}',
                    '--disable-blink-features=AutomationControlled',
                ],
                viewport={'width': 1920, 'height': 1080}
            )

            print("Browser initialized successfully")

            page = await browser.new_page()

            await page.evaluate('''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            ''')
            for url in urls:
                page.on('popup', lambda popup: asyncio.create_task(popup.close()))
                page.on('dialog', lambda dialog: asyncio.create_task(dialog.dismiss()))
                await process_url(url, page)

    except Exception as e:
        print(f"Failed to initialize browser: {e}")
    finally:
        if browser:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
