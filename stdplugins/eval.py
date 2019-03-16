# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from telethon import events, sync, errors, functions, types
import inspect
import io


@borg.on(events.NewMessage(pattern=r"\.eval ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing ...")
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        cmd = (await event.get_reply_message()).text
        reply_to_id = event.reply_to_msg_id
    evaluation = None
    # https://t.me/telethonofftopic/43873
    try:
        if inspect.isawaitable(eval(cmd)):
            evaluation = await eval(cmd)
        # https://t.me/telethonofftopic/43873
        else:
            evaluation = eval(cmd)
    except (Exception) as e:
        evaluation = str(e)
    # https://t.me/telethonofftopic/43873
    final_output = "**EVAL**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    if len(final_output) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=cmd,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(final_output)
