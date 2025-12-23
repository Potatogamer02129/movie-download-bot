from time import sleep

from playwright.sync_api import sync_playwright

def parse_query(query: str) -> tuple[str, str] | str:
    lst = query.split()
    lang = lst[0]
    return lang, '+'.join(lst[1:])

def build_search_url(language: str, movie: str) -> str | None:
    if language.lower() == 'english':
        return f"https://moviesmod.cards/search/{movie}"
    elif language.lower() == 'hindi':
        return f"https://moviesleech.eu/search/{movie}"
    return None

def open_first_result(page) -> None:
    page.wait_for_selector("article.latestPost",timeout=5000)
    first_result = page.locator("article.latestPost").first
    first_result.locator("h2.title a").click()

def extract_poster_url(page) -> str | None:
    page.wait_for_selector("article")
    poster = page.locator("article img").first
    poster_link = poster.get_attribute("src")
    if not poster_link:
        poster_link = poster.get_attribute("data-src")
    return poster_link

def select_1080p_download(page) -> str | None:
    try:
        page.wait_for_selector("a.maxbutton-1.maxbutton.maxbutton-download-links",timeout=5000)
        downloads = page.locator("a.maxbutton-1.maxbutton.maxbutton-download-links")
        num = downloads.count()
        if num <= 2:
            return downloads.nth(num - 1).get_attribute("href")
        else:
            return downloads.nth(2).get_attribute("href")
    except Exception as e:
        print("Timeout error")
        return None

def bypass_verification_page(page) -> str | None:
    page.wait_for_selector("text=START VERIFICATION")
    page.locator("text=START VERIFICATION").evaluate("el => el.click()")

    page.wait_for_selector("text=VERIFY TO CONTINUE")
    page.locator("text=VERIFY TO CONTINUE").evaluate("el => el.click()")

    page.wait_for_selector("text=CLICK HERE TO CONTINUE")
    page.locator("text=CLICK HERE TO CONTINUE").evaluate("el => el.click()")

    page.wait_for_selector("a:has-text('GO TO DOWNLOAD')")
    return page.locator("a:has-text('GO TO DOWNLOAD')").first.get_attribute("href")

def get_cdn_link(page) -> str | None:
    page.wait_for_selector("body",timeout=5000)
    page.add_style_tag(content="iframe { pointer-events: none !important; }")
    page.wait_for_selector("a[href*='video-leech']")
    link_again = page.locator("a[href*='cdn.video-leech']").nth(0).get_attribute("href")
    page.goto(link_again)
    page.wait_for_selector("text=Instant Download")
    final_link = page.locator("a[href*='video-downloads']").nth(0).get_attribute("href")
    return final_link

def get_download_link(user_txt: str) -> str | tuple[str | None, str | None]:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, args=["--mute-audio"])
    context = None
    try:
        context = browser.new_context()
        page = context.new_page()
        lang,movie_name = parse_query(user_txt)
        if lang.lower() not in ("english","hindi"):
            return "Specify Movie Language First\nFor example:\nEnglish Avatar\nor\nHindi Stree\nTry again"
        movie_site = build_search_url(lang, movie_name)
        if not movie_site:
            return "Specify Movie Language First\nFor example:\nEnglish Avatar\nor\nHindi Stree\nTry again"
        page.goto(movie_site)
        image_link = extract_poster_url(page)
        open_first_result(page)
        FullHD = select_1080p_download(page)
        if not FullHD:
            return "Movies only please", None
        else:
            page.goto(FullHD)
        #page.goto(select_1080p_download(page))
        FastServer_link = page.locator("a[href*='unblockedgames']").nth(0).get_attribute("href")
        page.goto(FastServer_link)
        page.goto(bypass_verification_page(page) , wait_until="domcontentloaded")
        return get_cdn_link(page) , image_link
    except Exception as e:
        print(e)
        return "Error Try Again (3 Times max then search for another movie)",None
    finally:
        browser.close()
        pw.stop()

if __name__ == "__main__":
    movie = input("Enter movie title: ")
    link = get_download_link(movie)
    print(link)