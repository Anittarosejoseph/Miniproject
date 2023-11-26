document.addEventListener("DOMContentLoaded", function () {

   
    updateTotalPrice();

const increaseButtons = document.querySelectorAll(".increase-quantity");
const decreaseButtons = document.querySelectorAll(".decrease-quantity");
//const quantityElements = document.querySelectorAll(".item-quantity");
//const priceElements = document.querySelectorAll(".cart-item-price");

increaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const quantityElement = currentItem.querySelector(".item-quantity");
        const priceElement = currentItem.querySelector(".cart-item-price");
        const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        quantityElement.textContent = currentQuantity + 1;
        updateCartItemPrice(priceElement, pricePerItem, currentQuantity + 1);
        updateTotalPrice();
    });
});

decreaseButtons.forEach((button, index) => {
    button.addEventListener("click", (event) => {
        event.preventDefault();
        const currentItem = event.target.closest(".cart-item");
        const quantityElement = currentItem.querySelector(".item-quantity");
        const priceElement = currentItem.querySelector(".cart-item-price");
        const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
        const currentQuantity = parseInt(quantityElement.textContent);

        if (currentQuantity > 1) {
            quantityElement.textContent = currentQuantity - 1;
            updateCartItemPrice(priceElement, pricePerItem, currentQuantity - 1);
            updateTotalPrice();
        }
    });
});

function updateCartItemPrice(priceElement, pricePerItem, quantity) {
    const totalPrice = (pricePerItem * quantity).toFixed(2);
    priceElement.textContent = "Rs." + totalPrice;
}
function updateTotalPrice() {
    
    const itemElements = document.querySelectorAll(".cart-item");

    itemElements.forEach(function (itemElement) {
        const sale_price = parseFloat(itemElement.querySelector(".cart-item-price").getAttribute("data-price"));
        const quantity = parseInt(itemElement.querySelector(".cart-item-quantity").textContent);
        total += sale_price * quantity;
    });

    const totalPriceElement = document.getElementById("total-price");
    totalPriceElement.textContent = total.toFixed(2);
}
});