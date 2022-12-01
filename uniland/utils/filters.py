import asyncio
# from uniland.db import user_methods as user_db
from uniland import usercache
from uniland.db.db_methods import get_last_step
from uniland.db.tables import User
from uniland.utils import messages, steps
from pyrogram import filters
import pyrogram


async def admin_checker(self, client, message):
  return False


admin_only = filters.create(admin_checker)

def access_level(min: int = 1, max: int = 3):
	async def func(self, client, message):
		return usercache.has_permission(message.from_user.id, 
                                      min_permission=min,
                                      max_permission=max)

	return filters.create(func)

def user_step(step: str):
  async def func(self, client, message):
    return usercache.match_step(message.from_user.id, step)

  return filters.create(func)

async def document_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.DOCUMENT_SUBMISSION:
    return True
  return False


async def document_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.DOCUMENT_SUBMISSION:
    return True
  return False


async def document_search_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.DOCUMENT_SEARCH:
    return True
  if message.text == 'سلام':
    return True


async def source_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.SOURCE_SUBMISSION:
    return True
  return False


async def source_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.SOURCE_SUBMISSION:
    return True
  return False


async def source_search_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.SOURCE_SEARCH:
    return True
  return False


async def recorded_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.RECORDED_SUBMISSION:
    return True
  return False


async def recorded_submission_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.RECORDED_SUBMISSION:
    return True
  return False


async def recorded_search_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  last_step = get_last_step(message.from_user.id)
  if last_step == steps.RECORDED_SEARCH:
    return True


async def document_func_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  return message.text.startswith('/bo')


async def recorded_func_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  return message.text.startswith('/re')


async def source_func_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  return message.text.startswith('/so')


async def document_react_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  return message.data.startswith('like:document') or message.data.startswith(
      'dislike:document')


async def document_submission_no_check(
        self, client: pyrogram.client.Client,
        message: pyrogram.types.messages_and_media.message.Message):
  print(message.data)
  print(messages.DOCUMENT_SUBMISSION_NO + ':document')
  return messages.DOCUMENT_SUBMISSION_NO + ':document' == message.data

document_submission = filters.create(document_submission_check)
document_submission = filters.create(document_submission_check)
document_search = filters.create(document_search_check)
source_submission = filters.create(source_submission_check)
source_submission = filters.create(source_submission_check)
source_search = filters.create(source_search_check)
recorded_submission = filters.create(recorded_submission_check)
recorded_submission = filters.create(recorded_submission_check)
recorded_search = filters.create(recorded_search_check)
document_check = filters.create(document_func_check)
recorded_check = filters.create(recorded_func_check)
source_check = filters.create(source_func_check)
document_react = filters.create(document_react_check)
document_submission_no = filters.create(document_submission_no_check)
