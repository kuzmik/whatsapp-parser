# WhatsApp log parser

Parse a WhatsApp `_chat.txt` log into SQLite. Tested with a log from WhatsApp v2.17.42 on an iPhone.

1. [Export](https://faq.whatsapp.com/en/iphone/20888066) your chat history to your computer
1. Unzip the zipfile that is copied to your computer
1. Run `./parser -f YOUR_CHAT_FILE.txt`
	* This will just parse the file; add `-d` to save it to a sqlite database
1. That's basically it

This is definitely a work in progress and will probably not work for everyone; for instance time formats will break things.


#### TODO
1. find a way to combine the two regular expressions into one
1. whatever else crops up