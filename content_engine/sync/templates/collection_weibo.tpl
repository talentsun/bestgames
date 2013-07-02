<html>
<head>
    <meta charset='utf-8' />
    <title>collection</title>
    <link rel="stylesheet" type="text/css" href="{{ template_path }}css/collection.css">
    <link rel="stylesheet" type="text/css" href="http://cow.bestgames7.com/static/css/bootstrap.min.css">
</head>
<body>
    <div id="container">
        <div>
            <img src="{{ cover }}" class="cover" />
        </div>
        <div class="games">
            {% for game in games %}
            <div class="game-info">
                <div class="screenshot", style="background-image:url('{{ game.screenshot_path_1 }}');"></div>
                <div class="rating rating-{{ game.rating }}"></div>
                <div class="meta-info">
                    <div class="icon thumbnail img-rounded" style="background-image:url('{{ game.icon }}')"></div>
                    <div class="meta">
                        <h3>{{ game.name }}</h3>
                        <p>{{ game.category }}</p>
                        {% if game.size %}
                        <p>{{ game.size }}</p>
                        {% else %}
                        <p>&nbsp;</p>
                        {% endif %}
                    </div>
                    <p class="intro">{{ game.recommended_reason }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>
