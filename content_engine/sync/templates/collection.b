html [
    head [
        meta(charset='utf-8'),
        title ['collection'],
        link(rel='stylesheet', type='text/css', href=template_path+'css/collection.css'),
        link(rel='stylesheet', type='text/css', href='http://cow.bestgames7.com/static/css/bootstrap.min.css')
    ],

    body [
        div(id='container') [
            div(class_='head'),
            div [
                img(class_='cover', src=collection_cover),
                div(class_='triangle'),
                div(class_='title') [
                    span(style='margin-left:40px;') ['游戏合集 之'],
                    span(style='margin-left:20px;') [collection_title]
                ]
            ],
            div(class_='games') [
                div(class_='game-info') [
                    div(class_='screenshot', style='background-image:url(\'$game_img\');'),
                    div(class_='rating rating-$game_rating'),
                    div(class_='meta-info') [
                        div(class_='icon thumbnail, img-rounded', style='background-image:url(\'$game_icon\');'),
                        div(class_='meta') [
                            h3 ['$game_name'],
                            p ['$game_category'],
                            p ['$game_size']
                        ],
                        p(class_='intro') ['$game_brief_comment']
                    ]
                ] * games
            ],
            div(class_='bottom')
        ]
    ]
]