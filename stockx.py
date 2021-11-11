import datetime
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def captcha():
    print("{}: Solve captcha".format(datetime.datetime.now()))
    time.sleep(5)


class Stockx:

    def __init__(self, driver, sku, email, password, price, rate_gbp, date, last_month, current_month):
        self.driver = driver
        self.sku = sku
        self.email = email
        self.password = password
        self.value = price
        self.rate_gbp = rate_gbp
        self.date = date
        self.last_month = last_month
        self.current_month = current_month

    def region(self):
        # Chooses country
        self.driver.get("https://stockx.com/")
        time.sleep(3)

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@role="dialog'
                                                                                              '"]/footer/button')))
                self.driver.find_element_by_xpath('/html/body/div[5]/div[4]/div/section/footer/button').click()
                break
            except Exception as e:
                print(e)
                captcha()
        time.sleep(4)

    def logging_in(self):
        # Logs

        while True:
            try:
                self.driver.find_element_by_xpath('//*[@id="nav-login"]').click()
                break
            except Exception:
                captcha()
        self.driver.refresh()

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((
                    By.XPATH, '//*[@id="email-login"]')))
                self.driver.find_element_by_xpath('//*[@id="email-login"]').send_keys(self.email)
                time.sleep(0.5)
                self.driver.find_element_by_xpath('//*[@id="password-login"]').send_keys(self.password)
                time.sleep(2)
                break
            except Exception:
                captcha()

    def product_link(self):
        # Finds product link
        while True:
            try:
                self.driver.get("https://stockx.com/search/sneakers?s={}".format(self.sku))
                break
            except Exception:
                continue

        while True:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@data-testid'
                                                                                              '="search-confirmation"]')
                                                                                   ))
                href = self.driver.find_element_by_xpath('//*[@data-testid="product-tile"]')
                return href.find_element_by_css_selector('a').get_attribute('href')
            except Exception:
                captcha()

    def item_info(self):
        # Gets product name, sku and sizes

        self.driver.get(self.product_link())

        # Scraps sizes
        sizes = ""
        item_name1 = self.driver.find_element_by_xpath('//*[@class="chakra-heading css-146c51c"]'). \
            get_attribute("innerText")
        item_name2 = self.driver.find_element_by_xpath('//*[@class="chakra-heading css-xgzdo7"]'). \
            get_attribute("innerText")
        for s in range(1, 27):
            try:
                while True:
                    try:
                        self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div[3]/div['
                                                          '2]/div[1]/div[1]/div/button').click()
                        break
                    except Exception:
                        try:
                            self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section[1]/div['
                                                              '4]/div[2]/div[1]/div[1]/div/button').click()
                            break
                        except Exception:
                            print('Something wrong')
                        print('Something wrong')

                # Chooses appropriate size
                try:
                    if '€' in self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                                '2]/div/dl/dd[@class="chakra-stat__number '
                                                                'css-1pulpde"]'.format(s)).text or '$' in \
                            self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]/span['
                                                              '2]/div/dl/dd[@class="chakra-stat__number '
                                                              'css-1pulpde"]'.format(s)).text:
                        self.logging_in()
                        return self.item_info()

                    self.driver.find_element_by_xpath('//div[@class="css-1o6kz7w"]/button[{}]'.format(s)).click()

                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="chakra'
                                                                                                  '-button__group '
                                                                                                  'css-1etipep'
                                                                                                  '"]/button[3]')))
                    self.driver.find_element_by_xpath('//*[@class="chakra-button__group css-1etipep"]/button[3]').\
                        click()

                    staleElement = True
                    date1 = 0
                    date_month = ""
                    count = 0
                    size = ""
                    while staleElement:
                        try:
                            count = len(self.driver.find_elements_by_class_name('css-153ufkt'))
                            date = str(self.driver.find_element_by_xpath('//*[@class="css-aydg0x"]/tr[20]/td[1]/p').
                                       get_attribute('innerText'))
                            size = str(self.driver.find_element_by_xpath('//*[@class="css-aydg0x"]/tr[1]/td[3]/p').
                                       get_attribute("innerText"))
                            date_month = date[0:3]
                            date = date[4:6]
                            if ',' in date:
                                date = date.replace(',', '')
                            date1 = int(date)
                            staleElement = False
                        except Exception:
                            staleElement = True
                            if (count < 20) and (count != 0):
                                staleElement = False

                    while True:
                        try:
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*['
                                                                                                          '@aria'
                                                                                                          '-label'
                                                                                                          '="Close"]')))
                            self.driver.find_element_by_xpath('//*[@aria-label="Close"]').click()
                            break
                        except Exception:
                            self.driver.refresh()
                            break

                    try:
                        price = int(self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section['
                                                                      '1]/div[3]/div[2]/div[1]/div[2]/div['
                                                                      '2]/div/dl/dd').get_attribute(
                            "innerText").replace('£', ''))
                        price1 = (price - (price * 0.03) - (price * 0.065)) * self.rate_gbp
                        percent = (price1 - (self.value / 1.23)) / (self.value / 1.23)
                    except Exception:
                        price = int(self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div/section['
                                                                      '1]/div[4]/div[2]/div[1]/div[2]/div['
                                                                      '2]/div/dl/dd').get_attribute(
                            "innerText").replace('£', ''))
                        price1 = (price - (price * 0.03) - (price * 0.065)) * self.rate_gbp
                        percent = (price1 - (self.value / 1.23)) / (self.value / 1.23)

                    # If margin is >= 28% then write size
                    if percent >= 0.28:
                        sizes += (size + ", ")
                        continue

                    if (count < 20) and (count != 0):
                        continue

                    # If difference between 20th purchase and today's day is more 7 days then next size
                    if self.date - date1 > 7:
                        continue
                    if self.date < 8:
                        if (date_month != self.current_month) and (date_month != self.last_month):
                            continue
                    else:
                        if date_month != self.current_month:
                            continue

                    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@class="chakra'
                                                                                                  '-button__group '
                                                                                                  'css-1etipep'
                                                                                                  '"]/button[1]')))
                    self.driver.find_element_by_xpath('//*[@class="chakra-button__group css-1etipep"]/button[1]').\
                        click()

                    staleElement = True
                    list_price = 0
                    while staleElement:
                        try:
                            list_price = float(self.driver.find_element_by_xpath('//*[@class="css-aydg0x"]/tr[1]/td['
                                                                                 '3]/p/p').get_attribute(
                                "innerText").replace('£', ''))
                            staleElement = False
                        except Exception:
                            staleElement = True
                    list_price1 = (list_price - (list_price * 0.03) - (list_price * 0.065)) * self.rate_gbp
                    percent = (list_price1 - (self.value / 1.23)) / (self.value / 1.23)

                    while True:
                        try:
                            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*['
                                                                                                          '@aria'
                                                                                                          '-label'
                                                                                                          '="Close"]')))
                            self.driver.find_element_by_xpath('//*[@aria-label="Close"]').click()
                            break
                        except Exception:
                            self.driver.refresh()
                            break

                    # If margin is >= 28% then write size
                    if percent >= 0.28:
                        sizes += (size + ", ")
                        continue

                except Exception:
                    continue
            except Exception as e:
                print(e)
                print('{}:Nothing for sale'.format(datetime.datetime.now()))

        return [item_name1 + " " + item_name2, sizes[:-2]]
