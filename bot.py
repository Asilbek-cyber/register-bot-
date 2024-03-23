import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import Form
import re 


ADMIN = 6214256605 

TOKEN = "6951152230:AAH51Or0Sp_2R3CVaI7Y7RlvsJsY1STgFIY" 
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    await state.set_state(Form.first_name)
    full_name = message.from_user.full_name
    text = f"Assalomu alaykum,{full_name} Sifat botiga hush kelibsiz\nRo'yhatdan o'tish uchun ismingizni kiriting!"
    await message.reply(text=text)

@dp.message(Form.first_name)
async def get_first_name(message:Message,state:FSMContext):
    pattern = "^[a-z0-9_-]{3,15}$";
    if re.match(pattern,message.text): 
     first_name = message.text
     await state.update_data(first_name=first_name)

     await state.set_state(Form.last_name)
     text = f"Familyangizni kiriting!"
     await message.reply(text=text)
    
    else:
        await message.reply(text="Ismingizni noto'g'ri kiritdingiz")
@dp.message(Form.last_name)
async def get_last_name(message:Message,state:FSMContext):
    pattern = "^[a-z0-9_-]{3,15}$"
    if re.match(pattern,message.text): 
     last_name = message.text
     await state.update_data(last_name=last_name)

     await state.set_state(Form.email)
     text = f"Emailingizni kiriting!"
     await message.reply(text=text) 
    
    else:
        await message.reply(text="Familiyangizni noto'g'ri kiritdingiz")

@dp.message(Form.email)
async def get_email(message:Message,state:FSMContext):
    pattern = "[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"
    if re.match(pattern,message.text):

        email = message.text
        await state.update_data(email=email)

        await state.set_state(Form.photo)
        text = f"Rasmingizni yuboring!"
        await message.reply(text=text)
    
    else:
        await message.reply(text="Emailingizni noto'g'ri kiritdingiz")

@dp.message(Form.photo,F.photo)
async def get_photo(message:Message,state:FSMContext):
    photo = message.photo[-1].file_id 
    await state.update_data(photo=photo)
    await state.set_state(Form.phone_number)
    text = f"Telefon nomeringizni kiriting!"
    await message.reply(text=text)

@dp.message(Form.photo)
async def not_get_photo(message:Message,state:FSMContext):
    text = f"Iltimos rasm yuboring!"
    await message.reply(text=text)




@dp.message(Form.phone_number)
async def get_phone_number(message:Message,state:FSMContext):
    pattern = "^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    if re.match(pattern,message.text):

        phone_number = message.text
        await state.update_data(phone_number=phone_number)

        await state.set_state(Form.planet)
        text = f" Vazningizni kiriting!"
        await message.reply(text=text)
    
    else:
        await message.reply(text="telefon nomeringizni noto'g'ri kiritdingiz")



@dp.message(Form.planet)
async def get_planet(message:Message,state:FSMContext):
        planet = message.text
        await state.update_data(planet=planet)

        await state.set_state(Form.city)
        text = f"shaxringizni nomini kiriting!"
        await message.reply(text=text)

@dp.message(Form.planet)
async def not_get_planet(message:Message,state:FSMContext):
    text = f"Vazningizni kiriting!"
    await message.reply(text=text)        


@dp.message(Form.city)
async def get_city(message:Message,state:FSMContext):

        city = message.text
        await state.update_data(city=city)

        await state.set_state(Form.country)
        text = f"Mamalakatingizni kiriting!"
        await message.reply(text=text)


@dp.message(Form.city)
async def not_get_city(message:Message,state:FSMContext):
    text = f"Iltimos shahringizni nomini kiriting!"
    await message.reply(text=text)

@dp.message(Form.country)
async def get_country(message:Message,state:FSMContext):

        country = message.text
        await state.update_data(country=country)

        await state.set_state(Form.house_number)
        text = f"uyingiz raqamini kiriting kiriting!"
        await message.reply(text=text)

@dp.message(Form.country)
async def not_get_country(message:Message,state:FSMContext):
    text = f"Viloyatingizni kiriting!"
    await message.reply(text=text)      




@dp.message(Form.house_number)
async def not_get_house_number(message:Message,state:FSMContext):
    text = f"Yoqtirgan raqam kiriting!"
    await message.reply(text=text) 
    

    address = message.text
    await state.update_data(address=address)
    await bot.send_photo(ADMIN,photo=my_photo,caption=text)
    print(first_name,last_name,phone_number,address,)
    

    await state.clear()
    text = f"Siz muvaffaqiyatli tarzda ro'yhatdan o'tdingiz🎉"
    await message.reply(text=text)
         

      



    




    data = await state.get_data()    
    my_photo = data.get("photo") 
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    address = data.get("address")
    email = data.get("email")
    photo = data.get("photo")
    country = data.get("country")
    city = data.get("city")
    planet = data.get("city")
    house_number = data.get("house_number")

    text = f"<b>Ariza</b>\nIsmi: {first_name}\nFamilyasi: {last_name}\nTel: {phone_number}\nManzil: {address}\nGmail: {email}\nMamalakat: {country}\nShahar: {city}\nSayyora: {planet}\nUy raqami: {house_number}"
    
    




async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())