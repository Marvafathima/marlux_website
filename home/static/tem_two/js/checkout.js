$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();
        console.log("clicked the button")
        var name = $("input[name='user_name']").val();
        var email = $("input[name='email']").val();
        var phone_number = $("input[name='phone_number']").val();
        var house_name=$("[house_name='house_name']").val();
        var street=$("[street='street']").val();
        var city=$("[city='city']").val();
        var district=$("[district='district']").val();
        var state=$("[state='state']").val();
        var amount=$("[amount='amount']").val();
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
                "handler": function(response) {
                    alert(response.razorpay_payment_id);
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
            
            // rzp1.on('payment.failed', function (response){
            //         alert(response.error.code);
            //         alert(response.error.description);
            //         alert(response.error.source);
            //         alert(response.error.step);
            //         alert(response.error.reason);
            //         alert(response.error.metadata.order_id);
            //         alert(response.error.metadata.payment_id);
            // });
            rzp1.open();
            }
        });
        
    // }
        
        
    });
});

