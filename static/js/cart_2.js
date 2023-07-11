console.log("hello");
// lấy ra tất cả các nút có chức năng update-cart
var update_button = document.getElementsByClassName("update-cart");

for (let i = 0; i < update_button.length; i++) {
  update_button[i].addEventListener("click", function () {
    // cách lấy các thuộc tính của element được đặt tên bằng data-...
    // data.ten or data['ten']
    var product_id = this.dataset.product;
    var action = this.dataset["action"];
    console.log("productid:", product_id, "action:", action);
    console.log("USER:", user);
    if (user === "AnonymousUser") {
      addCookieItem(product_id,action);
    } else {
      updateUserOrder(product_id, action);
    }
  });
}

function addCookieItem(product_id, action) {
  console.log("not logged in..");
  if(action =='add')
  {
    if (cart[product_id]==undefined)
    {
      cart[product_id] ={'quantity':1}

    }else{
      cart[product_id]['quantity']+=1
    }
  }
  if(action == 'remove')
  {
    cart[product_id]['quantity'] -= 1
    if(cart[product_id]['quantity'] <= 0)
    {
      console.log("item should be deleted")
      delete cart[product_id]
    }
  }
  // set cart in cookie
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  console.log(cart)
  location.reload()
}

function updateUserOrder(product_id, action) {
  console.log("user is authenticated, sending data...");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: product_id,
      action: action,
    }),
  })
    .then((response) => response.json())
    .then((responseData) => {
      location.reload();
    });
}
