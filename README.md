# street_nine-nine

쇼핑몰을 구현해보고자 진행한 프로젝트로 Iamport를 이용해 실제 결제까지 구현

<hr>

### Street99 Project 기능 설명
  + 계정 관련(accountapp)
    + Custom User Model로 구현
    + 계정 CRUD 구현
    
  + 배송지 관련(addressapp)
    + Daum 주소 API 적용(https://postcode.map.daum.net/guide)
    + 배송지 CRUD 구현
    + 하나의 계정은 여러개의 배송지를 가질 수 있음(1:N)
    + 기본 배송지 설정 가능
    
  + 장바구니 관련(cartapp)
    + 장바구니 CRUD 구현
    + 하나의 계정은 하나의 장바구니를 갖고(1:1) 그 장바구니는 여러개의 장바구니 상품을 가질 수 있음(1:N)
  
  + 상품 관련(productapp)
    + 하나의 카테고리는 여러개의 상품을 가짐(1:N)
    + 하나의 상품은 여러개의 썸네일/상세이미지를 가질 수 있음(1:N)
    + 상품 관련(카테고리, 상품 상세이미지, 썸네일 이미지) CRUD 구현
    + 상품 등록시(create) django-multi-form-view 패키지를 이용해 하나의 template에 여러개의 Form을 출력하거나 저장할 수 있음

  + 주문 관련(orderapp)
    + 하나의 계정은 하나의 여러개의 주문을 가질 수 있고(1:N), 그 주문은 여러개의 주문 상품을 가질 수 있음(1:N)
    + 결제 부분은 iamport를 이용해 구현하였고, iamport-rest-client 패키지를 통해 구현
    + 사용자 주문시, 주문 table에 저장되면(post_save) iamport에 prepare_validation 요청후 PG사 결제 후 해당 내용을 iamport에서 가져와
      로컬 DB > order transaction이란 table에 저장하여 로컬, iamport에 둘 다 결제 진행 상황을 동기화함
    + 결제 취소시 order transaction에 저장된 정보를 기준으로 iamport에 결제 취소 요청을 보낸 후 응답받은 response를 다시 order transaction에
      update함
  
  + 리뷰 관련(reviewapp)
    + 리뷰 Create, Read 구현
    + 이미지는 원본 이미지로 thumbnail을 구현(django-imagekit으로)하고, 원본 이미지는 따로 저장
    

Velog를 통해 작업 내용을 작성중
https://velog.io/@danho-vak/Django-%EC%87%BC%ED%95%91%EB%AA%B0-%EB%A7%8C%EB%93%A4%EA%B8%B0-1
