<html>
<head>
    <meta charset="utf-8" />
    <title>game</title>
    <link rel="stylesheet" type="text/css" href="{{ template_path }}css/game.css" />
    <script type="text/javascript" src="{{ template_path }}js/screenshots.js"></script>
</head>
<body onload="load()">
    <div id="container">
        <div class="screenshots">
            {% if game.screenshot_path_1 %}
                <img src="{{ game.screenshot_path_1.path }}" id="screenshot_1" />
            {% endif %}
            {% if game.screenshot_path_2 %}
                <img src="{{ game.screenshot_path_2.path }}" id="screenshot_2" />
            {% endif %}
            {% if game.screenshot_path_3 %}
                <img src="{{ game.screenshot_path_3.path }}" id="screenshot_3" />
            {% endif %}
            {% if game.screenshot_path_4 %}
                <img src="{{ game.screenshot_path_4.path }}" id="screenshot_4" />
            {% endif %}
        </div>
        <div class ="bottom"></div>
    </div>
</body>
</html>
