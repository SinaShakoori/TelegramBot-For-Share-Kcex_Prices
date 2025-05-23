from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as chromeService
from selenium.webdriver.common.by import By
import time 
from telegram.ext import Application , ContextTypes , CommandHandler
from telegram import Update
from config import id,TOKEN
import asyncio
import datetime

def get_prices():
    prices=[]
    try:
        Service = chromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=Service)
        driver.get("https://www.kcex.com/markets")
        time.sleep(10)
        for i in range(2,42):
            try:
                name = driver.find_element(By.XPATH,f"""//*[@id="__next"]/div[2]/div/div[2]/div[3]/div/div[{i}]/div[1]/div/div[3]/div/div[2]/span""")
                namen=name.text
                price = driver.find_element(By.XPATH,f"""//*[@id="__next"]/div[2]/div/div[2]/div[3]/div/div[{i}]/div[2]/span[1]""")
                pricen = price.text
                prices.append(f"{namen} : {pricen}")
            except:
                continue
       
    except:
        print("مشکل نت!")
    finally:
        driver.quit()
        return prices

async def sendmessage ( update : Update , context:ContextTypes.DEFAULT_TYPE) -> None :
    channel_id= f"@{id}"

    while True:
        prices=get_prices()
        current = datetime.datetime.now().strftime('%H:%M:%S')
        await context.bot.send_message(chat_id=channel_id,text="\n".join(prices)+"\n\n" + current)
        await update.message.reply_text("پیام ارسال شد !")
        await asyncio.sleep(300)
    


def main()-> None:
    application = Application.builder().token(f"{TOKEN}").build()

    application.add_handler(CommandHandler("send", sendmessage))
    application.run_polling()
    


if __name__ == "__main__":
    main()