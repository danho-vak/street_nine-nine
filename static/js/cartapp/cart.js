

function addCartItem(){
    target_product = $('#target_product_pk').val();
    selected_option_1 = $('#option_1 option:selected').val();
    selected_option_2 = $('#option_2 option:selected').val();

    if ((!selected_option_1) || (!selected_option_2)) {
        alert('상품 옵션을 선택해주세요!');
    } else {
        $.ajax({
            url : '/cart/add/',
            type : 'post',
            data : {
                csrfmiddlewaretoken : csrftoken,
                product_id : target_product,
                option_1 : selected_option_1,
                option_2 : selected_option_2,
                quantity : 1
            },success : function (){
                var result = confirm('장바구니에 상품을 추가했어요! 장바구니로 갈까요?');

                if (result){
                    location.href='/cart/';
                } else {
                    location.reload();
                }
            }, error : function (err, status) {
                alert(err+' : '+status);
            }
        });
    }
}