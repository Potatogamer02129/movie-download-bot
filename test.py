from time import sleep

from playwright.sync_api import sync_playwright



def get_download_link(movie: str) -> str:
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False, args=["--mute-audio"])
    context = None
    try:
        context = browser.new_context()
        page = context.new_page()
        lst = movie.split()
        lang = lst[0]
        if lang.lower() not in ("english","hindi"):
            return "Specify Movie Language First\nFor example:\nEnglish Avatar\nor\nHindi Stree\nTry again"
        lst.pop(0)
        movie = "+".join(lst)
        if lang.lower() == "english":
            movie_site = f"https://moviesmod.cards/search/{movie}"
        else:
            movie_site = f"https://moviesleech.eu/search/{movie}"
        page.goto(movie_site)
        #page.get_by_placeholder("What are you looking for?").fill(movie)
        #page.get_by_role("button").nth(0).click()

        page.wait_for_selector("article.latestPost")


        first_result = page.locator("article.latestPost").first

        # get the title link inside it
        #link = first_result.locator("h2.title a")
        first_result.locator("h2.title a").click()
        downloads = page.locator("a.maxbutton-1.maxbutton.maxbutton-download-links")
        num = downloads.count()
        if num <= 2:
            fullhd_link = downloads.nth(num-1).get_attribute("href")
        else:
            fullhd_link = downloads.nth(2).get_attribute("href")
        page.goto(fullhd_link)

        fullhd_link = page.locator("a[href*='unblockedgames']").nth(0).get_attribute("href")
        page.goto(fullhd_link)

        page.wait_for_selector("text=START VERIFICATION")
        page.locator("text=START VERIFICATION").evaluate("el => el.click()")

        page.wait_for_selector("text=VERIFY TO CONTINUE")
        page.locator("text=VERIFY TO CONTINUE").evaluate("el => el.click()")

        page.wait_for_selector("text=CLICK HERE TO CONTINUE")
        page.locator("text=CLICK HERE TO CONTINUE").evaluate("el => el.click()")

        page.wait_for_selector("a:has-text('GO TO DOWNLOAD')")
        final_url = page.locator("a:has-text('GO TO DOWNLOAD')").first.get_attribute("href")
        page.goto(final_url , wait_until="domcontentloaded")
        page.wait_for_selector("body")
        page.add_style_tag(content="iframe { pointer-events: none !important; }")
        page.wait_for_selector("a[href*='video-leech']")
        link_again = page.locator("a[href*='cdn.video-leech']").nth(0).get_attribute("href")
        page.goto(link_again)
        page.wait_for_selector("text=Instant Download")
        final_link = page.locator("a[href*='video-downloads']").nth(0).get_attribute("href")
        print(final_link)
        return final_link
    except Exception as e:
        print(e)
        return "Error Try Again (3 Times max then search for another movie)"
    finally:
        browser.close()
        pw.stop()

if __name__ == "__main__":
    movie = input("Enter movie title: ")
    link = get_download_link(movie)
    print(link)