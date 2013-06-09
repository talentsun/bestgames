html [
    head [
        meta(charset='utf-8'),
        title ['redier'],
        link(rel='stylesheet', type='text/css', href=template_path+'css/redier.css'),
        script(type='text/javascript', src=template_path+'js/redier.js')
    ],

    body(onload='load()') [
        div(id='container') [
            div(class_='head') [
                img(src=template_path+'img/redier_head_min.jpg')
            ],
            div(class_='redier') [
                img(id='redier_img', src=redier_image)
            ],
            div(class_='bottom') [
                img(src=template_path+'img/redier_bottom_min.jpg')
            ]
        ]
    ]
]