// 장바구니 상품의 수량을 변경
    function changeQuantity(target_item, origin_item_quantity){
        input_quantity = $('#cart_item_quantity_'+target_item).val();

        // 기존에 저장된 수량값과 다르다면(수정할 수 있다면)
        if (input_quantity != origin_item_quantity) {

            if (input_quantity > 0) {
                $.post(quantity_update_url,
                    {
                        'csrfmiddlewaretoken' : csrftoken,
                        'target_item' : target_item,
                        'input_quantity' : input_quantity
                    }, function() {
                        alert('상품 수량을 변경했어요!');
                        location.reload();
                });
            } else {
                alert('수량을 정확하게 입력해주세요!');
            }
        }
    }

    // checkbox 선택된 값이 있는지 확인
    function isChecked(){
        checked_item = $('input[name=cart_item_checkbox]:checked');

        if (checked_item.length > 0) {
            return checked_item;
        } else {
            return false;
        }
    }

    // 선택된 장바구니 상품 삭제
    function deleteCartItem(){
        checked_item = isChecked();
        if (checked_item) {
            var result = confirm('해당 상품을 장바구니에서 제외할까요?');
            var cart_pk = $('#target_cart').val()
            var cart_item_list = []

            if (result) {
                for (var i=0; i<checked_item.length; i++) {
                    cart_item_list.push(checked_item[i].value);
                }

                $.post(cart_item_delete_url,
                    {
                        'csrfmiddlewaretoken' : csrftoken,
                        'cart_item_list' : cart_item_list
                    }, function() {
                        alert('삭제완료!');
                        location.reload();
                });
            }
        } else {
            alert('상품을 선택해주세요!');
        }
    }

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