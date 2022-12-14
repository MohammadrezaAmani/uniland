# Messages to be shown in the project

import enum


class Messages(enum.Enum):

    HELP_MENU = 'راهنمای ثبت و دریافت فایل، جستجو و استفاده از ربات UniLand'

    HELP_MENU_SEARCH = 'نکات مرتبط به بخش جستجو :\n⭕️ ربات UniLand به شما عزیزان قابلیت دو مدل سرچ را می‌دهد. \n     - سرچ داخل ربات \n     - سرچ اینلاین (داخل چت های pv و گروه و کانال...)\n⭕️ در جستجوی خود سعی کنید از کاراکتر "نیم فاصله" استفاده نکنید. (علوم‌‌ریاضی❌، علوم ریاضی✅)\n⭕️ برای دستیابی هرچه دقیق تر به اطلاعات مورد نظرتان، نگارش صحیح و دقیق کلمه را رعایت کنید. (امیرگبیر❌، امیرکبیر✅'

    HELP_MENU_SUBMIT = 'نکات مرتبط به بخش ارسال محتوا:\n⭕️ در درج اطلاعات مرتبط با فایل ارسالی خود و نگارش کلمات دقت کافی داشته باشید.\n⭕️ پس از درج و تکمیل اطلاعات، دکمه "اتمام" را بزنید.\n⭕️ در ثبت اطلاعاتی مانند دانشگاه و نام استاد، از کلمات "دانشگاه" و "استاد" استفاده نکنید. (استاد دهقان❌، دهقان✅، دانشگاه صنعتی امیرکبیر❌، صنعتی امیرکبیر✅)'

    HELP_MENU_ABOUT_US = 'ساخته شده توسط جمعی از دانشجویان علوم کامپیوتر دانشگاه صنعتی امیرکبیر (پلی‌تکنیک تهران)\n\nایلیا، پوریا، دلارام، علی، فاطمه، محمدرضا، مریم، مهسا'

    HELP_MENU_COMING_SOON = '⭕️ دسترسی اسان به فرم های آموزشی دانشگاه\n⭕️ راهنما و اطلاعات به روز انتخاب واحد هر ترم\n⭕️ راهنمای اپلای\n⭕️ تعامل و درس خوانی با دانشجو های دیگر\n⭕️ ریمایندر\n⭕️ دریافت و تبادل روزانه غذای سلف\n⭕️ و ...'

  #     ------- MYPROFILE ---------

    MYPROFILE_ACCESS_LEVEL = '🎚️ سطح دسترسی: '

    MYPROFILE_SCORE = '🎰 امتیاز: '

    SUBMISSIONS_COUNT = '📦 تعداد ثبت‌ها: '

    BOOKMARKS_TITLE = '🖇️ تعداد پسندها: '
    BOOKMARKS_NOT_FOUND_TITLE = '!شما هیچ پسندی ندارید'

  #    ----- MISC -----
    DEFAULT_EMPTY_RESULT_TITLE = '.نتیجه‌ای یافت نشد'

  #   ------ ADMIN -----
    ACCESS_LEVEL_BY_USERID = ':یوزر آیدی مورد نظر را وارد کنید \n .می‌توانید یوزر آیدی را وارد کنید و یا یک پیام از شخص مورد نظر فوروارد کنید'
    ACCESS_LEVEL_CHOOSE = ':سطح دسترسی مد نظر را وارد کنید \n\n'
    ACCESS_LEVEL_LEVELS = 'عادی: 1 - ادیتور: 2 - ادمین: 3'
    ACCESS_LEVEL_UPDATED = '.سطح دسترسی کاربر با موفقیت آپدیت شد \n\n'

    CONFIRMATION_NO_UNCONFIMRED_FILE = ".فایل تایید نشده‌ای یافت نشد"
    CONFIRMATION_FINISH_PREVIOUS_REVIEW = "قبل از دریافت فایل جدید، بررسی فایل قبلی را تکمیل کنید."
    CONFIRMATION_ALREADY_REVIEWED = "این فایل قبلا بررسی شده است"

    CONFIRMATION_REJECTION_HEAD = "❕یکی از ثبت‌های شما رد شده است."
    CONFIRMATION_REJECTION_SUBMISSION = "📑 محتوای ارسالی: "
    CONFIRMATION_REJECTION_REASON = "🚫 دلیل رد شدن: "
