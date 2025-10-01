import logging
import aiogram.utils.markdown as md
import psycopg2
import asyncio
from datetime import datetime
from typing import Optional
from random import randint
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardMarkup,InlineKeyboardButton, ParseMode
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = '5840255695:AAG-y-qUw-xl9Mr-zzQHyzzByQrqyOzqyNk'
DB_URI ="postgresql://postgres:EdEfBcABB6cedG5EGBf6616gEb44ACCa@monorail.proxy.rlwy.net:53816/railway"
    
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
  
db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()
   
#first keyboard
button1 =KeyboardButton('مين خابر 👀 ؟')
button2 = KeyboardButton('برسل سؤال 💬')
buttonNotifi = KeyboardButton('بفعل التنبيهات 🔔')
homeKB = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button2).add(button1).add(buttonNotifi)

#second keyboard
button3 = KeyboardButton('بصورة 🔗')
button4 = KeyboardButton('بدون صورة')
button5 = KeyboardButton('ارجع للبداية 🔙')
questionTypeKB = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button3).add(button4).add(button5)

#thitd keyboard
button6 = KeyboardButton('#بريدة')
button7 = KeyboardButton('#عنيزة')
button8 = KeyboardButton('#الرس')
button9 = KeyboardButton('#البكيرية')
button10 = KeyboardButton('#البدائع')
button11 = KeyboardButton('#القصيم')
cityKB = ReplyKeyboardMarkup(resize_keyboard=True, 
                                one_time_keyboard=True).add(button6).add(button7).add(button8).add(
  button9).add(button10).add(button11)

#fourth keyboard
categ1 = KeyboardButton('#مطاعم_ومقاهي')
categ2 = KeyboardButton('#تسوق_وترفيه')
categ3 = KeyboardButton('#صحة')
categ4 = KeyboardButton('#تعليم')
categ5 = KeyboardButton('#مواصلات')
categ6 = KeyboardButton('#استشارة')
categ7 = KeyboardButton('#عام')
categoryKB = ReplyKeyboardMarkup(resize_keyboard=True, 
                                one_time_keyboard=True).add(categ1).add(categ2).add(categ3).add(categ4).add(categ5).add(categ6).add(categ7)
#fifth & sixith keyboard
button12 = KeyboardButton('ألغي سؤالي❌، وارجع للبداية 🔙')
button13 = KeyboardButton('أرسل السؤال للقناة ✔️')
button14 = KeyboardButton('أرسل السؤال مع الصورة للقناة ✔️')
sendKB = ReplyKeyboardMarkup(resize_keyboard=True, 
                                one_time_keyboard=True).add(button12).add(button13)
sendPicKB = ReplyKeyboardMarkup(resize_keyboard=True, 
                                one_time_keyboard=True).add(button12).add(button14) 

class Form(StatesGroup):
    questionWO = State()  
    questionW = State()  
    photo = State()
    cityW = State() 
    cityWO = State()
    categoryWO = State()
    categoryW = State()
    send = State()   # this is to determine weather to send or cancel
  
#handle blocked users   
acl = (6273650093,1372349969, 5282286720, 5828130150, 5602615567, 871302586, 974607964, 931864629, 934189268, 5439890927)
admin_only = lambda message: message.from_user.id in acl

@dp.message_handler(admin_only, content_types=['any'])
async def handle_unwanted_users(message: types.Message):
    await message.answer(md.text(
                md.text('يمنع استخدام هذا المستخدم للبوت'),
                md.text('وللدعم⚒'),
                md.text(''),
                md.text('نسعد بتواصلكم معنا على الإيميل📥'),
                md.text(''),
                md.text('Khaberapp@gmail.com'),
                sep='\n',
            ),
            parse_mode=ParseMode.MARKDOWN,
        )
    print("blocked user:")
    print(message.chat.id)
    await bot.delete_message(message.chat.id, message.message_id)
    return
    
@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
     username = message.from_user.first_name
     await message.answer(md.text(
                md.text('ياهلا فيك '+ username+'! نورتنا🤩'),
                md.text('اختر احد الخيارات الظاهرة عندك👀'),
                sep='\n',
            ),
            reply_markup=homeKB,
            parse_mode=ParseMode.MARKDOWN,
        )
