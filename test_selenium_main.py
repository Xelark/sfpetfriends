import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
chromedriver_autoinstaller.install()

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   driver.maximize_window()
   # Переходим на страницу авторизации
   driver.get('http://petfriends.skillfactory.ru/login')


   yield driver

   driver.quit()


def test_show_my_pets(driver):

   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('alex@alex.ru')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('alex')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   #assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

   #Открываем раздел Мои питомцы
   driver.find_element(By.XPATH, '//a[text()="Мои питомцы"]').click()
   #Добавляем явное ожидание загрузки таблицы со списком питомцев
   WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//table[@class="table table-hover"]/tbody/tr')))
   #Получаем список существующих питомцев
   sum_my_pets = driver.find_element(By.XPATH, '//div[@class =".col-sm-4 left"]').text.split('\n')[1].split(':')[1]
   #Получаем цифру статистики питомцев
   table_my_pets = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

   #Проверка соответствия числа у пользователя с числом записей в таблице
   assert len(table_my_pets) == int(sum_my_pets)

   #Получаем и группируем список имен, пород и изображений питомцев
   names = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[1]')
   breeds = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[2]')
   ages = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table[1]/tbody[1]/tr[1]/td[3]')
   images = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr[1]/th')

   #В цикле проверяем, что у каждой записи по имени есть так же возраст и порода
   for i in range(len(names)):
      assert names[i].text != ''
      assert breeds[i].text != ''
      assert ages[i] != ''

   #Проверяем, что количество питомцев с фото больше половины
   count_image = 0
   for i in range(len(images)):
      if images[i].get_attribute('src') != '':
         count_image += 1

   assert count_image > len(images)/2


