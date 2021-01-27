

function addCart(){
    target_product = $('#target_product_pk').val();

    $.ajax({
        url : '/cart/add/',
        type : 'post',
        data : {
            csrfmiddlewaretoken : csrftoken,
            product_id : target_product,
            quantity : 1
        },success : function (){
            var go_to_cart = confirm('장바구니에 상품을 추가했어요! 장바구니로 갈까요?');

            if (go_to_cart){
                location.href='';
            } else {
                location.reload();
            }
        }, error : function (err, status) {
            alert(err+' : '+status);
        }
    });
}