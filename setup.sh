echo "\
[general]\n\
email = \"alex0972112871@gmail.com\"\n\
" > ~/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/config.toml