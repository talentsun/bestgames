<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" type="text/css" href="{{ template_path }}css/evaluation.css" />
<title>review</title>
</head>
<body>
    <div id="container_head">
        <div id="left">
            <img src="{{ icon }}" width="130px" height="130px"/>
        </div>
        <div id="right">
            <p style="font-family:arial;color:#666666;font-size:20px">{{ title }}</p>
            <p style="font-family:arial;color:#666666;font-size:15px">{{ comment }}</p>
            <div class="right_picture">
            {% if rating == 1 or rating == 2 %}
                <img src= "{{ template_path }}img/score1.png" /> 
            {% endif %}
            {% if rating == 3 or rating == 4 %}
                <img src= "{{ template_path }}img/score2.png" /> 
            {% endif %}
            {% if rating == 5 or rating == 6 %}
                <img src= "{{ template_path }}img/score3.png" /> 
            {% endif %}
            {% if rating == 7 %}
                <img src= "{{ template_path }}img/score3.5.png" /> 
            {% endif %}
            {% if rating == 8 %}
                <img src= "{{ template_path }}img/score4.png" /> 
            {% endif %}
            {% if rating == 9 %}
                <img src= "{{ template_path }}img/score4.5.png" /> 
            {% endif %}
            {% if rating == 10 %}
                <img src= "{{ template_path }}img/score5.png" /> 
            {% endif %}
            {% if android %}
                <img src= "{{ template_path }}img/android.png"/>
            {% endif %}
            {% if ios %}
                <img src= "{{ template_path }}img/ios.png" />
            {% endif %} </div></div> 
    </div>
    <div id="container_body">
        {{ content|safe }}
    </div>
    <div id="container_bottom">
        <img src= "{{ template_path }}img/bottom.png" /></div> 
</body>
</html>
