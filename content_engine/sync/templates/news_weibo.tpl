<html>
<head>
    <meta charset="utf-8" />
    <title>news</title>
    <link rel="stylesheet" type="text/css" href="{{ template_path }}css/news.css" />
    <script type="text/javascript" src="{{ template_path }}js/screenshots.js"></script>
</head>
<body onload="load()">
    <div id="container">
        <div class="screenshots">
            {% if screenshot_path_1 %}
            <img src="{{ screenshot_path_1 }}" id="screenshot_1" />
            {% endif %}
            {% if screenshot_path_2 %}
            <img src="{{ screenshot_path_2 }}" id="screenshot_2" />
            {% endif %}
            {% if screenshot_path_3 %}
            <img src="{{ screenshot_path_3 }}" id="screenshot_3" />
            {% endif %}
            {% if screenshot_path_4 %}
            <img src="{{ screenshot_path_4 }}" id="screenshot_4" />
            {% endif %}
        </div>
        <div class="bottom"></div>
    </div>
</body>
</html>
