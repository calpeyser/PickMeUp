from create_account.models import User, Location, Ride, Message, Conversation


# A message_pruner object is a collection of messages that can be made non-redundant in conversations.
# That is, a message_pruner is userful for obtaining only the most recent messages in any given conversation.
# It will also maintain the appropriate string of text to display with the converstaion


class message_pruner:

	def __init__(self, message_list):
		self.messages = message_list;
		if (len(self.messages) > 0):
			self.current = self.messages[0];
			self.index = 0;
		else:
			self.current = None;
			self.index = 0;

	def add(self, new_element):
		self.messages.append(new_element);

	def __iter__(self):
		return self;

	def next(self):
		if self.current == None:
			raise StopIteration;
		elif self.index == len(messages) - 1:
			raise StopIteration;
		else:
			self.index += 1;
			self.current = messages[self.index];
			return self.current;

	def __getitem__(self, key):
		return self.messages[key];

	def __contains__(self, key):
		return key in self.messages;

	def return_list(self):
		return self.messages;

	def print_contents(self):
		for m in self.messages:
			print m.title;

	# this is the important method.  It "punes" the list of messages so that only the most recent message 
	# from each conversation remains.  This way, they can be effectively represented in the template.
	def prune(self):
		# get a hash table of conversations -> messages
		conversations = {};
		for m in self.messages:
			if m.conversation in conversations:
				conversations[m.conversation].append(m);
			else:
				conversations[m.conversation] = [];
				conversations[m.conversation].append(m);
		# sort by timestamp
		for c in conversations:
			conversations[c] = sorted(conversations[c], key=lambda message: message.timestamp);
			conversations[c] = list(reversed(conversations[c]));
		# repopulate message list with most recent of each conversation 
		# for each message, adjust the content to reflect what should be written in the inbox
		self.messages = [];
		for c in conversations:
			for m in conversations[c][1:]:
				conversations[c][0].message += "\\n \\n-----------------------------------------------------------------";
				conversations[c][0].message += "\\n On " + str(m.timestamp) + ", " + str(m.sender) + " wrote: \\n";
				conversations[c][0].message += m.message; 
			self.messages.append(conversations[c][0]);



