import telebot
from googleapiclient.discovery import build
from pytube import YouTube

# указываем токен нашего бота
token = '7159605277:AAENqd_ld-8rPcU3aFW_-R35sseTVSoTdBA'
bot = telebot.TeleBot(token)

# указываем ключ для доступа к YouTube API
youtube_api_key = 'AIzaSyDM3xUhvONxTSynKbGGVQXxrKm__pDGp9s'
youtube_service = build('youtube', 'v3', developerKey=youtube_api_key)


# функция для поиска видео на YouTube по запросу и вывод ссылок
def search_youtube_videos(query):
    request = youtube_service.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=5
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        videos.append(video_url)
    return videos


def download_video(url):
    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download('downloads')
    return f'downloads/{yt.title}.mp4'


# обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я могу найти видео на YouTube, картинки в Google и что-то еще. Введите команду"
                          " /help для получения инструкций.")


# обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(message, "Чтобы найти видео на YouTube, введите /video <запрос>. Чтобы скачать видео с Youtube"
                          " по ссылке, введите /download <ссылка>.")


# обработчик команды /video
@bot.message_handler(commands=['video'])
def handle_video(message):
    query = message.text.replace('/video ', '')
    videos = search_youtube_videos(query)
    bot.reply_to(message, f"Результаты поиска на YouTube: {' '.join(videos)}")


# обработчик команды /download
@bot.message_handler(commands=['download'])
def handle_video(message):
    query = message.text.replace('/download ', '')
    videos = search_youtube_videos(query)

    for video in videos:
        video_path = download_video(video)
        video_file = open(video_path, 'rb')
        bot.send_video(message.chat.id, video_file)
        video_file.close()


# запускаем бота
bot.polling()