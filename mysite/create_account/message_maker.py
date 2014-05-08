from create_account.models import User, Location, Ride, Message, Conversation, Passenger
import datetime
from datetime import datetime
from datetime import date


# m_title = string.  m_content = string. m_sender = User.  m_recepients = list of users
def message_make(m_title, m_content, m_sender, m_recepients):
	this_conversation = Conversation(title=m_title);
	this_conversation.save();
	this_conversation.participants.add(m_sender);
	for recepient in m_recepients:
		this_conversation.participants.add(recepient);
	this_message_contents = m_content;
	this_message = Message(sender = m_sender, title = m_title, message = m_content, unread = True, timestamp = datetime.now(), conversation =	this_conversation);
	this_message.save();
	for recipient in m_recepients:
		this_message.recipients.add(recipient);
