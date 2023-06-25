console.log("hello world")
var update_button = document.getElementsByClassName('update-cart')

for (let i = 0; i < update_button.length; i++) {
    update_button[i].addEventListener('click',function(){
        // cách lấy các thuộc tính của element được đặt tên bằng data-...
        // data.ten or data['ten']
        var product_id = this.dataset.product;
        var action = this.dataset['action'];
        console.log('productid:',product_id,'action:',action)
        console.log('USER:',user)
        if(user ==='AnonymousUser')
        {
            console.log("not log in")

        }else{
            updateUserOrder(product_id, action)
        }
    })
}

function updateUserOrder(product_id, action) {
    console.log("user is authenticated, sending data...");
    var url ='/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({
            'productId':product_id,
            'action':action
        })
    })
    .then((response)=>response.json())
    .then((responseData)=>{
        console.log("res data:",responseData)
        
    })
}