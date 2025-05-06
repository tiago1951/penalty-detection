@echo off
echo == Penalty Cutter - JPN vs CRO - WC2022 (vídeo apenas) ==
echo.

yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:00:12-00:00:17" -o "jpn-cro-wc2022-1.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:00:53-00:00:56" -o "jpn-cro-wc2022-2.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:01:20-00:01:26" -o "jpn-cro-wc2022-3.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:02:01-00:02:05" -o "jpn-cro-wc2022-4.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:02:41-00:02:46" -o "jpn-cro-wc2022-5.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:03:21-00:03:26" -o "jpn-cro-wc2022-6.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:03:59-00:04:03" -o "jpn-cro-wc2022-7.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=e28LKjF8NI4" --cookies cookies.txt --download-sections "*00:04:35-00:04:42" -o "jpn-cro-wc2022-8.mp4" -f "bv*" --recode-video mp4

echo.
echo ✅ Penáltis JPN vs CRO extraídos com sucesso (vídeo apenas)!
pause >nul
