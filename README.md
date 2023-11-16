Handles die roll strings on twitch. Supports penetrating dice, which are like exploding dice except 1 is subtracted from the explosions. (Used in kenzerco games; https://kenzerco.com/product
-category/hackmaster/)

Builds rolls out of a XdY string
 !roll 3d4 - 2
 !roll 6d10000
 !roll 4d7p + 3

Handles some possible errors but not all of them.

TO GET A TWITCH ACCESS TOKEN
Register your app at https://dev.twitch.tv/console
(You have to enable 2FA on twitch). 
You can set your OAuth Redirect URL to http://localhost:3000 if nothing is listening on that port already.

Get the twitch CLI and 'configure' it. The scope string has to include "chat:read chat:edit"
https://dev.twitch.tv/docs/cli/
need://dev.twitch.tv/docs/cli/configure-command/

There is a guide for doing this that you can follow basically straightforwardly.
https://dev.twitch.tv/docs/authentication/register-app/

Uses twitchio python library
https://twitchio.dev/en/stable/index.html
