<p>{{ content }}<!--more--></p>

[box style="rounded shadow"]
[col grid="4-1 first"]<img src="{{ icon }}" class="img-rounded" />[/col]
[col grid="4-2"]<p>平台：{{ platforms }}</p><div class="rating rating-{{ rating }}"></div>[/col]
[col grid="4-1"]<a class="btn btn-success" rel="lightbox" href="http://qrickit.com/api/qr?qrsize=300&d=http://cow.bestgames7.com/evaluation/{{id}}/preview" onclick="_gaq.push(['_trackEvent', 'evaluation', 'download', '{{ id }}']);"><i class="icon-qrcode icon-white"></i>二维码下载</a>[/col]
{% if android_download_url %}
[col grid="4-1"]<a class="btn" href="{{ android_download_url }}" style="margin-top:10px;"><i class="icon-download-alt"></i>下载安卓版</a>[/col]
{% else %}
[col grid="4-1"]<a class="btn disabled" href="#" style="margin-top:10px;"><i class="icon-download-alt icon-white"></i>无安卓版</a>[/col]
{% endif %}
{% if iOS_download_url %}
[col grid="4-1"]<a class="btn" href="{{ iOS_download_url }}" style="margin-top:10px;"><i class="icon-download-alt"></i>下载苹果版</a>[/col]
{% else %}
[col grid="4-1"]<a class="btn disabled" href="#" style="margin-top:10px;"><i class="icon-download-alt icon-white"></i>无苹果版</a>[/col]
{% endif %}
[/box]

[box style="rounded shadow"]
<p>测评内容</p>
{{ evaluation_content|safe }}
[/box]