@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(md.text(
                md.text('لجواب تساؤلاتكم عنا'),
                md.text('وللدعم⚒'),
                md.text(''),
                md.text('نسعد بتواصلكم معنا على الإيميل📥'),
                md.text(''),
                md.text('Khaberapp@gmail.com'),
                sep='\n',
            ),
            reply_markup=homeKB,
            parse_mode=ParseMode.MARKDOWN,
        )
  
@dp.message_handler()
async def kb_answer(message: types.Message):
    if message.text == 'بصورة 🔗':
      await Form.questionW.set() #set qestion first   
      await message.answer("تفضل ارسل سؤالك أولًا:")
    elif message.text == 'بدون صورة':
      await Form.questionWO.set() #set question
      await message.answer("تفضل ارسل سؤالك:")  
    elif message.text == 'مين خابر 👀 ؟':
           await message.answer(md.text(
                md.text('خابر هو منصة للمجتمع العربي!'),
                md.text('هدفنا ربط اصحاب الاسئلة مع اصحاب الخبرات🔗'),
                md.text('في بيئة سهلة الاستخدام!'),
                md.text('مايحتاج تسأل في قروبات الواتس اب، او ترسل في حسابات تويتر!'),
                md.text(''),
                md.text('ارسل لي👾'),
                md.text('وبثواني سؤالك راح يوصل للجهة المستهدفة!🎯'),
                md.text(''),
                md.text('من سؤال بسيط الى سؤال كبير'),
                md.text('اصدقاء خابر قادرين عليه💪🏼'),
                md.text(''),
                md.text('وعلى فكرة! بيئتنا مصممة عشان تكون خالية من ازعاج بوستات ورسايل مالها علاقة بالاسئلة!'),
                md.text('والاسئلة مقسمينها حسب مناطق القصيم'),
                md.text(' عشان يسهل البحث فيها🗂'),
                md.text(''),
                md.text('يحتاج نتكلم اكثر؟ 🤩'),
                sep='\n',
            ),
            reply_markup=homeKB,
            parse_mode=ParseMode.MARKDOWN,) 
    
    elif message.text == 'برسل سؤال 💬':
        await message.answer("وش نوع سؤالك؟", reply_markup=questionTypeKB)
    elif message.text == 'بفعل التنبيهات 🔔':
        mention = "[@KhaberNotific_bot](tg://user?id=6000131725)"
        await message.answer(md.text(
                md.text('لتفعيل التنبيهات'),
                md.text('لما يوصلك جواب لسؤالك🔔'),
                md.text(''),
                md.text('كل اللي عليك انك ترسل لبوت التنبيهات:'),
                md.text(mention),
                sep='\n',
            ),
            reply_markup=homeKB,
            parse_mode = ParseMode.MARKDOWN,)          
    elif message.text == 'ارجع للبداية 🔙':
        await message.answer("على راحتك🙏🏻", reply_markup=homeKB)
    else:
        await message.reply("مافهمتك🤔، ممكن تختار من الخيارات الظاهرة عندك؟")
        
@dp.message_handler(lambda message: '#' in message.text, state=Form.questionWO)
async def process_questionWO_invalid(message: types.Message):
   return await message.reply("سؤالك يحتوي على هاشتاق, اكتب سؤالك بدون هاشتاق")

@dp.message_handler(lambda message: 'http' in message.text, state=Form.questionWO)
async def process_questionWO_invalid_link(message: types.Message):
   mention = "[@kadiar](tg://user?id=679625443)"
   return await message.reply(md.text(
                md.text('نعتذر عن ارسال رابط'),
                md.text('لإرسال رابط في سؤالك'),
                md.text('تواصل هنا:'),
                md.text(mention),
                sep='\n',
            ),
         reply_markup=homeKB,
         parse_mode = ParseMode.MARKDOWN,)
    
@dp.message_handler(state=Form.questionWO)
async def process_questionWO(message: types.Message, state: FSMContext):
     async with state.proxy() as data:
        data['questionWO'] = message.text
        await message.answer(md.text(
                md.text('▪️اختر المنطقة التي تبحث عن الإجابة فيها من الخيارات الظاهرة.'),
                md.text('▪في حالة أنك تبحث عن الإجابة في أي منطقة في القصيم, اختر: #القصيم'),
                sep='\n',
            ),
            reply_markup=cityKB,
            parse_mode=ParseMode.MARKDOWN,
        )
        await Form.cityWO.set() # set cityWO
        
