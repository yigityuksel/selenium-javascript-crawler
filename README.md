# Selenium Javascript Crawler
Crawls your site and collects your Javascript errors. To use it, give your page list into page-list.txt.

To use it without chrome window show, add following code : 

    chrome_options.add_argument("--start-maximized")

To use it page with requires authentication, enable following line : 

    chrome_options.add_argument("--user-data-dir={0}".format('path-to-your-chrome-profile'))

