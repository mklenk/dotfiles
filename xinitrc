export PATH="$PATH:$HOME/.i3/bin"

#settings
xset -b

setxkbmap de

oset fp+ ~/.fonts/

xrandr --output DP1 --auto --right-of DP2

[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources
#xrdb -merge ~/.Xresources

dunst -config ~/.i3/dunstrc 
