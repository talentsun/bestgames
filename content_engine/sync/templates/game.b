html [
    head [
        meta(charset='utf-8'),
        title ['game'],
        link(rel='stylesheet', type='text/css', href=template_path+'css/game.css'),
        script(type='text/javascript', src=template_path+'js/game.js')
    ],

    body(onload='load()') [
        div(id='container') [
            div(class_='head'),
            div(class_='screenshots') [
                img (id='screenshot_1', src=screenshot_path_1),
                img (id='screenshot_2', src=screenshot_path_2),
                img (id='screenshot_3', src=screenshot_path_3),
                img (id='screenshot_4', src=screenshot_path_4)
            ],
            div(class_='bottom')
        ]
    ]
]