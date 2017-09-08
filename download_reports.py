import pdb
import os
import csv
import django
import requests
import datetime

from os import sys, path
from selenium import webdriver
from StringIO import StringIO

sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbsw.settings")
django.setup()

from general.models import *

def get_reports():
    # pdb.set_trace()
    try:
        driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true',
                                                   '--ssl-protocol=any',
                                                   '--load-images=false'],
                                     executable_path='/usr/local/bin/phantomjs')
        driver.set_window_size(1850, 1000)
        url = 'https://app.appeagle.com/login?redirect=upload.aspx%3f'
        driver.get(url)
        # driver.save_screenshot("login.png")

        email = driver.find_element_by_id("blankMasterContent_emailTextBox")
        passwd = driver.find_element_by_id("blankMasterContent_passwordTextBox")
        login = driver.find_element_by_id("blankMasterContent_loginButton")

        email.send_keys("premiumupgrades@gmail.com")
        passwd.send_keys('@PPeag1epaSS')
        login.click()
        # driver.save_screenshot("disabled.png")    

        cookies = driver.get_cookies()
        cookie = '; '.join(['{}={}'.format(item['name'], item['value']) for item in cookies])
        driver.close()

        url = 'https://app.appeagle.com/reports'
        header = {
            'Cookie': cookie,
            'Origin': 'https://app.appeagle.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://app.appeagle.com/reports',
            'Connection': 'keep-alive'
        }

        body = "__EVENTTARGET=ctl00%24ctl00%24ContentPlaceHolder1%24InsightContentPlaceholder%24QuickReportListGV%24ctl02%24SecondaryQuickReportDownloadLink&__EVENTARGUMENT=&__VIEWSTATEFIELDCOUNT=3&__VIEWSTATE=VRyNOd3phQEru6lS1LA91%2FP2M%2F37ElhpAMjpr%2FZsXPMWXXw7L81x1zuTHo8gHtH6LwY7A625DYR5nHzv5C3%2B9kINlntfGqpNYty8zAJD%2FM6Zmt2zJfCbN4687rfeFeLiNChaSDE7TT07v7Y9rqrXdZxfeSj0kWTQpuYlrQ0D4DzTfJQSwIUMvpoCE5tPuW1U5EEeFNX8q0teAKc2Oj8MVl4KA6d%2BiWHK7wq0siplF2QbuQyJFkeQ77KdOu5hubCqIZD1JQzRu6AN%2B%2F1ys%2BuHc2xU5EvGemxQp66pMyd7OAka1W5BvRWCdn%2FrDBaoEVY1tPdsBOOKVSUuZvwidaoeNzBwTLcKeRb2NeO65JXUmHmgvRWt16nidDS3CXEEtCaNygI4knJA69Up%2BwRQGgzrsnrAqWFle%2Bg%2FruiyNH3%2BM1h2cuu08aUy53lywIAstT1KiI366sinvM3Mayd9vp3yfwB%2BlGpaFsJTyO0IyypYgiHla263hadSeM2Xv%2Bc0e%2Fu2o0lxIPP5irPGSHiNkp7c8SK6%2Bu%2B7Cs6CxzXQM%2FkQaig%2FSXeEROx7BpvMjVK4rhN6s29c1gpflAoWliHytp%2BqFD6leH%2FZojqvzOJh8%2F5jATGcbATavIx4mBupICHMdoiDG6oSwJ8VvHAgwsHmKEQ7Un9IgVQh%2Bx7KE0x1%2FKDo%2B5deLjSgahK0neYFSwH%2BXimo3r8ouftrNr%2Fi1XWBDYa%2BbZ1Csh%2F4RxOKy%2FKC%2FLMpB53blKrZxrYUD1kvn6P6BqgXvSaQ9FJD9GNm5qMVspUpuBP8sya%2BtXRCWlwW0Q3k9h31DfYZimktHxvF9vjfXBhGS6kiux1AZpi%2BsLOBaSJN7LoePeB0cQNfPrYWSmicb652giZ1m1XM8nwy3T9wcY0WpvLKqnQX28bhJu58sJi94fXU0IR%2B3GhKC7bWopR%2FAn57%2Fr4tHkGKdl70%2FQQz9w20hSmXksIY%2BKdOLB2j7sGRimRbHJaG%2BRQFsSA4%2BZOfMJUU%2FsKdF9j1graZmWTjVwPAAapsj8BgAhXVQb6CrZtFtyGqvPnvvmvjJoxoYfimjdG9W3sB7XbWExb%2FiuWWLEiXbqqH71witWXyx8ltT%2BNfFR9zSzYJ07Ov0GiOerhLij0rzr3%2FFx%2BWfHSPoJdMMFLHbv1Cbhk8OGdAJW6gxZ3d0brWUcU851a0PYbn8TdGQyVNgt3DlWoOVcdhpAyosRvwEuWqhknoVwyENC9X74ygmhuNEYucpphBhSXDIle%2F2PmfZj5O3NNX%2F6BYaQqmPaMKytllrIzZcccrJ6WIJzZvv%2FNACewm%2BGzaS%2BWGmvXtZK%2F0Vg1tt0Ye2qoX7WY6f5t6Z1EZqNsC21NjCDVuNcmPBXb%2BNI5VbO7EKD17b0OPmeGz73pJ%2BJK9QYQanLjiiN8XXY6ODnQPiT5%2BaCrSEgfPEBHVgG%2FYD91vkk8M4sTgOiU70LykCIwFzQw6Q%2FmyY1TOoyz2sWBZnKanrDmoyywt0edc%2B3imgFl9DIbWd1KvhOUBO5RyW%2FxjGwO%2FZg2VwLiA2h4mrqFTxL7R73Xv%2BQngcJRMubsy6pReuYTrNP9pjDqUgI9Fqu%2BdZCvqYuogdbrPMCtqZV61adkBgN6SorWgIMuqt3UHTlitVf92p8BomcklsydNWR5r%2BZFtUT4yfiuCiYc%2Fhj8XdTA2X3sBmAi6LKa3hHTmf%2BGIJaz2SIgqiSv972ZTgZmHE22F7hfp18BgaxmXczcmMV%2FZ18Bsxo5zsM1LrMcLZEtSvpfOoy3lKUO1DNWiOEIKUjGXrKOQCYVAsLd6P%2FPd%2BID6H0SeJtYztmrTCbwnMCkbZEW%2FpC2tFU3yAxo3kZZqZp6RcyQl0BOz0GW3JMoQJ7m8jR77Sz3ESYbd9WWMUdIiYjKzwrgIb4likL3%2BN3GzdSwdk90KRtZIPQdQ4jf9m7K9kW4IB2mz01GiH69eDiukfX7KKbpiQ6V5WTgiZPosRwpFvtZ0afUf%2FQ8tdSuFWKl5OLXI0uikETpmvqndhTN7NcmucY23CGqMgx5Yz7rIC4559mUD8LG1mXTgIYOHP43A%2FhGVAWinqid5cpifzYqZZ%2FiaqRmR33ZJ%2FVFz1eM341gdSr4lGsxAkyFM4KS0q4GawOhL8Sg%2B4hx2Hx26oFI2jQlNc2mExLYJx4DAMeBcBsCmQBPBujaiTIcHpVUX8AyZiHAxqD2x23BY9CVsX2QGSRINl02UCSDVAKXYbX7OBsgIee82eqTBW4f5uVQZ4ttYmMWRAfGUQrAZOKQD6kodKmhVSbK2jPFLW2yItxBUmZMbkB00VZrLhrGoCBYGx27iMucnJob3o8R72MvOyrYhl%2BlnO43aX2nnC6Q3EiourzPiQRG3ikaUhPAkhmK%2BSZ8YVf1CFWcl%2FoLuINkRG%2FAdbhGynfMrn19xE%2Bv9P1ri0EF7tsWIbmhTBdztdAqa3sdpsbQRN90yIpfuMBMLwVcgxxFdZ8keEDtzUKE3C%2B3EQ9bhKHQXKctxnOF78lCaQRIJ3%2FuEOZnEMFCPodHt%2FFjrFxaroBfCGRdKEMPjYRCRUBnprhHlCW%2FoBTdbbMsZJkzoiBlPe2wurko3m6TS7%2FSf1DPibbAoEU6VZcg6T6p31yUx3fyd%2B9MZySIlnnxTKP6VlfT4mPMBNKsQcD4h%2BX4MphjTnZpCpF8Pjg4BWgErIhDEmURRGOuOm1x3aHnigQi0mRCR8jMgGxmHPl%2Fszf0cpXCu26OgdGfJPiOrRUdk63upQUNsW8sgOcCjy1PntsOSz9ICiAtw5KyhZ33%2B08FJi1ogW1JBkF4G4GqVH4FfAa8pZK%2BmH5uN9b1OCUCJ%2B%2BDrBQ4TBGjFfBE04aFT2YsA9JNjPP3rMb%2FkRZZiTGBTsN364%2FYw9IHgcRJwZTRLfsc9lzFswZlmkcOLx4AYmndCqwARCvPtZV6YXzFt6BJSEuYn4zGFh2kIF1NAZglnhdDgWc7cCTO11mNc5XyA7urVFDhdRQhlwDgB1B0sov5H2ZMUUon5L0proZ9SseZyIJl%2BPxed1o90LXuavD36mRGXHa3Wd28PAeUGLgLxL32x%2FW0YGEAeuVluXnLC%2Fplo9csznbIuRU6rU858er4SW0dLz3Orrc5MzoQDktk33T5nEBqrnT6xq8dZdbTWuosQEIkAElNR2rhE95T94DGIRkHsqqEUKH5xSoGX5mpFL33ntwfFaLoegeQd%2Blg8lpQGMz6fycpckA58%2BhJPIGFBZ1LDkwiYubHWAHBjp2YbWeoC%2B35BezVA6%2B0YvKsuVLKvi2s7ncr837yV28xGC8LiXOn7rqKjF4qjxCBWV1pomCIXNYel67mpIan4mzeW%2FzYWkNgvFOOlaayP5Mxm%2BaxXvHzWhp7ZciU%2FftQjNWPa6BHYTNORAnFkUYSwRJqO1a6gRlusd1trQ8JST46p8oAZvS8N5hKH%2BYRWTPnY9fLLjaNzrq%2B%2FCI0WGCLWdRT8GtHyOA%2BXKRxKM8SR8QAaFn5sGJgWu0MecZbY%2FFu5QGHmOOjGVA%2BpIM%2FKiZuDhu5A2YcBm%2BQsEPIr%2FpX7m8Svy60dThCffERalN29%2FbGxqODn4B6EitTjJ94LFXFg3DDfuXaLrRfylllJorN0oMLRNqnZBIcGQCoRgP6RWceb3cVTP4QkHEGSeuHHX4H3Rs1k61ZGRoVxJngF%2F9xYZA8KGcW0ixOIR%2FORYNO1ay3jcSxkK5EuAaLV0PDfC5ltHVFopWzOGZThRP%2FUXtaGIK8WYLta%2BuX%2B8iLqJit%2Bv8WS0K8MqbACxTyg6tK%2FfC1lqZxZhqBpSGqPIQaqYhFstunxaLzo987nQuVpdwQXLBWEusvO%2FgOZuUuMEriP%2FD8vAWDLvxmBu8OF8A5BECSjwFMEwpuO8tZOIxEPzPgh%2B1SJhiOTFQXHO0NRRCE05FJcQ9BozmKGcHqdzIJIuZghbrbb5sLiwLqednW6KkTK2IgOBxyeX0oXciNumHxyyfdsQjoAMNpS6q3ZJ1QCIOTta22JynkfFR7O&__VIEWSTATE1=jGX%2BLDp8F5GoKjX2bg5SZjIqOOGP9p%2BINANvBWGvJa2UlvfSrJd%2Fd8BGb1IvsAwwy71q8x2hcjHNnitFzpydYl%2FU2PJEiwTqbSe9xuuXdMSrd6m%2BcVG1Jc5Caf2nNufv6RPS%2F7dhyXX5lAq1FIrn16TcW6%2BPw6aSW7yz8xYO4PWl8OPzyDur4a3UtRdAn2Bpj488zpFFfwCPNAH%2Fr7XDV%2FA%2BHF2P3MB2He0zSimB7bKFt68Z7hYo%2FA2NhrsLB1EhcRfkKd0623UOQTKj6lXVAiCGyJ1uzgrpHG0XQXVQqu0PszhDujqZGR9ux%2F9ZC4EbJ0jU8Ynzqd1vm5IwHE9W%2BFE2ZGyPQvP7talx%2BGTgMRf2gvJf6394OQUIZ1mgvW%2F%2Fta7lRgRvydJdKdYRsZNNJuYvSeeC4LDiUOQc3c%2FB%2FDlZ%2BqdIRGoyz0EpRTmEfciXekLWeHe2ZChJYaqwswIP87jxzAwKm0tlXoL8Xgn4ggaUBpCpdorrwQHLmq%2FddcwivK1MpZssqtxQ%2FIsaMm%2BhZc0ubrVX3oBfWJ2RnmaEoQ7ejCylHdXIIzO8%2B0vqLjRU8Fz2g3wpwjPZrrblslN7gsJYXNeoGf2%2FonUO2%2BKA2pMVr6W5qp856FyIEl3uXgohUX86LB02W2%2FdfZc0IXFVqkyqyxnnZF13bOvRcVaNEQ9d3DFjIIhr2S%2B0JMKWl5cfY0zY9GlvyKANusG2puOJrunVkHmGIdkHe5JHMkcGimz%2FuVflq0JQhprofCMR3jPnyaiRjLLysAIEhQpoHy8RBKeR9IHX0hrqJUn5Hkt0%2Bg5F0lLBHtsmAxCmNDXrAkM9O8%2B2GNVbJX1LxG%2FkDBki3GhoL%2BasEWE3V1v6e0J1VVzT7USPGyGWdf0r2Wwasyr9VyeMenMqOahHAFjFZkc%2Bmyi7%2B6dOTdcMRYTiuPJzA5VmBy3Glj1T8rqBhu3tRSCLp7NLSkzN8nHg6b%2B8L4l%2BYvg4XR4puOcTIxucOx2mN%2BpZi1uUyTNRSuC7SpildAMaZqKTwFL8SGn%2Fg9qJCvMM1xbkrPgeqVsVx4vzRtgyD05NN4JvEzBW6F%2FF%2Bqu1UEcg2utnpS0HSRs5kwtpCY48e1FOYQamW84%2BctWMSPq%2BboFvOg9uuQgzf7%2BO%2F8nm49wpDMqoB9S0t%2F8YGwIwb9BxjjAELdGGiNcsHrZH0fCDUCu%2F1BrOqYFkrhIQuXShi5UYoRyan%2BsCqGadI6qWj7lDXV1atQu2WCjaxV7BrPPAvzX1UckzmdrIT6VbXD5FqiLeY%2Fgl6Qvdbcuf5mZ6gtjzyVSOJVv7wBHeZGaG7%2FTdBTgZm1pFX%2F1%2BKkaRxQ6uXFeOEpauFyxTr9%2FvaL5UKCVWN%2FtOyc%2Buh%2BaYDloga91D3XuM07ZWKxH%2BtUtR5fiCqf9C5h4M%2B7ju4LdMlm1hCsRMiuaalu3PxsK%2FrX7jAnCkSgTEo0X8q5qIKOtXOk0qQlxsOnUzzkCgWdQAbthaRt9LPmCPTPXxgam%2FgG6Y7lh%2FVx8Nstz9kT3NjivjTWqDe%2BavqxeuGf03DiVrlh4C2mjmJ7CXP7tZOy7iqdZGSIaMW%2BoHIX0wNrUx8Ex7vcse0X2kamj93l9tfYhQdZSToHbuiTqZ3m5b0PBEvLL6EFT65UYTHscw0y0wy8goMlGB27EUDLlj5VbYG8yePqD4MI8EapaUSb65LkkuZxAAlkdrN2IxxRQ5fgSXyNx6x2mody7muoCH1ZIF4q8fbR8fjbF%2B%2BTV%2BT%2BE7y3dLyZLcrSSt9pztRv4fu7YtVXQGfyYe3mPXZ%2FkG%2FSWnNoheUz9SHgQc1RMEqnGJckF4kuK86UoA9vqmYAHG1G3JfyWZVT2iH3eX6I%2BZ29Iovwq%2F1vHqgEvXmy4qmZe3X9P0DU8TqXrrjPr3dUPqPqZmj5%2FS5U1PhV29UM%2FhA27RWsjfS%2FtbVJVs0uKbfazqwK6Qiu3sS8gCUUD4rP6EweHg715JKnByk%2BieKLfVQiDYKA%2B2HFDHCaCThs5MHGs%2BnhRC6nvETolKBARrUl5r9saRQK59%2FBZT2XayHO5jaOJrRL5s39q9obHNSIivXBa36IMJAosmABvbDqAPUQuAd%2Bj2bocDD5S0Sh%2Bn4OstXeHSEurCN4AVmxFgx%2FSO6eNXwL7h%2BIeukk4UhxqlrxChLqNzdKTZAsJpBe4mzUfHpiBHsrIOWCE1PU4%2FxFYlSRrQvhthM6sWy0OTBlD8A4zUbaP31q8yEYAgrX%2Bi2UF70oJqm9T%2FqaU8hzwF4QlUeft9TkGxwLFXdCavF1CYBBNRTrPmuV1n53drQAIzbnXEIXaeNhl1LT6yEYktM4jMWrCoJyaw%2BHaCih0TF9JGBj0nShJm0OM%2Br1jMeJE1WlQxRWZcHnfMjNWqDAa1y4P6DQh6mnhcLXD2FTF0qkBnLGnwLd8pOGNc%2BilmUBm5ZjgSBjRaYo35I53wTByliJPWHhs4sX%2BY8%2F8KAYs5QHC4hkgW26xk1eAgyQB%2BKCVw1w102meaNzYigrgYNKqLOc2EgNctQExCjplTMdGul7RpdW6w6GKDKhD72%2FPv6pUj8NxFWh4zYE3oA3fHvNKBhHmWGMsuzVz94JLGRUvXLa3MLoWqICE4REIz4%2BmPaY%2BsEGppkf6ETsqPAZ6N0hob0F90uDT4%2F3aG%2F8yBXW4m%2Fj6XlM6v%2BlFdtUwdtDw%2BmC6dC3180TxCxPw2DRjblBAUFnuWF2Dxdwmc8yvksoJdQupm1s3Uh8zyUT3MvPY%2BZg73zo8MdyiOmNLYaJcyHWwa5PdVguj4iACOgQs2HJaHgH7QL07jB1A5PB3rfL4IBIZTaLbkLDDMlaSCFnvysbsl8beIqpqDMHzzS6nDLcaHJC8nP8yYIZ9NorrbIVwDzsHq%2FnUNloMHvvqfVOF8Ac23Y6drGDTeieHQ%2FgvyVfOEe35FIfZ2aCZmq6Io5GkwuSlo7KW2Cn7FSiIxQE6U7T3Y%2FAGdG%2BAiKlZJBYXRL5iFBlqmfVAXahF30EPncblO%2FlEEQXnQMJdkkDG7sBgInT91vBL%2FYaoNCe2VJ%2BB2tB3XxiCJnZSeG13ZGI1rVof1EmiiFlSzzFcayPZxxHXbWu66%2BFueL327mtIgdwdDKXFFkehxI5hdV75oa712AkWKxE5otHANZG5hR6fXqbeYdmm7%2Fq2KHVgqUYH75fQpk6Qzezr567xBhoLQKhDpa5eNySEPTNnsgngSbTVKMoYqLPiD4OjwBQ2y8T1YxZuH38Iook4kaJ%2F17AtggaMHzsLNEukIFL81j%2BKzu4ctTidnqjOkm4XlfcXeEiSUpALvcw1sBOBEj%2F057N%2F3q8xaFvJ3hr14wcxgeAJUvSqT2GyZ0bbBCkdPpgzDEnFXYmoRAw8riyDVvplBaL3gicr6hmQaRrQY2uqmZYaUaCmi%2Bo8SLGE4NBHdafpccG%2Fa22rztj6Ww4VnGQyV0P0rZGLudlBnsc7DoSe3txCEx4%2Fwc25r4H2vhD32FOXfTil8pR27m%2FBvQ6B9xpPuhrM0R6JGRbfe4uACKYjLe%2FwyrEMRcM06BkQq7q9n6YhYIrZw08k%2FnZiAbULRbKp2JJXWZ%2FZzZirvKHPmL3meapKIFZ7xbuV99z6WMg2dH8cW1a64ZFTF3SXu%2BPl0EqxZSxEC7Zbq8goAovqksiFbetwxKexQUG1b4I2yPTPtSVIfSuYaeOOa3xRg%2FerLCyEBEkWPbii26JVtkDCsbH5yWI4X325W%2BaOmpoPX6uBzIFiUNZr9yfzvMqnyCFhLhvNd1b46zt4VVD6XCwHiOreRsC4Ud0TWXuzRdH7ZvBkj8pq5nUDQJTvreEnjdbwUZSmMiY5khVAfJzHfqQ2QnQ9tr2J2BCiZ27%2B97cUqDRvZJaLqbu9XcGqUl4Luo4rZ3ua9q0Bs8xxHqCd9UnoXu%2Fth1jcUaPGsDVVVbpIv3YZUN50QnNU3K52US4%2FyZe7JvHHHyBQ8UeEVgOlbUs4DcR1pGexGdlLGVaQesM5SzlhP4fCtpK53&__VIEWSTATE2=W6NXxwk6oA0i24TZrO0q24xWatYwrrky1D%2FgU48d5bvJPIzVpSmdvitGGjxAZIl0DE58QqVfu%2FuteLqu3i2sV8rFAWzUMmyT5xlNkDFaHOEXDMlSNQijM46UXBlz%2F21jeL6WIONrgycgy%2BN8jttAa7fw4EIdE9i0K5lbLDDoGgSubLXk1pgoKY8zTR7XMKCaUDxGzv2MIylkPi5Pj3cHqrKjvUdVLvwlHu%2BMLKiYKMez2K%2BCo6h9mjborWip26D4NIyaXYAYmHp7Y6xy%2B7LqYy0MRuyPQQvnJGIdpeyhP06SVQbYMf9gUqT0r7YN0NlcJ0jfuqC5wItd%2BF3m7RS1Gtzl7PNHQg3iU4FvPZpzLh6C0CHHayK3ZDNowsRDsbuDrBBC75YczyKObv5NvSBjjLE%2FpaOVGOVWWCkjY5l6eJfpvNCgRNDnTLpnWp7QxTRhQeHntU3ro6DxVj0FrmUJc3YD96ipmWvdbouAZtIWbGj%2BiLP%2F%2Bzwdhlhpn0WOow8q4IBL1W1g7ZdrddcT%2FDO2Ne%2F7zjfO7ZGSxyXobJxWTH5rM6fOGMyLyBUwhjSk3v19U3QKfsekm5y8c89XO%2Bab7roOK4vkNRPKzhvl0yGH4m6z1ToaK5n3c%2Bf42vbr89Whebfl1uFyw5kJKGhYNg%2FGVzZtO5S8z4IUM5rjQjYb6xUTLVFwmfH9fWi1smrQfO0IjU14pjPzta88NYVnPNWyg5ZEcOLCtBMwmrKtBzB11iXx%2BGL%2F9cHoVDdF4GvcMt%2BQjCesj%2FoMOJiWk0UBUzET1zPilHZOXi7FjvojJg9AiKjXOJ%2BF5Tj9olZqzMCfQVvg2DuGH87YlesrlAOYxm8LQczEVMJna23nMcpjgkO6MiO%2FUfkKOpZSBOow0MnCvx4xBwXBq1qRwULjFukDZasUzpMEyiWOddb56jKpbSW%2FzVzHYwBFWGjP4xn7MwU7ZxOBz5OEsvwL9Pl6BzSbcF8e1T3bU3YPWuoo1MTmnkrJKYY56t9MAzkd9fVMsD8CZEuJ%2BYnA3qtDVql6RAE0%2BoA7ODSjyvwE%2FVUOgS7U%2FwmTegWkGtrv4TnYooffeHVbpDybHUZJjOCkGGXVV0CQKFF4yL4EJT%2FlElyg2A%2BS5K9CQ3c%2FtwgSEFwSdlBFJtsHmKGPfwlTZxe37xyzdRTL8%2FFFclVbNpswCB14jgqGoewk%2BH4q7DvcCuHFLq8B%2Fw3%2Fo4PIf7d9KCdTkH5PiWUwJwpEgBmWfgM%3D&__VIEWSTATEGENERATOR=ACDEA523&__EVENTVALIDATION=eC1POnOuvrbe9DPnt6rlYgoPiA0JIPL82Q0c2Vp4FiSYWY%2FBAykFGpHWYcR0CnN%2BKd0osRZGgBeUmm2TYSgh69CXmlM0wBCBPu9oLrS0kHzog%2FhW8aw1ouEiq8wVlS8S8Y%2FbUSpPZFIH5NZQHoVVJHQ4l6XMrR%2F4tnJ1b3CsV7DJRFGgIy%2FK0O2DjbQlpgmq0FjM%2BCBeko%2F%2F5j4auUhSzKL%2BfmzA3MeHUOMwHP8hRzbQ1x3%2BbThb0c0%2F5QaMSDp6%2B%2BWQS%2B022R1xg5dzvluAGgLbes2b1ugraJTAq37cbFAa6q19PwTMznNygEGSylSh5jnMs%2BDoGrHOYvXsv7e4hGV3LK%2BFXNydgAyoGVtXQXWqQOIuWtN0MIr9ThmP6ECJen%2FbleUO1XmuAqRHY48rXdULJhucjIJMvE6t22OyZ7V45os1owuWQCdVCtRZ5XeCmqBmTcZhhKa5QQ62trzQgQS%2FqLhuSTB8Hg3a8BYFkv307J%2FrpsyjyOK%2FY3uKFoZXylAItWVMe%2FExHiu2AkSytTKeM1ZX2%2BIodWKUvoAYb%2B8CL5ldctscYj4qEF7%2BCWebiw%2F4decT9l9zLBfbJGMfzIXmdvKhpEIInPqKad%2Fit1KDZJD1pGnPwbpNVt%2BkSCnatPRxc%2F%2FnXmbUfmQoS81kTXIHURil7rO43W5PO6LSXPAF%2BI1x&ctl00%24ctl00%24verticalNavControl%24searchControl%24menuSearchTextBox=&ctl00%24ctl00%24ContentPlaceHolder1%24LanguageISO=&formulaName=&formulaId=&formulaOutputType=&hidden_validateFormulaBasePriceDD=&hidden_validateCountParameters=0&vFixedNumberBase=0&hidden_FormulaUserParametersDD=&vFixedNumber=0&vFixedPercent=0&ctl00%24ctl00%24UserIDHidden=9904&ctl00%24ctl00%24FullNameHidden=Appeagle.Webapp.reports&ctl00%24ctl00%24LanguageISO=en-US&ctl00%24ctl00%24MarketplaceTypeHdn=0"

        lthtbb = requests.post(url=url, headers=header, data=body).text

        url = "https://app.appeagle.com/upload"

        body = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTTARGET\"\r\n\r\nctl00$ContentPlaceHolder1$ctl02\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTARGUMENT\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATEFIELDCOUNT\"\r\n\r\n5\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE\"\r\n\r\n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\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE1\"\r\n\r\n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\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE2\"\r\n\r\n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\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE3\"\r\n\r\n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\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATE4\"\r\n\r\n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\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__VIEWSTATEGENERATOR\"\r\n\r\n69164837\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"__EVENTVALIDATION\"\r\n\r\nJL1TCS6BhFcr5qfyxEtBLiptaQIazzrwrG3fwPPBr+H2AexlYLuLzMzeORW7y3lTYpb5uNjurxDNv3rXR5KyGnd1ijy4tCn3M2wp11AA5oujDKeE0AqD00n7JDSoD8u+NXh15Dof27PDqoMLFukamIlB0k1bcugXcYa/wdbZ+WsU48+SPXtc/Y7zg3fmQSHdj6UyLZBv/8TKEGZM8OPDJSN7rJJRdWuVjp42cav5VQzbkfXF7CwwKyQsn91v9FBM7zFM1ZmGWxdylHa2d5h5NJzsQFW0bhTY9ib+XUsVIS5uBiKcdRVFmLWj9Js8XNWrylOKtvzW4sny0XafRs1URgtI6qa6GBawPGWoiVbLYu4csTu/898uTQNHi2ZWMAuK8sdnUlq44aUjvCpRcaMt2qcEqKmx0CNrPu6aGsD6wKgswcsLAmB5fDXjgNIIhecls7JwjA==\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$verticalNavControl$searchControl$menuSearchTextBox\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$ContentPlaceHolder1$hidden_pageNumber\"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"formulaName\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"formulaId\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"formulaOutputType\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hidden_validateFormulaBasePriceDD\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hidden_validateCountParameters\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"vFixedNumberBase\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"hidden_FormulaUserParametersDD\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"vFixedNumber\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"vFixedPercent\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$UserIDHidden\"\r\n\r\n9904\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$FullNameHidden\"\r\n\r\nAppeagle.Webapp.app_uploads\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$LanguageISO\"\r\n\r\nen-US\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$MarketplaceTypeHdn\"\r\n\r\n0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"ctl00$ContentPlaceHolder1$summaryUpload\"\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        header['Content-Type'] = 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
        header['referer'] = "https://app.appeagle.com/upload"

        aaf = requests.request("POST", url, data=body, headers=header).text

        lthtbb='\n'.join(lthtbb.split('\n')[2:-1])
        lthtbb = csv.DictReader(StringIO(lthtbb))
        lthtbb = [row for row in lthtbb]
        
        aaf = csv.DictReader(StringIO(aaf))
        aaf = [row for row in aaf]

        with open('/root/30DR', 'r') as f:
            dr30 = csv.DictReader(f, delimiter='\t')
            dr30 = [row for row in dr30]

        return lthtbb, aaf, dr30
    except Exception, e:
        # with open('LTHTBB', 'r') as f:
        #     lthtbb = f.read()

        # with open('AAF', 'r') as f:
        #     aaf = f.read()
        path = '123123'
        with open(path, 'w') as f:
            f.write(str(e))
        # pdb.set_trace()
        return [], [], []


