import sys
import argparse
import praw

message_text = "I want some gold too! Feed me :)"

# depth is the length of the chain (including og_comment) minus 1
def rec_is_end_of_chain(comment, og_comment, depth):
	# assert comment.gilded
	assert depth >= 1
	if not comment.gilded:
		return False
	parent = comment.parent()
	if type(parent) == praw.models.reddit.submission.Submission:
		return False
	if parent.gilded:
		if depth == 1:
			og_comment.refresh()
			replies = og_comment.replies
			# print(replies)
			for child in replies:
				# print(child)
				if child.gilded:
					return False
			return True
		else:
			rec_is_end_of_chain(parent, og_comment, depth - 1)
	return False

def open_log(filename):
	file = open(filename, "r")
	log = file.readlines()
	file.close()
	i = 0
	while i < len(log):
		log[i] = log[i][:-1]
		i += 1
	return log

def write_log(filename, log):
	with open(filename, "w") as file:
		for line in log:
			file.write(line + "\n")

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("client_id")
	parser.add_argument("client_secret")
	parser.add_argument("user_agent")
	parser.add_argument("username")
	parser.add_argument("password")
	parser.add_argument("log_file_path")
	parser.add_argument("-t", "--top_child_of_gilded", action="store_true")
	parser.add_argument("-c", "--char_limit", type=int, default=200)
	parser.add_argument("-d", "--depth", type=int, default=2)
	parser.add_argument("-n", "--num_comments", type=int, default=200)
	args = parser.parse_args()

	r = praw.Reddit(client_id=args.client_id,
	client_secret=args.client_secret,
	user_agent=args.user_agent,
	username=args.username,
	password=args.password)

	log = open_log(args.log_file_path)
	# print(log)

	all_gilded = r.subreddit("all").gilded(limit=args.num_comments)
	comment_list = []
	for c in all_gilded:
		try:
			if type(c) == praw.models.reddit.submission.Submission:
				continue
			comment = praw.models.Comment(r, id=c)
			submission = comment.submission.id
			print(f"retrieved comment {comment.id} in thread {submission}")
			comment_list.append((comment, submission))
		except:
			print("failed to retrieve comment")

	commented = False
	for c in comment_list:
		if rec_is_end_of_chain(c[0], c[0], args.depth) and \
			c[1] not in log:
			try:
				if (not args.char_limit) or len(c[0].body) <= args.char_limit:
					if args.top_child_of_gilded:
						c[0].refresh()
						replies = c[0].replies
						if len(replies) > 0:
							replies[0].reply(message_text)
						else:
							c[0].reply(message_text)
					else:
						c[0].reply(message_text)
					log.append(c[1])
					print(f"commented on comment {c[0].id} in thread {c[1]}")
					commented = True
				else:
					print("over character limit")
			except Exception as e:
				print(e.message)
				print("rate limited or other exception")
			# print(c[0], c[1])
	if not commented:
		print("presumably there are no comments left to comment on")

	write_log(args.log_file_path, log)
