<p>{{ content }}<!--more--></p>

[box style="rounded shadow"]
[col grid="4-1 first"]<img src="{{ icon }}" class="img-rounded" />[/col]
[col grid="4-2"]<p>分类：{{ category }}</p><p>大小：{{ size }}</p><p>平台：{{ platforms }}</p>[/col]
[col grid="4-1"]<a class="btn btn-success" rel="lightbox" href="http://qrickit.com/api/qr?qrsize=300&d=http://cow.bestgames7.com/games/{{id}}/preview" onclick="_gaq.push(['_trackEvent', 'game', 'download', '{{ id }}']);"><i class="icon-qrcode icon-white"></i>二维码下载</a>[/col]
[/box]

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

{% if video_url %}
[box style="rounded shadow"]<p>游戏视频</p><div class="post-video"><iframe height=498 width=510 src="{{ video_url }}" frameborder=0 allowfullscreen></iframe></div>[/box]
{% endif %}