$(document).ready(function () {
    login_out();
    randomStation();
});

function sign_out() {
    $.removeCookie('mytoken', { path: '/' });
    alert('로그아웃!');
    window.location.href = "/home"
}

function randomStation() {
    $('#card').empty();
    $.ajax({
        type: "GET",
        url: "/random",
        data: {},
        success: function (response) {
            let rows = response['random_posts']
            for (let i = 0; i < rows.length; i++) {
                let liquorNAME = rows[i]['liquorNAME']
                let manufacturer = rows[i]['manufacturer']
                let ingredient = rows[i]['ingredient']
                let volume = rows[i]['volume']
                let proof = rows[i]['proof']
                let feature = rows[i]['feature']
                let imageURL = rows[i]['imageURL']
                let temp_html = `<div class="col">
                                    <div class="card h-100">
                                        <div class="img-container">
                                            <div class="img-content">
                                                <div class="img-box">
                                                    <img src="${imageURL}" class="card-img-top">
                                                </div>
                                            </div>
                                        </div>
                                        <div class="card-body">
                                            <h5 class="card-title"><b>${liquorNAME}</b></h5>
                                            <p class="card-text"><b>제조사</b>: ${manufacturer}</p>
                                            <p class="card-ingredient"><b>주원료</b>: ${ingredient}</p>
                                            <p class="card-text"><b>규격</b>: ${volume}</p>
                                            <p class="card-text"><b>도수</b>: ${proof}</p>
                                            <p class="card-feature"><b>특징</b>: ${feature}</p>
                                        </div>
                                    </div>
                                </div>`
                $('#card').append(temp_html);
            }
        }
    })
}


function login_out() {
    $.ajax({
        type: "GET",
        url: "/loginout",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                $('#logbtn').hide()
                $('#outbtn').show()
            } else {
                $('#logbtn').show()
                $('#outbtn').hide()
            }
        }
    })
}

new Swiper('.notice-line .swiper', {
    direction: 'vertical',
    autoplay: true,
    loop: true
});

new Swiper('.promotion .swiper', {
    slidesPerView: 4, // how many slides we wanna show at once
    spaceBetween: 30, // margin between slides
    centeredSlides: true, // first slide would be centered
    loop: true,
    autoplay: {
    delay: 5000
    },
    pagination: {
    el: '.promotion .swiper-pagination', //
    clickable: true //user's page numbering control
    },
    navigation: {
    prevEl: '.promotion .swiper-prev',
    nextEl: '.promotion .swiper-next'
    }
});
