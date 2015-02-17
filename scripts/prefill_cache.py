import click

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@click.command()
@click.argument('base_url', type=str)
def main(base_url):
    driver = webdriver.Firefox()
    driver.get(base_url)
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
        if "profiles/b" in url or "profiles/c" in url:
            try:
                iframes = driver.find_elements_by_xpath("//div[@class='lightbox guide_app']/iframe")
                links = driver.find_elements_by_class_name("app_links")
                for idx, link in enumerate(links):
                    frame = iframes[idx]
                    link.click()
                    driver.switch_to_frame(driver.find_element_by_id(frame.get_attribute("id")))
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "key"))
                    )
                    driver.switch_to_default_content()

            except Exception, exception:
                print "Moving on after 10 second wait.", str(exception)

if __name__ == "__main__":
    main()