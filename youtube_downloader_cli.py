
from pytube import YouTube


# функция принимает в качестве аргумента url видео
def video_downloader(video_url):

    # передача url объекту YouTube
    my_video = YouTube(video_url)

    # загрузка видео в высоком разрешении
    my_video.streams.get_highest_resolution().download('C:\\download_youtube\download')

    # возвращает название видео
    return my_video.title

# оператор try будет выполняться, если нет ошибок
try:
    # получение url от пользователя
    youtube_link = input('Вставьте ссылку на видео:')
    
    print('Закрузка видео, подождите.......')
    
    # передача url в функцию
    video = video_downloader(youtube_link)

    # вывод названия видео
    print('Загрузка выполнена!!')
    
# except будет отлавливать ValueError, URLError, RegexMatchError и им подобные
except:
    print('не удалось загрузить видео\n'
          'Причинами могут быть следующие факторы\n* Нестабильное интернет-соединение \n* Недопустимая ссылка')
