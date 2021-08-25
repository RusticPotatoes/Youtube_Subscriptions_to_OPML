import os
import pandas as pd 
import youtube_api
import argparse
import datetime

def main(args): 
	timestr= datetime.datetime.now().strftime(f"%Y_%m_%d-%I_%M_%S_%p")
	parent_dir = os.path.dirname(os.path.realpath(__file__))
	# base url
	url = f"https://www.youtube.com/user/{args.channel}/channels"
	# initilize youtube api object
	youtube_obj=youtube_api.YouTubeDataAPI(key=args.apikey,api_version=3,verify_api_key=True)
	# grab channel id
	channelid=youtube_obj.get_channel_id_from_user(args.channel)
	# use channel id to get subscriptions 
	subscriptions = youtube_obj.get_subscriptions(channelid)
	# data 
	sub_df = pd.DataFrame(subscriptions)
	sub_data = pd.DataFrame()
	sub_data['subscription_title'] = sub_df['subscription_title']
	sub_data['subscription_channel_id'] = sub_df['subscription_channel_id']
	sub_data_transposed = sub_data.transpose()

	content = '''<opml version="1.0">'''
	content +=f'''	
	<body>
		<outline title="YT Subs {args.channel}" text="Youtube {args.channel}">'''
	for index, row in sub_data.iterrows():
		sub_title=row['subscription_title']
		channel_id=row['subscription_channel_id']
		content+=f'''        
			<outline title="{sub_title}" text="{sub_title}" xmlUrl="https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}" htmlUrl="https://www.youtube.com/channel/{channel_id}" />'''
	content += '''		
		</outline>
	</body>
</opml>'''
	
	with open(os.path.join(parent_dir,f"{args.channel}_subscriptions_{timestr}.xml"), "w") as file:	
		file.write(content)
		file.close()

if __name__ == "__main__":
	# setup arg parser
	parser = argparse.ArgumentParser(description='Generate OPML From a Youtube Channels Subscriptions For RSS Import or Archive Purposes')
	# add arguments
	parser.add_argument('--apikey', type=str, required=True,
						help='API key from a google project, 39 chars, setup instructions here: https://developers.google.com/youtube/v3/getting-started')
	parser.add_argument('--channel', default="Youtube",
						type=str,
						help='Channel name you wish to scrape channel subscriptions from, example RickastleyCoUkOfficial')
	# pass arguments to main
	main(parser.parse_args())
