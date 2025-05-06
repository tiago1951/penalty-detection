@echo off
echo == Penalty Cutter - CRO vs DIN - WC2018 (vídeo apenas) ==
echo.

yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:00:52-00:00:58" -o "cro-din-wc2018-1.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:01:44-00:01:47" -o "cro-din-wc2018-2.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:02:39-00:02:42" -o "cro-din-wc2018-3.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:03:22-00:03:26" -o "cro-din-wc2018-4.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:04:17-00:04:20" -o "cro-din-wc2018-5.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:05:03-00:05:06" -o "cro-din-wc2018-6.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:05:53-00:05:57" -o "cro-din-wc2018-7.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:07:00-00:07:06" -o "cro-din-wc2018-8.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:07:52-00:07:58" -o "cro-din-wc2018-9.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=lO36Q8Uj2bE" --cookies cookies.txt --download-sections "*00:08:50-00:08:54" -o "cro-din-wc2018-10.mp4" -f "bv*" --recode-video mp4

echo.
echo ✅ Penáltis CRO vs DIN extraídos com sucesso (vídeo apenas)!
pause >nul