def manipulate_reports():
    lthtbb, aaf, dr30 = get_reports()
    print len(lthtbb), len(aaf), len(dr30)

    products = {}

    for item in lthtbb:
        if item['SKU'].startswith('C_'):
            product = {}        
            product['sku'] = item['SKU']
            product['asin'] = item['ItemID']
            product['title'] = item['Title']
            product['bb_status'] = True
            product['bb_price'] = item['Buy Box Price']
            product['num_orders'] = 0

            products[product['asin']] = product

    for item in aaf:
        if item['SKU'].startswith('C_'):        
            asin = item['ITEM_ID'].replace("'", '').strip()
            if asin in products:
                product = products[asin]            
                product['our_min_price'] = item['MIN_PRICE']
                product['appeagle_strategy'] = item['STRATEGY_ID']

                products[asin] = product

    for item in dr30:
        if item['SKU'].startswith('C_'):        
            if item['(Child) ASIN'] in products:
                product = products[item['(Child) ASIN']]                
                product['num_orders'] += int(item['Units Ordered'])

                products[item['(Child) ASIN']] = product

    return products

def store_reports():
    products = manipulate_reports()

    if products:
        Product.objects.all().update(bb_status=False)

        for key, val in products.items():
            val['updated_at'] = datetime.datetime.now()            
            Product.objects.update_or_create(asin=key, defaults=val)
            ProductHistory.objects.create(**val)

    print len(products)


if __name__ == '__main__':
    interval = Interval.objects.all()[0].interval * 60      # in minutes
    last_run = Product.objects.all().order_by('-updated_at')

    if last_run:
        last_run = last_run[0].updated_at.replace(tzinfo=None)
        passdue = (datetime.datetime.now() - last_run).seconds / 60
    else:
        passdue = interval

    # pdb.set_trace()    
    if interval <= passdue:
        store_reports()
