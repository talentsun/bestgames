<html>
<head>
    <meta charset='utf-8' />
    <title>puzzle</title>
    <link rel="stylesheet" type="text/css" href="{{ template_path }}css/puzzle.css" />
</head>
<body>
    <div id="container">
        <div class="head"></div>
        <div class="puzzle_pic">
            <img src="{{ puzzle_pic }}" />
        </div>
        <p id="description">{{ puzzle_content }}</p>
        <table>
            <tr>
                <td><span class="option_id">A.</span>{{ optiona }}</td>
                <td><span class="option_id">B.</span>{{ optionb }}</td>
            </tr>
            <tr>
                <td><span class="option_id">C.</span>{{ optionc }}</td>
                <td><span class="option_id">D.</span>{{ optiond }}</td>
            </tr>
        </table>
        <div class="bottom"></div>
    </div>
</body>
</html>


