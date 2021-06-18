from instascrape import *

saved_reel_path = "./insta/reel.mp4"
saved_hashtag_path = "./insta/"
saved_profile_path = "./insta/"

def getInsta(url):
    check_url = url.split('/')
    del check_url[0:3]
    if ("reel" == check_url[0].lower()):
        reel = Reel(url)
        reel.scrape()
        reel.download(saved_reel_path)
    elif ("explore" == check_url[0].lower()):
        hashtag = Hashtag(url)
        hashtag.scrape()
        get_hashtag_posts = hashtag.get_recent_posts(amt=12)
        profile_photo_posts = [post for post in get_hashtag_posts if not post.is_video]
        for index, post in enumerate(profile_photo_posts):
            post.download('{}/{}.png'.format(saved_hashtag_path ,index))
    else:
        #Profile URL
        profile = Profile(url)
        profile.scrape()
        get_profile_posts = profile.get_recent_posts(amt=12)
        profile_photo_posts = [post for post in get_profile_posts if not post.is_video]
        for index, post in enumerate(profile_photo_posts):
            post.download('{}/{}.png'.format(saved_profile_path ,index))

if __name__ == '__main__':
    getInsta()
