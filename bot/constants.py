"""In this module defines all text constants used by the bot to create text replies."""

start_message_private = """Hello, {fullname}!
This bot helps you to create and manage queues in your group. Just add it to the group and type 
/create_queue <queue name> 
command.

To see the help type /help
To the the detailed info about the bot type /about_me.
"""

start_message_chat = "Hello, [{fullname}](tg://user?id={user_id})\! \n" \
                     "I've already here and waiting for your commands\.😉"

unknown_command = "Unknown command. \n" \
                  "To see the help type /help or type '/' to see the hints for commands, " \
                  "press tab and complete selected command by adding required arguments."" "

unimplemented_command = "This command haven't implemented yet.😔😔\n" \
                        "Type /about_me to contact the developer."

help_message = """Add this bot to the group and type
/create_queue <queue name> 
command to create a queue. You can also type /notify_all command before creating any queue to notify group members when some queue was created. You can then add yourself to the created queue by typing
/add_me <queue name> 
command. 
And, at the end, type 
/next <queue name> 
command to notify a group member, whose turn came and move the queue further.

You can also type '/' to see all available commands.
"""

help_message_in_chat = 'TODO'

about_me_message = """
Having troubles with managing queues in your group? Want to make queues maximum honest and objective? Well, this is the decision!
I'm QueueBot and I'll help you to do all stuff related to queues and managing them.

Just add me to the group and type 
/create_queue &lt;queue name&gt; 
command to create a queue. You can also type /notify_all command before creating any queue to notify group members when some queue was created. This will help them to be in touch and don't miss the new queues, they could want to participate in.
You can then add yourself to the created queue by typing
/add_me &lt;queue name&gt; 
command. 
And, at the end, type 
/next &lt;queue name&gt; 
command to notify a group member, whose turn came and move the queue further.

My creator said that he will be very thankful for your feedback, any suggestions are welcomed and bug reports are priceless!

Bot version: unreleased.
Developer: @l3_l_a_cl
Github repository: <a href='https://github.com/BlaD200/QueueTGBot'>link</a>
"""
