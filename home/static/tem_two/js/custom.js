<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

    $(document).ready(function() {
        $('input[type="radio"]').change(function() {
            var colorId = $('input[name="color"]:checked').val();
            var sizeId = $('input[name="size"]:checked').val();

            if (colorId && sizeId) {
                $.ajax({
                    url: "{% url 'get_price' %}", // replace this with your URL to fetch price
                    method: "GET",
                    data: {
                        'color_id': colorId,
                        'size_id': sizeId
                    },
                    success: function(response) {
                        if (response.price){
                        $('#priceDisplay').text("₹" + response.price);
                    } else {
                        $('#priceDisplay').text("Product Unavailable");
                    } },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText);
                    }
                });
            }
        });

 // Script for adding product to cart
 $('#addToCartBtn').click(function() {
    var colorId = $('input[name="color"]:checked').val();
    var sizeId = $('input[name="size"]:checked').val();
    var quantity = $('#quantityInput').val();

    if (colorId && sizeId && quantity) {
        $.ajax({
            url: "{% url 'add_to_cart' %}",
            method: "GET",
            data: {
                'color_id': colorId,
                'size_id': sizeId,
                'quantity': quantity
            },
            success: function(response) {
                console.log(response);
                var currentBadgeValue = parseInt($('.fa-shopping-cart').next('.badge').text());
                var newBadgeValue = currentBadgeValue + parseInt(quantity);
                $('.fa-shopping-cart').next('.badge').text(newBadgeValue);
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                if (xhr.status === 400 && xhr.responseJSON.error === "Product unavailable") {
                    alert("Product is unavailable.");
                }
            }
        });
    }
});});


