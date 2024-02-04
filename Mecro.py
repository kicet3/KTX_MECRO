import time
import asyncio
import discord
from playwright.async_api import async_playwright
from datetime import datetime
from UserInfo import user,discordInfo
import certifi
import os

os.environ['SSL_CERT_FILE'] = certifi.where()


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

async def send_discord_message(channel_id, message):
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    if channel:  # 채널이 존재하는지 확인
        await channel.send(message)
    await client.close()
    
async def main():
    async with async_playwright() as p:  # 비동기 Playwright 사용
        year,month,day = user["wantDate"].split('-')
        findStartTime = user["findStartTime"]
        wantStartTimeHour = user["wantStartTime"].split(':')[0]
        wantEndTimeHour = user["wantEndTime"].split(':')[0]
        startStation = user["startStation"]
        destinationStation = user["destinationStation"]
        browser = await p.chromium.launch(headless=False, args=["--disable-popup-blocking"])
        context = await browser.new_context()
        page = await context.new_page()
        
        #로그인
        
        await page.goto('https://www.letskorail.com/korail/com/login.do')
        await page.wait_for_load_state('domcontentloaded')
        if(page.url == 'https://www.letskorail.com/korail/com/login.do'):
            await page.locator('input[title="휴대전화번호 로그인"]').click()
            await page.wait_for_selector('.login_phon')
            await page.locator('input[title="휴대전화 중간자리"]').fill(user["middlePhoneNumber"])
            await page.locator('input[title="휴대전화 끝자리"]').fill(user["lastPhoneNumber"])
            await page.locator('.login_phon').locator('input[title="8자리이상 영문 숫자 특수문자"]').fill(user["password"])
        
            await page.locator('.login_phon').locator('li.btn_login').locator('a').click()
            await page.wait_for_load_state('domcontentloaded')
            await page.wait_for_load_state('networkidle') 
        # 예약 내역 셋팅
        await page.goto("https://www.letskorail.com/ebizprd/prdMain.do")
        time.sleep(1)
        reservationSettingBox = page.locator('.tk_box')
        
        await reservationSettingBox.locator('input[title="출발역"]').fill(startStation)
        await reservationSettingBox.locator('input[title="도착역"]').fill(destinationStation)
        await reservationSettingBox.locator('input[title="출발일"]').input_value()
        await reservationSettingBox.locator('[alt="승차권예매"]').click()        
        #예약 일자 셋팅
        calendarSetting = page.locator('.ticket_box').locator('.part_rig')
        await calendarSetting.locator('input[title="KTX"]').click()
        reservation = True
        while(reservation):
            await asyncio.sleep(1.5)
            await calendarSetting.locator('select[title="출발일시 : 년도"]').select_option(year)
            await calendarSetting.locator('select[title="출발일시 : 월"]').select_option(month)
            await calendarSetting.locator('select[title="출발일시 : 일"]').select_option(day)
            await calendarSetting.locator('select[title="출발일시 : 시"]').select_option(findStartTime)
            await page.locator('[alt="조회하기"]').click()
            await page.wait_for_load_state('domcontentloaded')
            await page.wait_for_selector('#tableResult')
            table = page.locator('#tableResult')
            
            resultRow = await table.locator('tr').all()
            
            resultRowTd = [await row.locator('td').all() for row in resultRow]
            
            for td in resultRowTd:
                if(len(td) == 14):
                    nomalSeat =  td[5].locator('img[alt="예약하기"]')
                    standSeat =  td[7].locator('img[alt="예약하기"]')
                    reservationSeat = td[9].locator('img[alt="예약하기"]')
                    reservationTimeHour = (await td[2].inner_text()).split('\n')[1].split(':')[0]
                    if reservationTimeHour>=wantStartTimeHour and reservationTimeHour<wantEndTimeHour:
                        nowTime = datetime.now()
                        if(await nomalSeat.is_visible()):
                            td[5].locator('img[alt="예약하기"]').click()
                            await send_discord_message(int(discordInfo["channelId"]), '현재 시간'+ nowTime.strftime("%Y-%m-%d %H:%M:%S")+ (await td[2].inner_text()).replace('\n',' ')+' 출발 예매 완료 \n결제를 진행해주세요')
                            print("예약완료")
                            reservation = False
                            break
                        elif(await standSeat.is_visible()):
                            td[7].locator('img[alt="예약하기"]').click()
                            await send_discord_message(int(discordInfo["channelId"]), '현재 시간'+ nowTime.strftime("%Y-%m-%d %H:%M:%S")+ (await td[2].inner_text()).replace('\n',' ')+' 출발 예매 완료 \n결제를 진행해주세요')
                            print("예약완료")
                            reservation = False
                            break
                        elif(await reservationSeat.is_visible()):
                            td[9].locator('img[alt="예약하기"]').click()
                            await send_discord_message(int(discordInfo["channelId"]), '현재 시간'+ nowTime.strftime("%Y-%m-%d %H:%M:%S")+ (await td[2].inner_text()).replace('\n',' ')+' 출발 예매 완료 \n결제를 진행해주세요')
                            print("예약완료")
                            reservation = False
                            break
            # Close browser
        await browser.close()
    

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await main()  # Discord 클라이언트가 준비되면 비동기 작업 실행

if __name__ == "__main__":
    client.run(discordInfo["token"])
    
    