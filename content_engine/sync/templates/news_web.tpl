<p>{{ content }}<!--more--></p>

[box style="rounded shadow"]
<p>游戏截图</p>
[slider class="screenshots"]
{% if screenshot_path_1 %}
[slide]<img src="{{ screenshot_path_1 }}" class="img-rounded" />[/slide]
{% endif %}
{% if screenshot_path_2 %}
[slide]<img src="{{ screenshot_path_2 }}" class="img-rounded" />[/slide]
{% endif %}
{% if screenshot_path_3 %}
[slide]<img src="{{ screenshot_path_3 }}" class="img-rounded" />[/slide]
{% endif %}
{% if screenshot_path_4 %}
[slide]<img src="{{ screenshot_path_4 }}" class="img-rounded" />[/slide]
{% endif %}
[/slider]
[/box]

[box]
<p>游戏视频</p>
<div class="post-video"><iframe height=498 width=510 src="{{ video_url }}" frameborder=0 allowfullscreen></iframe></div>
[/box]
