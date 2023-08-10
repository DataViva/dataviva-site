import click
import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@click.command()
@click.argument('base_url', type=str)
def main(base_url):
    if not base_url.startswith("http://"):
        base_url = "https://" + base_url
    pages = ['/', '/apps']
    for page in pages:
        target = urlparse.urljoin(base_url, page)
        print "Crawling:", target
        crawl_page(target)


def crawl_page(page):
    driver = webdriver.Firefox()
    driver.get(page)
    links = driver.find_elements_by_tag_name("a")
    driver.implicitly_wait(5)

    urls = []

    for link in links:
        driver.switch_to_default_content()
        if link.is_displayed():
            url = link.get_attribute("href")
            print "url", url
            if url:
                urls.append(url)

    for url in urls:    
        driver.get(url)
        if "profiles/" in url and not url.endswith("profiles/"):
                iframes = driver.find_elements_by_xpath("//div[@class='lightbox guide_app']/iframe")
                links = driver.find_elements_by_class_name("app_links")
                for idx, link in enumerate(links):
                    try:
                        frame = iframes[idx]
                        # this way will allow us to click into hidden accordion links
                        driver.execute_script("arguments[0].click();", link);
                        driver.switch_to_frame(driver.find_element_by_id(frame.get_attribute("id")))
                        element = WebDriverWait(driver, 15).until(
                            EC.element_to_be_clickable((By.ID, "data"))
                        )
                        driver.switch_to_default_content()

                    except Exception, exception:
                        print "Moving on after 20 second wait.", str(exception)
                        driver.switch_to_default_content()
                        print "Error occured with link", link
        elif "/apps/builder" in url:
            frame = driver.find_element_by_xpath("//div[@class='lightbox']/iframe")
            driver.switch_to_frame(driver.find_element_by_id(frame.get_attribute("id")))
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "data"))
                )
            except Exception, exception:
                print "Moving on after 10 second wait.", str(exception)
            driver.switch_to_default_content()


if __name__ == "__main__":
    main()
