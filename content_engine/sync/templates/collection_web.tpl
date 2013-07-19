<img src="{{ cover }}" class="img-rounded" />
<p>{{ content }}<!--more--></p>
{% for game in games %}
[box style="rounded shadow"]
<h3 style="padding-bottom:4px;">{{ forloop.counter }}. {{ game.name }} - {{ game.brief_comment}}</h3>
[col grid="4-1 first"]<img src="{{ game.icon }}" class="img-rounded" />[/col]
[col grid="4-2"]<p>分类：{{ game.category }}</p><p>大小：{{ game.size }}</p><p>平台：{{ game.platforms }}</p>[/col]
[col grid="4-1"]<a class="btn btn-success" rel="lightbox" href="http://qrickit.com/api/qr?qrsize=300&d=http://cow.bestgames7.com/games/{{ game.id }}/preview" onclick="_gaq.push(['_trackEvent', 'collection', 'download', '{{ game.id }}']);"><i class="icon-qrcode icon-white"></i>二维码下载</a>[/col]
{% if game.android_download_url %}
[col grid="4-1"]<a class="btn" href="{{ game.android_download_url }}" style="margin-top:10px;"><i class="icon-download-alt"></i>下载安卓版</a>[/col]
{% else %}
[col grid="4-1"]<a class="btn disabled" href="#" style="margin-top:10px;"><i class="icon-download-alt icon-white"></i>无安卓版</a>[/col]
{% endif %}
{% if game.iOS_download_url %}
[col grid="4-1"]<a class="btn" href="{{ game.iOS_download_url }}" style="margin-top:10px;"><i class="icon-download-alt"></i>下载苹果版</a>[/col]
{% else %}
[col grid="4-1"]<a class="btn disabled" href="#" sytle="margin-top:10px;"><i class="icon-download-alt icon-white"></i>无苹果版</a>[/col]
{% endif %}
[col grid="1-4"]
<div class="rating rating-{{ game.rating }}"></div>
[/col]
<div style="clear:both;padding-top:8px;">{{ game.recommended_reason }}</div>
[/box]
{% endfor %}
