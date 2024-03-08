$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();
        console.log("clicked the button")
        var name = $("input[name='user_name']").val();
        var email = $("input[name='email']").val();
        var phone_number = $("input[name='phone_number']").val();
        var house_name=$("input[name='house_name']").val();
        var street=$("input[name='street']").val();
        var city=$("input[name='city']").val();
        var district=$("input[name='district']").val();
        var state=$("input[name='state']").val();
        var amount=$("input[name='amount']").val();
        var payment_mode=$("input[name='payment_mode']").val();
        var cartid=$("input[name='cartid']").val();
        var token=$("[name='csrfmiddlewaretoken']").val();



        console.log(email)
    //     if(name == "" || email == "" || phone_number == "" ||house_name == "" ||street == "" ||city == "" ||district == "" || state == "" ||amount == "")
    // {
    //     alert("all fields are mandatory")
    //     swal("Alert!", "All fields are mandatory", "error");
    //     return false
    // }
    // else{
        $.ajax({
            method: "GET",
            url: "/proceed_to_pay",
    
            success: function (response) {
              console.log(response); 
               
              var options = {
                "key": "rzp_test_ZCCSyrCe5ZqrEH",
                "amount": response.total_price * 100,
                "currency": "INR",
                "name": "MARLUX",
                "description": "Thank You For Shopping With Us.",
                // "order_id": "{{ order_id }}",
                "handler": function(responseb) {
                    alert(responseb.razorpay_payment_id);
                   
                    data={

                        "name":name ,
                        "email":email,
                        "phone_number":phone_number,
                        "street":street,
                        "city":city,
                        "state":state,
                        "amount":amount,
                        "cartid":cartid,
                        "payment_mode":payment_mode,
                        "payment_id":responseb.razorpay_payment_id,
                        csrfmiddlewaretoken:token

                    }
                    $.ajax({
                       method: "POST",
                        url: "/place_order",
                        data: data,
                        success: function (responsec) {
                            // alert("payment succesful");
                            console.log("order was succesfull")
                            var order_id=responsec.order
                            console.log(order_id)
                            console.log("this is my order id")
                            var redirectUrl = '/my_orders/' + order_id + '/';
                            swal("Congrats",responsec.status,"success").then((value) => {
                                
                                window.location.href=redirectUrl
                              });
                            
                        }
                    });
                    // alert(response.razorpay_order_id);
                    // alert(response.razorpay_signature);
                },
                
                "prefill": {
                    "name": name ,
                    "email": email ,
                    "contact": phone_number 
                },
               
     
                "theme": {
                 "color": "#3399cc"
             }
            };
            var rzp1 = new Razorpay(options);
            
            rzp1.on('payment.failed', function (responsed){
                    alert(responsed.error.code);
                    alert(responsed.error.description);
                    alert(responsed.error.source);
                    alert(responsed.error.step);
                    alert(responsed.error.reason);
                    alert(responsed.error.metadata.order_id);
                    alert(responsed.error.metadata.payment_id);
                    handlePaymentFailure(email, phone_number, street, city, state, amount, cartid, payment_mode, token); 
            });
            rzp1.open();
            }
        });
        
    // }
        
        
    });
    function handlePaymentFailure(email, phone_number, street, city, state, amount, cartid, payment_mode, token) {
        console.log("failure called")
        var data = {
            "email": email,
            "phone_number": phone_number,
            "street": street,
            "city": city,
            "state": state,
            "amount": amount,
            "cartid": cartid,
            "payment_mode": payment_mode,
            csrfmiddlewaretoken: token
        };
        console.log(data.email,data.cartid)
        console.log("the values are hereeeee")
        $.ajax({
            method: "POST",
            url: "/failure_order",
            data: data,
            success: function(responsef) {
                swal("Error", responsef.status, "error").then((value) => {
                    window.location.href = '/failed_order_history';
                });
            }
        });
    }
    
    
});
