
str = "C:/Users/ghost/Music/yt1s.com - Dandelion.mp3"
dir_list = []


reverse_dir = str[::-1]
title_reverse = reverse_dir[:reverse_dir.index('/')]
title = title_reverse[::-1]

print(title)