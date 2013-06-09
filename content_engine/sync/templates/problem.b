html [
    head [
        meta(charset='utf-8'),
        title ['problem'],
        link(rel='stylesheet', typt='text/css', href=template_path+'css/problem.css'),
        script(type='text/javascript', src=template_path+'js/problem.js')
    ],

    body(onload='load()') [
        div(id='container') [
            div(class_='head') [
                img(src=template_path+'img/head_min.jpg')
            ],
            div(class_='problem') [
                img(id='problem_img', src=problem_image)
            ],
            div(class_='bottom') [
                img(src=template_path+'img/bottom_min.jpg')
            ]
        ]
    ]
]