read -r -d '' DOMAINS <<EOV
http://tiktok.com
https://ads.faceBook.com.
https://sub.ads.faCebook.com
api.tiktok.com
Google.com.
aws.amazon.com
EOV

echo "Domains to parse:"
echo "$DOMAINS"

COMMAND_1="grep -oP \'[a-zA-Z0-9\-]+\.[a-z]+[\.]{0,1}$\' | sed \'s/\.$//\' | awk \'{print tolower(\$0)}\' | sort -u"
printf "\nExample 1:\n"
echo "$COMMAND_1"
echo "Result:"
echo "$DOMAINS" | grep -oP '[a-zA-Z0-9\-]+\.[a-z]+[\.]{0,1}$' | sed 's/\.$//' | awk '{print tolower($0)}' | sort -u


printf "\nExample 2:\n"
COMMAND_2="sed -E 's@^https?://@@' | tr '[:upper:]' '[:lower:]' | sed \'s/\.$//\' | grep -oP \'[a-zA-Z0-9\-]+\.[a-z]+[\.]{0,1}$\' | sort -u"
echo "$COMMAND_2"
echo "Result:"
echo "$DOMAINS" | sed -E 's@^https?://@@' | tr '[:upper:]' '[:lower:]' | sed 's/\.$//' | grep -oP '[a-zA-Z0-9\-]+\.[a-z]+[\.]{0,1}$' | sort -u
