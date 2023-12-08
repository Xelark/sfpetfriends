import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
chromedriver_autoinstaller.install()

@pytest.fixture(autouse=True)
def driver():
   driver = webdriver.Chrome()
   driver.maximize_window()
   # Переходим на страницу авторизации
   driver.get('http://petfriends.skillfactory.ru/login')


   yield driver

   driver.quit()


def test_show_all_pets(driver):

   # Вводим email
   driver.find_element(By.ID, 'email').send_keys('alex@alex.ru')
   # Вводим пароль
   driver.find_element(By.ID, 'pass').send_keys('alex')
   # Нажимаем на кнопку входа в аккаунт
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя и добавляем неявное ожидание
   driver.implicitly_wait(10)
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
   #Записываем в переменные фото, имена и возраст с породами
   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
   names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
   descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')
   #Проверяем, что карточки не имеют пустых фото, имен, возрастов и пород
   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0
