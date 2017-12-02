def handle(user, msg, page):
    page.send(user, "thank you! your message is '%s'" % msg)