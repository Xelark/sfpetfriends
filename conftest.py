import pytest
import uuid


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = 'd:\\chromedriver.exe'
    #chrome_options.add_extension('/path/to/extension.crx')
    chrome_options.add_argument('--kiosk')
    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):

    driver = selenium
    driver.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield driver

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            driver.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            driver.save_screenshot('screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', driver.current_url)
            print('Browser logs:')
            for log in driver.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here
