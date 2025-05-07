@echo off
echo == Penalty Cutter - BRA vs CRO - WC2022 (vídeo apenas) ==
echo.

yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:00:15-00:00:17" -o "bra-cro-wc2022-1.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:01:51-00:01:52" -o "bra-cro-wc2022-3.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:02:29-00:02:32" -o "bra-cro-wc2022-4.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:03:16-00:03:20" -o "bra-cro-wc2022-5.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:03:58-00:04:03" -o "bra-cro-wc2022-6.mp4" -f "bv*" --recode-video mp4
yt-dlp "https://www.youtube.com/watch?v=uR9vgLLDhE0" --cookies cookies.txt --download-sections "*00:04:43-00:04:48" -o "bra-cro-wc2022-7.mp4" -f "bv*" --recode-video mp4

echo.
echo ✅ Penáltis BRA vs CRO extraídos (vídeo apenas)!
pause >nul