@dp.message_handler(lambda message: message.text not in ["#بريدة", "#عنيزة", "#الرس", "#البكيرية","#البدائع","#القصيم"], state=Form.cityWO)
async def process_cityWO_invalid(message: types.Message):
    return await message.reply("مافهمتك🤔، ممكن تختار من الخيارات الظاهرة عندك؟")
                               
@dp.message_handler(state=Form.cityWO)
async def process_cityWO(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
        data['cityWO'] = message.text
        await message.answer(md.text(
        md.text('▪️اختر التصنيف الأقرب لسؤالك.'),
        md.text('▪️في حالة أن سؤالك لا يندرج تحت أي من التصنيفات الظاهرة, اختر: #عام'),
        sep='\n',
            ),
            reply_markup=categoryKB,
            parse_mode=ParseMode.MARKDOWN,
        )        
        await Form.categoryWO.set() # set category
@dp.message_handler(lambda message: message.text not in ["#مطاعم_ومقاهي","#تسوق_وترفيه","#صحة","#تعليم","#مواصلات","#استشارة","#عام"], state=Form.categoryWO)
async def process_categoryWO_invalid(message: types.Message):
    return await message.reply("مافهمتك🤔، ممكن تختار من الخيارات الظاهرة عندك؟")
  
@dp.message_handler(state=Form.categoryWO)
async def process_categoryWO(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
        data['categoryWO'] = message.text
        await message.answer(md.text('▫️ سؤالك هو :', data['questionWO'] ,
                                     data['cityWO'], data['categoryWO'] ) , reply_markup=sendKB)
        await Form.send.set() # set send
    
@dp.message_handler(lambda message: '#' in message.text, state=Form.questionW)
async def process_questionW_invalid_hashtag(message: types.Message):
   return await message.reply("سؤالك يحتوي على هاشتاق, اكتب سؤالك بدون هاشتاق")
 
@dp.message_handler(lambda message: 'http' in message.text, state=Form.questionW)
async def process_questionW_invalid_link(message: types.Message):
   mention = "[@kadiar](tg://user?id=679625443)"
   return await message.reply(md.text(
                md.text('نعتذر عن ارسال رابط'),
                md.text('لإرسال رابط في سؤالك'),
                md.text('تواصل هنا:'),
                md.text(mention),
                sep='\n',
            ),
         reply_markup=homeKB,
         parse_mode = ParseMode.MARKDOWN,)
 
@dp.message_handler(content_types=['audio','document','sticker','photo','video', 'location','poll' ] , state=Form.questionW)
async def process_questionW_invalid_type(message: types.Message):
    return await message.reply("يرجى ارسال السؤال أولًا")
    
@dp.message_handler(lambda message: message.text not in ["/start", "/help"],
                    state=Form.questionW)
async def process_questionW(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['questionW'] = message.text
        await Form.photo.set() # set photo
        await message.answer("تفضل ارسل الصورة:")
        
@dp.message_handler(content_types=['audio','document','sticker','text','video', 'location','poll' ] , state=Form.photo)
async def process_photo_invalid(message: types.Message):
    return await message.reply("عفوًا ولكن مازلت بانتظار الصورة, يرجى ارسالها كصورة وليس ملف")
  
@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=Form.photo)
async def load_photo(message: types.Message, state: FSMContext):
     # Configure ReplyKeyboardMarkup
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await message.reply("تم حفظ الصورة")
    await message.answer(md.text(
                md.text('▪️اختر المنطقة التي تبحث عن الإجابة فيها من الخيارات الظاهرة.'),
                md.text('▪في حالة أنك تبحث عن الإجابة في أي منطقة في القصيم, اختر: #القصيم'),
                sep='\n',
            ),
            reply_markup=cityKB,
            parse_mode=ParseMode.MARKDOWN,
        )
    await Form.cityW.set() # set cityW          


@dp.message_handler(lambda message: message.text not in ["#بريدة", "#عنيزة", "#الرس", "#البكيرية","#البدائع","#القصيم"], state=Form.cityW)
async def process_cityW_invalid(message: types.Message):
    return await message.reply("مافهمتك🤔، ممكن تختار من الخيارات الظاهرة عندك؟")
  
@dp.message_handler(state=Form.cityW)
async def process_cityW(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
        data['cityW'] = message.text
        await message.answer(md.text(
        md.text('▪️اختر التصنيف الأقرب لسؤالك.'),
        md.text('▪️في حالة أن سؤالك لا يندرج تحت أي من التصنيفات الظاهرة, اختر: #عام'),
        sep='\n',
            ),
            reply_markup=categoryKB,
            parse_mode=ParseMode.MARKDOWN,
        )        
        await Form.categoryW.set() # set category
    
@dp.message_handler(lambda message: message.text not in ["#مطاعم_ومقاهي","#تسوق_وترفيه","#صحة","#تعليم","#مواصلات","#استشارة","#عام"], state=Form.categoryW)
async def process_categoryW_invalid(message: types.Message):
    return await message.reply("مافهمتك🤔، ممكن تختار من الخيارات الظاهرة عندك؟")
  
@dp.message_handler(state=Form.categoryW)
async def process_categoryW(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
        data['categoryW'] = message.text
        await bot.send_photo(chat_id=message.from_user.id,
                              photo=data['photo'],
                              caption=md.text('▫️ سؤالك هو :', data['questionW'], data['cityW'],  data['categoryW']) , 
                              reply_markup=sendPicKB)

        await Form.send.set()

@dp.message_handler(state=Form.send)
async def process_send(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['send'] = message.text
        msglink = 'https://t.me/askkhaber/'
        user_id = message.from_user.id #user id is the same as chat id, to send notification later
        username = message.from_user.mention
        if(message.text=="أرسل السؤال مع الصورة للقناة ✔️"):
        # send message to channel
          async with state.proxy() as data:
           msg = await bot.send_photo(chat_id='@askkhaber',
                             photo=data['photo'],
                             caption=md.text(' 💬 ' + data['questionW'], data['cityW'], data['categoryW']))
           msgID = msg["message_id"]  
           await message.answer(md.text(
                md.text('تم الإرسال بنجاح ✅'),
                md.text('سعيدين لدعمك لنا👾'),
                md.text('رابط سؤالك 🔗: ' , msglink+str(msgID)),
                sep='\n',
            ),
           reply_markup=homeKB,
           parse_mode=ParseMode.MARKDOWN,) 
           print(user_id)
           print(msgID)
           print(username)
                       # insrt user's info into database
           db_object.execute("SELECT status FROM notification WHERE id = %s" , (user_id,)) #get status    
           DB_user_status = db_object.fetchone()
           if DB_user_status != None: #previous questions are there, there is a record in notification
            user_status = DB_user_status[0]     
            db_object.execute("INSERT INTO users(id, message_id, username) VALUES (%s, %s, %s)", (user_id, msgID, username,))
            db_connection.commit()
           else:
            db_object.execute("INSERT INTO users(id, message_id, username) VALUES (%s, %s, %s)", (user_id, msgID, username))
            db_connection.commit()            
            db_object.execute("INSERT INTO notification(id) VALUES (%s)", (user_id))
            db_connection.commit()              
           print(username, user_id)
            
        elif(message.text=="أرسل السؤال للقناة ✔️"):
          # send message to channel
           async with state.proxy() as data:
            msg = await bot.send_message(chat_id='@askkhaber',   #save message id
                             text=md.text(' 💬 ' + data['questionWO'], data['cityWO'],  data['categoryWO']))
            msgID = msg["message_id"]               
            await message.answer(md.text(
                md.text('تم الإرسال بنجاح ✅'),
                md.text('سعيدين لدعمك لنا👾'),
                md.text('رابط سؤالك 🔗: ' , msglink+str(msgID)),
                sep='\n',
            ),
            reply_markup=homeKB,
            parse_mode=ParseMode.MARKDOWN, )
            print(user_id)
            # insrt user's info into database
            db_object.execute("SELECT status FROM notification WHERE id = %s" , (user_id,)) #get status    
            DB_user_status = db_object.fetchone()
            print(DB_user_status)
            if DB_user_status != None: #previous questions are there, there is a record in notification
             user_status = DB_user_status[0]     
             db_object.execute("INSERT INTO users(id, message_id, username) VALUES (%s, %s, %s)", (user_id, msgID, username,))
             db_connection.commit()
            else:
             db_object.execute("INSERT INTO users(id, message_id, username) VALUES (%s, %s, %s)", (user_id, msgID, username))
             db_connection.commit()            
             db_object.execute("INSERT INTO notification(id) VALUES (%s)", (user_id,))
             db_connection.commit()              
            print(username, user_id)
             
        elif(message.text=="ألغي سؤالي❌، وارجع للبداية 🔙"):
               #state.clear()
               await message.answer("على راحتك🙏🏻", reply_markup=homeKB)
    # Finish conversation
    await state.finish()

            
executor.start_polling(dp)
