class XPathElementsLogin:
    cookies_element = '//*[@id="cookie-intro"]/div[2]/a'
    login_button = '//*[@id="site-header"]/nav/button'
    email_element = '//*[@id="email"][@data-testid="email"]'
    psw_element = '//*[@id="password"][@name="password"]'
    submit_element = '//*[@id="__next"]/main//form//button[@type="submit"]'
    waiting_download_element = '//*[@id="__next"]/div/div[1]/div[1]/a[3]/div'


class XPathElementsAddInfo:
    title_add_info = '//*[@id="__next"]/main//dl[@data-testid="service-request-questions-lists"]//dt'
    value_add_info = '//*[@id="__next"]/main//dl[@data-testid="service-request-questions-lists"]//dd'


class XPathElementsApplyJobRequest:
    button_interesse = '//*[@id="__next"]//button[@data-testid="express-interest-btn"]//span[text()="Toon interesse"]'
    verstuur = '//*[@id="__next"]//button[@data-testid="express-interest-send-button"]//span[text()="Verstuur"]'
    interest_is_expressed = '//*[@id="__next"]//div[@data-testid="interest-is-expressed-alert"]'
