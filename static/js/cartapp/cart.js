

function addCartItem(){
    target_product = $('#target_product_pk').val();

    $.ajax({
        url : '/cart/add/',
        type : 'post',
        data : {
            csrfmiddlewaretoken : csrftoken,
            product_id : target_product,
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