document.addEventListener("alpine:init", () => {
Alpine.data("products", () => ({
  items: [
    { id: 1, name: "Robusta Brazil", img: "1.jpg", price: 20000 },
    { id: 2, name: "Arabica Blend", img: "2.jpg", price: 25000 },
    { id: 3, name: "Primo Passo", img: "3.jpg", price: 30000 },
    { id: 4, name: "Coffe Bean", img: "4.jpg", price: 35000 },
    { id: 5, name: "Sumatra Mandheling", img: "5.jpg", price: 40000 },
    { id: 6, name: "Papua Mandheling", img: "1.jpg", price: 45000 },
  ],
}));

  Alpine.store("cart", {
    items: [],  // This is the cart's items array that starts empty
    total: 0,
    quantity: 0,

    // Function to add an item to the cart
    add(newItem) {
      const cartItem = this.items.find((item) => item.id === newItem.id);
      if (!cartItem) {
        this.items.push({ ...newItem, quantity: 1, total: newItem.price });
        this.quantity++;
        this.total += newItem.price;
      } else {
        this.items = this.items.map((item) => {
          if (item.id !== newItem.id) {
            return item;
          } else {
            item.quantity++;
            item.total = item.price * item.quantity;
            this.quantity++;
            this.total += item.price;
            return item;
          }
        });
      }
    },

    // Function to remove an item from the cart
    remove(id) {
      const cartItem = this.items.find((item) => item.id === id);

      if (cartItem.quantity > 1) {
        this.items = this.items.map((item) => {
          if (item.id !== id) {
            return item;
          } else {
            item.quantity--;
            item.total = item.price * item.quantity;
            this.quantity--;
            this.total -= item.price;
            return item;
          }
        });
      } else {
        this.items = this.items.filter((item) => item.id !== id);
        this.quantity--;
        this.total -= cartItem.price;
      }
    },

    // Function to convert numbers to Rupiah currency format
    rupiah(number) {
      return new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
        minimumFractionDigits: 0,
      }).format(number);
    },

    // Function to handle checkout
  async checkout() {
    try {
        const response = await fetch('/orders/checkout/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({
                total: this.total,
                items: this.items,
            }),
        });

        const data = await response.json();

        console.log("Response from server:", data); // Debugging respons

        if (data.status === 'success') {
            // Redirect ke URL yang diberikan
            window.location.href = data.redirect_url;
        } else {
            alert('Error creating order: ' + data.message);
        }
    } catch (error) {
        console.error('Checkout error:', error);
        alert('An error occurred during checkout');
    }
},
  });
});


