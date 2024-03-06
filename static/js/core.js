function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

var card_product_item = document.querySelectorAll('.card-item-update');
for(var i=0;i< card_product_item.length;i++){
    card_product_item[i].addEventListener('click',function(){
        var order_item_id = this.dataset.order_item_id;
        var action = this.dataset.action;
        console.log(order_item_id)
        console.log(action)
        updateOrderItem(order_item_id,action);
    })
}

//password show hide
var all_change_button = document.querySelectorAll(".password_show_hide");
all_change_button.forEach((data)=>{
    data.addEventListener('click',()=>{
    console.log(data.id)
    var change_id = data.id;
    var type_check = $("#i"+change_id).prop('type');
    $('#'+change_id).empty();
    if(type_check == 'password'){
        $("#i"+change_id).attr('type','text');
        $('#'+change_id).append('<i class="far fa-eye-slash"></i>');
    }else{
        $("#i"+change_id).attr('type','password');
        $('#'+change_id).append('<i class="far fa-eye"></i>');
    }
    
    });
});


var p_year =new Date()
$("#footer_present_year").text(p_year.getFullYear()) 